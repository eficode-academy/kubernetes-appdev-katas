#!/bin/bash

docker push hoeghh/age:1.0  &

docker push hoeghh/name:1.0 &

docker push hoeghh/sentence:1.0 &

wait
