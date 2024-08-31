#!/bin/bash

# すべてのイメージを削除
all_images=$(docker images -q)
if [ -n "$all_images" ]; then
    docker rmi $all_images
else
    echo "No images to remove."
fi