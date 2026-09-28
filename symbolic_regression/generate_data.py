import math
import random

def f(x):
  return (5 * math.sin(x) * x**3) / (120 * x)

def f_noise(x):
  return f(x) * random.uniform(0.8, 1.2) + random.uniform(-0.2, 0.2)

min_x = 0
max_x = 20
num_points = 250

print('x,f_x')
for i in range(num_points):
  x = random.uniform(min_x, max_x)
  print(f'{x},{f_noise(x)}')
