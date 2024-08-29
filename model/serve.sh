#!/usr/bin/env bash
# Serve pytorch model
# Usage: ./serve.sh model_name model_version

model_name=$1
model_version=$2

# Serve model
torchserve --start --model-store model_store --models "$model_name"="$model_version.mar"

