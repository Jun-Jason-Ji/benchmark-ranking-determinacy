#!/usr/bin/env bash
# Build the explicit layer in place (WSL). Nothing is installed; enable per process with:
#   export VK_LAYER_PATH=/mnt/e/research/the_world/third_party/vk_fakesemfd VK_INSTANCE_LAYERS=VK_LAYER_the_world_fakesemfd
set -euo pipefail
SRC=/mnt/e/research/the_world/third_party/vk_fakesemfd
gcc -O2 -shared -fPIC -Wall -I/mnt/e/research/the_world/third_party/vulkan_headers -o "$SRC/libVkLayer_fakesemfd.so" "$SRC/fakesemfd_layer.c"
echo "built $SRC/libVkLayer_fakesemfd.so"
