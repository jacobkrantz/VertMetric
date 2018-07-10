#!/bin/bash

python vert.py rouge \
  --generated='./generated.txt' \
  --target='./targets.txt' \
  --out_dir='./reports' \
