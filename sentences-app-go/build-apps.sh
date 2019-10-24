#!/bin/bash

cd apps/age
docker build -t hoeghh/age:1.0 .

cd ../name
docker build -t hoeghh/name:1.0 .

cd ../sentence
docker build -t hoeghh/sentence:1.0 .
