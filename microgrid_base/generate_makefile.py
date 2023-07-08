import os

generate_path = "Makefile.tmp"
import ast

def read_file(fname):
    with open(fname, 'r') as f:
        content = f.read()
        return content

for fname in os.listdir("."):
    if fname.endswith(".py"):
        content = read_file(fname)