# Original-stack software rendering: implementation reference

This reference preserves implementation details moved out of the manuscript's Appendix B.
It describes the archived implementation; it is not a claim of Vulkan conformance, a general
software-rendering solution, or independent validation of all synchronization paths.

## Files supplied in the companion snapshot

- `third_party/vk_fakesemfd/fakesemfd_layer.c`: the compatibility-layer source.
- `third_party/vk_fakesemfd/VkLayer_fakesemfd.json`: explicit-layer manifest.
- `third_party/vk_fakesemfd/build.sh`: original WSL build script; its paths are specific to the
  recorded author environment and must be adapted on another machine.
- `scripts/wsl_render_env.sh`: recorded evaluation-process setup, also environment-specific.

No compiled layer binary, Vulkan SDK/header tree, Mesa installation, or full simulator assets
are supplied by this small addition. Prepare the original-stack dependencies separately.

## What the implementation does

| Step | API or structure | Actual behavior and boundary |
|---|---|---|
| Extension enumeration | `vkEnumerateDeviceExtensionProperties` | Adds `VK_KHR_external_semaphore_fd` and `VK_KHR_external_fence_fd` if they are absent. This advertises names without implementing external synchronization. |
| Device creation | `vkCreateDevice`, `ppEnabledExtensionNames` | Removes those names before forwarding device creation to the driver. |
| Semaphore creation | `VkExportSemaphoreCreateInfo` | Removes matching export nodes while handling the supported creation-chain patterns. On an unknown structure it retains the remaining original chain; this is not a general chain rewriter. |
| Fence creation | `VkExportFenceCreateInfo` | Removes consecutive export nodes at the beginning of the chain, not arbitrary nodes anywhere in it. |
| Descriptor calls | `vkGetSemaphoreFdKHR`, `vkImportSemaphoreFdKHR`, `vkGetFenceFdKHR`, `vkImportFenceFdKHR` | All return `VK_ERROR_FEATURE_NOT_PRESENT`. The export functions also set the output descriptor to −1. These are error-returning substitutes, not synchronization implementations. |

Only the semaphore-export substitute has optional call logging, controlled by `FAKESEMFD_LOG`.
The available evaluation records do not contain a complete trace of all four entry points.
Neither successful task execution nor the presence of substitute functions proves that none
were called. The evaluated camera path uses host-memory images and a separate policy-inference
process; it does not request direct CUDA image interoperation. Policy inference may use a GPU.

## Build and activate in a prepared working copy

The following is a relocatable equivalent of the archived build command. Run from a writable
working copy of the companion snapshot after installing a compatible Linux C compiler and Vulkan
headers; replace the header path with the actual installation. The frozen snapshot should remain
unchanged. These commands were documented, not executed during the manuscript revision.

```bash
layer_dir="$PWD/third_party/vk_fakesemfd"
vulkan_headers="/absolute/path/to/vulkan/include"
gcc -O2 -shared -fPIC -Wall -I"$vulkan_headers" \
  -o "$layer_dir/libVkLayer_fakesemfd.so" "$layer_dir/fakesemfd_layer.c"

# Apply only to the evaluation command; no system-wide installation or automatic startup.
VK_LAYER_PATH="$layer_dir" \
VK_INSTANCE_LAYERS=VK_LAYER_the_world_fakesemfd \
  <prepared-evaluation-command>
```

The final command is a template, not a shell-ready command: substitute the prepared evaluation
entry point. Its child processes inherit the environment. Preserve the software renderer/driver
configuration recorded by the original evaluation setup; these variables alone do not select
Mesa lavapipe or establish compatibility with a different driver.

## Scope and evidence

The workaround is restricted to the tested WSL2 software-rendering workload and the creation-chain
patterns above. A workload requiring actual descriptor import/export or external synchronization
is outside its scope. The recorded success-rate comparison is an aggregate protocol check and
does not prove rendering equivalence, absence of compensating errors, or non-reachability of the
substitute entry points. The paper retains these boundaries in Appendix B.

The implementation notes were checked against the local layer source, the original-stack camera
path and sweep client. Runtime records and environment logs were inspected in the author project;
the companion remains a scoped data/code package, not a full installation image.
