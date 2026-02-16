#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate py312
./uvall.sh
jupyter lab --notebook-dir=/mnt/c/Ai
