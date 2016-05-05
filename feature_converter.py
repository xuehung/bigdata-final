#!/usr/bin/python

# filename: feature_converter.py
# description: this helps combine some features (columns) and generate new ones
# usage: cat <input file path> | ./feature_converter.py

import sys

for line in sys.stdin:
    feature = line.strip().split(" ")
    feature = map(lambda x: int(x.strip().split(":")[1]), feature[1:])
    print feature
    
