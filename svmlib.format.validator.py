#!/usr/bin/python
import sys

for line in sys.stdin:
    a = line.split(" ")
    a = a[1:]
    pre = 0
    for x in a:
        try:
            idx, val = x.split(":")
        except Exception:
            print "xxx"

        idx = int(idx)
        if idx <= pre:
            print "Error"
            print pre,idx
            print a
            exit(1)
        pre = idx
