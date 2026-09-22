# source this in WSL before running the original-SIMPLER stack with rendering (CPU lavapipe + fake-semaphore layer)
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json
export VK_DRIVER_FILES=/usr/share/vulkan/icd.d/lvp_icd.json
export VK_LAYER_PATH=/mnt/e/research/the_world/third_party/vk_fakesemfd
export VK_INSTANCE_LAYERS=VK_LAYER_the_world_fakesemfd
export PYTHONUNBUFFERED=1
