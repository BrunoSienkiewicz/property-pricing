#!/bin/bash

if ! [ $# -eq 2 ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Usage: $0 <model_name> <model_version> <feast_repo_dir> <artifacts_dir>"
    echo "Default values: feast_repo_dir=./feature_repo_local, artifacts_dir=./artifacts/<model_name>_<model_version>"
    exit 1
fi

MODEL_NAME=$1
MODEL_VERSION=$2
FEAST_REPO_DIR=${3:-./feature_repo_local}
ARTIFACTS_DIR=${4:-./artifacts}/${MODEL_NAME}_${MODEL_VERSION}

IMAGE_NAME="property_pricing-${MODEL_NAME}:${MODEL_VERSION}"
CONFIG_PATH="./cfgs/${MODEL_NAME}.json"

docker build -t "${IMAGE_NAME}" . \
  --build-arg FEAST_REPO_DIR="${FEAST_REPO_DIR}" \
  --build-arg CONFIG_PATH="${CONFIG_PATH}" \
  --build-arg MODEL_NAME="${MODEL_NAME}" \
  --build-arg MODEL_VERSION="${MODEL_VERSION}" \
  --build-arg ARTIFACTS_DIR="${ARTIFACTS_DIR}"

