#!/usr/bin/env bash

set -x

if [ -z ${PUBLIC_DNS+x} ]; then
    echo "Environment variable PUBLIC_DNS is unset"
    exit 1
fi

if [ -z ${SSH_CONFIG_DIR+x} ]; then
    echo "Environment variable SSH_CONFIG_DIR is unset"
    exit 1
fi

if [ -z ${PUBLIC_IP+x} ]; then
    echo "Environment variable PUBLIC_IP is unset"
    exit 1
fi

pytest -v tests --junit-xml=report.xml
