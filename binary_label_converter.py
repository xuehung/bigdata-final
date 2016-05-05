import sys

with open(sys.argv[1])as f:
    for line in f:
        label = line[0]
        if label != "0":
            line = "1" + line[1:]
        print line[:-1]
    
