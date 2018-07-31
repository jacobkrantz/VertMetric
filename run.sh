#!/bin/bash

python vert.py score \
  --generated='./generated.txt' \
  --target='./targets.txt' \
  --out_dir='./reports' \
  --rouge_type recall
