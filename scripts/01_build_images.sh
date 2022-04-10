#!/bin/bash

set -e

if [ "$1" = "--push" ]; then
    push=1
fi

# base image
docker build -f base/Dockerfile \
    -t ghcr.io/borncrusader/stanford-k8s-nextflow-demo-base:latest .

if [ -n "$push" ]; then
    docker push ghcr.io/borncrusader/stanford-k8s-nextflow-demo-base:latest
fi

# preprocessing scripts
docker build -f preprocessing/00_Dockerfile \
    -t ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-00:latest .

docker build -f preprocessing/01_Dockerfile \
    -t ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-01:latest .

docker build -f preprocessing/02_Dockerfile \
    -t ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-02:latest .

if [ -n "$push" ]; then
    docker push ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-00:latest
    docker push ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-01:latest
    docker push ghcr.io/borncrusader/stanford-k8s-nextflow-demo-pp-02:latest
fi

# model prediction
docker build -f models/Dockerfile \
    -t ghcr.io/borncrusader/stanford-k8s-nextflow-demo-models:latest .

if [ -n "$push" ]; then
    docker push ghcr.io/borncrusader/stanford-k8s-nextflow-demo-models:latest
fi
