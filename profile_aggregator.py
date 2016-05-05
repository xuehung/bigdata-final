sum = [0,0,0,0,0]
with open("30k_profile") as f:
    for line in f:
        line = line[1:-2]
        line = line.split(",")
        for i in range(len(sum)):
            sum[i] = sum[i] + int(line[i].strip())
print sum
    
