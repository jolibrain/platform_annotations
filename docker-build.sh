#!/bin/sh

NAME_ROOT=jolibrain/platform_annotations
TAG=latest

FRONTEND_IMAGE=${NAME_ROOT}_frontend:${TAG}
docker build -t $FRONTEND_IMAGE .
docker push $FRONTEND_IMAGE

cd flask

BACKEND_IMAGE=${NAME_ROOT}_backend:${TAG}
docker build -t $BACKEND_IMAGE .
docker push $BACKEND_IMAGE
