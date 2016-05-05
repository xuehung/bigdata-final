#!/usr/bin/python
# usage: ./prediction_result_combinator.py <output folder made by spark conaing part-xxxx files>

import os
import sys
import json
import random
from quadratic_weighted_kappa import quadratic_weighted_kappa 

PREDICTION="prediction"
# PREDICTION="predictedLabel"

FOLDER = sys.argv[1]

predict = []
true = []
for filename in os.listdir(FOLDER):
    if not filename.startswith("part"):
        continue
    for line in open(os.path.join(FOLDER, filename)):
        data = json.loads(line.strip())
        predict.append(int(float(data[PREDICTION])))
        if data[PREDICTION] != "0.0":
            print "!"
        true.append(int(float(data["label"])))

def get_ans():
    n = random.random()
    if n <= 0.728:
        return 0
    elif n <= 0.794:
        return 1
    elif n <= 0.953:
        return 2
    elif n <= 0.979:
        return 3
    else:
        return 4


print quadratic_weighted_kappa(predict, true, 0, 4)
