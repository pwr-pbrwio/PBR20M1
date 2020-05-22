import random
import sys
seed = sys.argv[4] if len(sys.argv) > 4 else 22052020
random.seed(seed)
up = int(sys.argv[3])
low = int(sys.argv[2])
num = int(sys.argv[1])
r = random.sample(range(low, up), num)
# [random.randint(low, up) for i in range(num)]
r.sort()

print(r)
