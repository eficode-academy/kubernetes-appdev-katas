#! /bin/bash

docker run -it -v $(pwd):/go golang:1.13.4 go test . -v