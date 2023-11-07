import pickle
import os

"""Load xy grid data"""
def load_xygrid():
    filename = "xygrid.pkl"
    print(os.popen('pwd').read())
    with open(filename, "r") as input_file:
        d_out = pickle.load(input_file)
    return d_out

def hello():
    print("Hello")
    return 0

