/*
 * VK_LAYER_the_world_fakesemfd — explicit Vulkan layer (VK_LAYER_PATH + VK_INSTANCE_LAYERS) that advertises VK_KHR_external_semaphore_fd
 * (and VK_KHR_external_fence_fd) on physical devices that lack them, strips those names at vkCreateDevice,
 * removes VkExportSemaphoreCreateInfo / VkExportFenceCreateInfo from create-info chains, and stubs the
 * fd import/export entry points. Purpose: let the SAPIEN 2 (svulkan2) renderer initialise on Mesa lavapipe
 * inside WSL2, where no driver offers fd-based external semaphores. Rendering itself does not use them
 * unless CUDA interop is requested. Build: see build.sh.
 */
#define VK_NO_PROTOTYPES
#include <vulkan/vulkan.h>
#include <vulkan/vk_layer.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(VkInstance inst, const char *name);
VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetDeviceProcAddr(VkDevice dev, const char *name);
VKAPI_ATTR VkResult VKAPI_CALL vkNegotiateLoaderLayerInterfaceVersion(VkNegotiateLayerInterface *p);

#define FAKE_SEM "VK_KHR_external_semaphore_fd"
#define FAKE_FENCE "VK_KHR_external_fence_fd"

typedef struct InstEntry { void *key; PFN_vkGetInstanceProcAddr gipa; PFN_vkEnumerateDeviceExtensionProperties enumDevExt;
                           PFN_vkCreateDevice createDevice; PFN_vkDestroyInstance destroyInstance; struct InstEntry *next; } InstEntry;
typedef struct DevEntry { void *key; PFN_vkGetDeviceProcAddr gdpa; PFN_vkCreateSemaphore createSemaphore; PFN_vkCreateFence createFence;
                          PFN_vkDestroyDevice destroyDevice; struct DevEntry *next; } DevEntry;
static InstEntry *g_inst = NULL;
static DevEntry *g_dev = NULL;
static int g_log = -1;

static void logmsg(const char *m) { if (g_log < 0) g_log = getenv("FAKESEMFD_LOG") != NULL; if (g_log) fprintf(stderr, "[fakesemfd] %s\n", m); }
static void *dkey(const void *h) { return *(void **)h; }
static InstEntry *find_inst(void *key) { for (InstEntry *e = g_inst; e; e = e->next) if (e->key == key) return e; return NULL; }
static DevEntry *find_dev(void *key) { for (DevEntry *e = g_dev; e; e = e->next) if (e->key == key) return e; return NULL; }

static VKAPI_ATTR VkResult VKAPI_CALL layer_CreateInstance(const VkInstanceCreateInfo *ci, const VkAllocationCallbacks *ac, VkInstance *inst) {
    VkLayerInstanceCreateInfo *lci = (VkLayerInstanceCreateInfo *)ci->pNext;
    while (lci && !(lci->sType == VK_STRUCTURE_TYPE_LOADER_INSTANCE_CREATE_INFO && lci->function == VK_LAYER_LINK_INFO))
        lci = (VkLayerInstanceCreateInfo *)lci->pNext;
    if (!lci) return VK_ERROR_INITIALIZATION_FAILED;
    PFN_vkGetInstanceProcAddr gipa = lci->u.pLayerInfo->pfnNextGetInstanceProcAddr;
    lci->u.pLayerInfo = lci->u.pLayerInfo->pNext;
    PFN_vkCreateInstance create = (PFN_vkCreateInstance)gipa(VK_NULL_HANDLE, "vkCreateInstance");
    VkResult r = create(ci, ac, inst);
    if (r != VK_SUCCESS) return r;
    InstEntry *e = calloc(1, sizeof *e);
    e->key = dkey(*inst); e->gipa = gipa;
    e->enumDevExt = (PFN_vkEnumerateDeviceExtensionProperties)gipa(*inst, "vkEnumerateDeviceExtensionProperties");
    e->createDevice = (PFN_vkCreateDevice)gipa(*inst, "vkCreateDevice");
    e->destroyInstance = (PFN_vkDestroyInstance)gipa(*inst, "vkDestroyInstance");
    e->next = g_inst; g_inst = e;
    logmsg("instance created");
    return VK_SUCCESS;
}

static VKAPI_ATTR void VKAPI_CALL layer_DestroyInstance(VkInstance inst, const VkAllocationCallbacks *ac) {
    InstEntry *e = find_inst(dkey(inst));
    if (!e) return;
    e->destroyInstance(inst, ac);
    InstEntry **pp = &g_inst; while (*pp && *pp != e) pp = &(*pp)->next; if (*pp) *pp = e->next; free(e);
}

static VKAPI_ATTR VkResult VKAPI_CALL layer_EnumerateDeviceExtensionProperties(VkPhysicalDevice pd, const char *layerName, uint32_t *count, VkExtensionProperties *props) {
    InstEntry *e = find_inst(dkey(pd));
    if (!e) return VK_ERROR_INITIALIZATION_FAILED;
    if (layerName && strcmp(layerName, "VK_LAYER_the_world_fakesemfd") == 0) { *count = 0; return VK_SUCCESS; }
    uint32_t n = 0;
    VkResult r = e->enumDevExt(pd, layerName, &n, NULL);
    if (r != VK_SUCCESS) return r;
    VkExtensionProperties *all = calloc(n + 2, sizeof *all);
    r = e->enumDevExt(pd, layerName, &n, all);
    if (r != VK_SUCCESS) { free(all); return r; }
    int hasSem = 0, hasFence = 0;
    for (uint32_t i = 0; i < n; i++) { if (!strcmp(all[i].extensionName, FAKE_SEM)) hasSem = 1; if (!strcmp(all[i].extensionName, FAKE_FENCE)) hasFence = 1; }
    if (!hasSem) { strncpy(all[n].extensionName, FAKE_SEM, VK_MAX_EXTENSION_NAME_SIZE - 1); all[n].specVersion = 1; n++; logmsg("advertising " FAKE_SEM); }
    if (!hasFence) { strncpy(all[n].extensionName, FAKE_FENCE, VK_MAX_EXTENSION_NAME_SIZE - 1); all[n].specVersion = 1; n++; }
    if (!props) { *count = n; free(all); return VK_SUCCESS; }
    uint32_t m = *count < n ? *count : n;
    memcpy(props, all, m * sizeof *props);
    *count = m; free(all);
    return m < n ? VK_INCOMPLETE : VK_SUCCESS;
}

static VKAPI_ATTR VkResult VKAPI_CALL layer_CreateDevice(VkPhysicalDevice pd, const VkDeviceCreateInfo *ci, const VkAllocationCallbacks *ac, VkDevice *dev) {
    InstEntry *ie = find_inst(dkey(pd));
    if (!ie) return VK_ERROR_INITIALIZATION_FAILED;
    VkLayerDeviceCreateInfo *lci = (VkLayerDeviceCreateInfo *)ci->pNext;
    while (lci && !(lci->sType == VK_STRUCTURE_TYPE_LOADER_DEVICE_CREATE_INFO && lci->function == VK_LAYER_LINK_INFO))
        lci = (VkLayerDeviceCreateInfo *)lci->pNext;
    if (!lci) return VK_ERROR_INITIALIZATION_FAILED;
    PFN_vkGetInstanceProcAddr gipa = lci->u.pLayerInfo->pfnNextGetInstanceProcAddr;
    PFN_vkGetDeviceProcAddr gdpa = lci->u.pLayerInfo->pfnNextGetDeviceProcAddr;
    lci->u.pLayerInfo = lci->u.pLayerInfo->pNext;
    /* strip the fake extensions */
    VkDeviceCreateInfo ci2 = *ci;
    const char **names = calloc(ci->enabledExtensionCount + 1, sizeof *names);
    uint32_t k = 0;
    for (uint32_t i = 0; i < ci->enabledExtensionCount; i++) {
        const char *nm = ci->ppEnabledExtensionNames[i];
        if (!strcmp(nm, FAKE_SEM) || !strcmp(nm, FAKE_FENCE)) { logmsg("stripping requested fake extension"); continue; }
        names[k++] = nm;
    }
    ci2.enabledExtensionCount = k; ci2.ppEnabledExtensionNames = names;
    PFN_vkCreateDevice create = (PFN_vkCreateDevice)gipa(VK_NULL_HANDLE, "vkCreateDevice");
    VkResult r = create(pd, &ci2, ac, dev);
    free(names);
    if (r != VK_SUCCESS) { logmsg("next vkCreateDevice failed"); return r; }
    DevEntry *e = calloc(1, sizeof *e);
    e->key = dkey(*dev); e->gdpa = gdpa;
    e->createSemaphore = (PFN_vkCreateSemaphore)gdpa(*dev, "vkCreateSemaphore");
    e->createFence = (PFN_vkCreateFence)gdpa(*dev, "vkCreateFence");
    e->destroyDevice = (PFN_vkDestroyDevice)gdpa(*dev, "vkDestroyDevice");
    e->next = g_dev; g_dev = e;
    logmsg("device created");
    return VK_SUCCESS;
}

static VKAPI_ATTR void VKAPI_CALL layer_DestroyDevice(VkDevice dev, const VkAllocationCallbacks *ac) {
    DevEntry *e = find_dev(dkey(dev));
    if (!e) return;
    e->destroyDevice(dev, ac);
    DevEntry **pp = &g_dev; while (*pp && *pp != e) pp = &(*pp)->next; if (*pp) *pp = e->next; free(e);
}

static VKAPI_ATTR VkResult VKAPI_CALL layer_CreateSemaphore(VkDevice dev, const VkSemaphoreCreateInfo *ci, const VkAllocationCallbacks *ac, VkSemaphore *sem) {
    DevEntry *e = find_dev(dkey(dev));
    if (!e) return VK_ERROR_INITIALIZATION_FAILED;
    VkSemaphoreCreateInfo ci2 = *ci;
    /* drop VkExportSemaphoreCreateInfo anywhere in the chain by rebuilding a shallow copy of the chain heads we know */
    const VkBaseInStructure *p = (const VkBaseInStructure *)ci->pNext;
    VkBaseInStructure *copies[8]; int n = 0; const void *first = NULL; VkBaseInStructure *last = NULL;
    while (p && n < 8) {
        if (p->sType == VK_STRUCTURE_TYPE_EXPORT_SEMAPHORE_CREATE_INFO) { logmsg("dropping VkExportSemaphoreCreateInfo"); p = p->pNext; continue; }
        /* keep the original struct but we must be able to relink; copy header-only is unsafe, so relink via the original pointers:
           since we only ever DROP entries, we can point 'last->pNext' at the original next kept struct by copying the kept struct
           into a small buffer when it is a VkSemaphoreTypeCreateInfo (the only other struct svulkan2 uses). */
        if (p->sType == VK_STRUCTURE_TYPE_SEMAPHORE_TYPE_CREATE_INFO) {
            VkSemaphoreTypeCreateInfo *c = calloc(1, sizeof *c); *c = *(const VkSemaphoreTypeCreateInfo *)p; c->pNext = NULL;
            copies[n++] = (VkBaseInStructure *)c;
            if (!first) first = c; else last->pNext = (const VkBaseInStructure *)c;
            last = (VkBaseInStructure *)c;
        } else {
            /* unknown struct: keep the rest of the chain as-is from here */
            if (!first) first = p; else last->pNext = p;
            break;
        }
        p = p->pNext;
    }
    ci2.pNext = first;
    VkResult r = e->createSemaphore(dev, &ci2, ac, sem);
    for (int i = 0; i < n; i++) free(copies[i]);
    return r;
}

static VKAPI_ATTR VkResult VKAPI_CALL layer_CreateFence(VkDevice dev, const VkFenceCreateInfo *ci, const VkAllocationCallbacks *ac, VkFence *f) {
    DevEntry *e = find_dev(dkey(dev));
    if (!e) return VK_ERROR_INITIALIZATION_FAILED;
    VkFenceCreateInfo ci2 = *ci;
    const VkBaseInStructure *p = (const VkBaseInStructure *)ci->pNext;
    while (p && p->sType == VK_STRUCTURE_TYPE_EXPORT_FENCE_CREATE_INFO) { logmsg("dropping VkExportFenceCreateInfo"); p = p->pNext; }
    ci2.pNext = p;
    return e->createFence(dev, &ci2, ac, f);
}

static VKAPI_ATTR VkResult VKAPI_CALL stub_GetSemaphoreFdKHR(VkDevice dev, const VkSemaphoreGetFdInfoKHR *info, int *fd) { (void)dev; (void)info; if (fd) *fd = -1; logmsg("vkGetSemaphoreFdKHR stub"); return VK_ERROR_FEATURE_NOT_PRESENT; }
static VKAPI_ATTR VkResult VKAPI_CALL stub_ImportSemaphoreFdKHR(VkDevice dev, const VkImportSemaphoreFdInfoKHR *info) { (void)dev; (void)info; return VK_ERROR_FEATURE_NOT_PRESENT; }
static VKAPI_ATTR VkResult VKAPI_CALL stub_GetFenceFdKHR(VkDevice dev, const VkFenceGetFdInfoKHR *info, int *fd) { (void)dev; (void)info; if (fd) *fd = -1; return VK_ERROR_FEATURE_NOT_PRESENT; }
static VKAPI_ATTR VkResult VKAPI_CALL stub_ImportFenceFdKHR(VkDevice dev, const VkImportFenceFdInfoKHR *info) { (void)dev; (void)info; return VK_ERROR_FEATURE_NOT_PRESENT; }

static PFN_vkVoidFunction device_intercept(const char *name) {
    if (!strcmp(name, "vkGetDeviceProcAddr")) return (PFN_vkVoidFunction)vkGetDeviceProcAddr;
    if (!strcmp(name, "vkDestroyDevice")) return (PFN_vkVoidFunction)layer_DestroyDevice;
    if (!strcmp(name, "vkCreateSemaphore")) return (PFN_vkVoidFunction)layer_CreateSemaphore;
    if (!strcmp(name, "vkCreateFence")) return (PFN_vkVoidFunction)layer_CreateFence;
    if (!strcmp(name, "vkGetSemaphoreFdKHR")) return (PFN_vkVoidFunction)stub_GetSemaphoreFdKHR;
    if (!strcmp(name, "vkImportSemaphoreFdKHR")) return (PFN_vkVoidFunction)stub_ImportSemaphoreFdKHR;
    if (!strcmp(name, "vkGetFenceFdKHR")) return (PFN_vkVoidFunction)stub_GetFenceFdKHR;
    if (!strcmp(name, "vkImportFenceFdKHR")) return (PFN_vkVoidFunction)stub_ImportFenceFdKHR;
    return NULL;
}

VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetDeviceProcAddr(VkDevice dev, const char *name) {
    PFN_vkVoidFunction f = device_intercept(name);
    if (f) return f;
    DevEntry *e = dev ? find_dev(dkey(dev)) : NULL;
    return e ? e->gdpa(dev, name) : NULL;
}

VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL vkGetInstanceProcAddr(VkInstance inst, const char *name) {
    if (!strcmp(name, "vkGetInstanceProcAddr")) return (PFN_vkVoidFunction)vkGetInstanceProcAddr;
    if (!strcmp(name, "vkCreateInstance")) return (PFN_vkVoidFunction)layer_CreateInstance;
    if (!strcmp(name, "vkDestroyInstance")) return (PFN_vkVoidFunction)layer_DestroyInstance;
    if (!strcmp(name, "vkEnumerateDeviceExtensionProperties")) return (PFN_vkVoidFunction)layer_EnumerateDeviceExtensionProperties;
    if (!strcmp(name, "vkCreateDevice")) return (PFN_vkVoidFunction)layer_CreateDevice;
    PFN_vkVoidFunction f = device_intercept(name);
    if (f) return f;
    InstEntry *e = inst ? find_inst(dkey(inst)) : NULL;
    return e ? e->gipa(inst, name) : NULL;
}

VKAPI_ATTR VkResult VKAPI_CALL vkNegotiateLoaderLayerInterfaceVersion(VkNegotiateLayerInterface *p) {
    if (!p || p->sType != LAYER_NEGOTIATE_INTERFACE_STRUCT) return VK_ERROR_INITIALIZATION_FAILED;
    if (p->loaderLayerInterfaceVersion >= 2) {
        p->loaderLayerInterfaceVersion = 2;
        p->pfnGetInstanceProcAddr = vkGetInstanceProcAddr;
        p->pfnGetDeviceProcAddr = vkGetDeviceProcAddr;
        p->pfnGetPhysicalDeviceProcAddr = NULL;
    }
    return VK_SUCCESS;
}
