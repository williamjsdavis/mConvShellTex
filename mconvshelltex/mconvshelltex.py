import pickle

"""Load xy grid data"""
def load_xygrid():
    filename = "mConvShellTex/mconvshelltex/xygrid.pkl"
    with open(filename, "rb") as input_file:
        d_out = pickle.load(input_file)
    return d_out

"""Load example temperature data"""
def load_example_tdata():
    filename = "mConvShellTex/mconvshelltex/tdata-example.pkl"
    with open(filename, "rb") as input_file:
        d_out = pickle.load(input_file)
    return d_out

def hello():
    print("Hello")
    return 0

