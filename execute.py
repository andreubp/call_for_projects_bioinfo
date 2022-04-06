
import argparse
import os.path
import run
import pandas as pd
parser = argparse.ArgumentParser()

parser.add_argument("path_file_csv", type=str)

args = parser.parse_args() 


if  os.path.isfile(args.path_file_csv):
    run.main(args.path_file_csv)
else:
    print("\n -------------------------------------------------------------------")
    print(" |The received file has problems (incorrect format or does not exist)|")
    print(" --------------------------------------------------------------------\n")

