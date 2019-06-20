#!/usr/bin/env bash

docker build --tag=paddle:lac_env -f Dockerfile_lac_env .
docker build --tag=paddle:lac -f Dockerfile .
