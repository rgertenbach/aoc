#!/usr/bin/python3
import sys
from image import Image

def read_file(filename):
  with open(filename) as f:
    lines = f.read()

  algo, img = lines.split('\n\n')
  algo = algo.strip()
  img = Image.parse(img)
  return algo, img
  

algo, img = read_file(sys.argv[1])
print(str(img.pad().pad().pad().pad()))
img = img.enhance(algo)
print(str(img.pad().pad()))
img = img.enhance(algo)
print(str(img))
print(img.n_lit())




