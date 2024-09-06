#!/bin/bash

echo "Current shell: $SHELL"
# 環境変数の反映
set -a
source .env
set +a