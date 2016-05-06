import numpy as np
import os, json

decompositions = ("xxxx", "xx", "zzxx", "zz", "zxx", "z", "zzz", "xxz",
                  "xzx", "xzxxx", "xzzzx", "xxxzx", "xzz", "zzx", "xxx", "x",
                  "zzzx", "xxzx", "zx", "zxxx", "xxxz", "xzzz", "xz", "xzxx")

directory = os.path.dirname(os.path.abspath(__file__))
where = os.path.join(directory, "tables/")
os.chdir(where)
unitaries = np.load("unitaries.npy")
conjugation_table = np.load("conjugation_table.npy")
times_table = np.load("times_table.npy")
cz_table = np.load("cz_table.npy")

with open("by_name.json") as f:
    by_name = json.load(f)

