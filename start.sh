#!/bin/bash
app="cross-entropy-services"
docker build -t ${app} .
docker run -d -p 4400:80 \
  --name=${app} \
  -v $PWD:/app ${app}