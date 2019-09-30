#!/bin/bash

cd apps/age
docker build -t age:latest .

cd ../name
docker build -t name:latest .

cd ../sentence
docker build -t sentence:latest .