#!/bin/bash

# 実行中のコンテナを停止
running_containers=$(docker ps -q)
if [ -n "$running_containers" ]; then
    docker stop $running_containers
else
    echo "No running containers to stop."
fi

# すべてのコンテナを削除
all_containers=$(docker ps -a -q)
if [ -n "$all_containers" ]; then
    docker rm $all_containers
else
    echo "No containers to remove."
fi