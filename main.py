#!/usr/bin/env python

"""
Python script to generate the list of projects for the UPF bioinformatic's master from the Google Form.
It is intended to download the CSV file from the dev google form page and pass it as argument in this file.
"""


import argparse
import os.path
import project_generator
import pandas as pd

__author__ = "Andreu Bofill"
__copyright__ = "Copyright 2021, Universitat Pompeu Fabra"
__credits__ = ["Andreu Bofill Pumarola"]
__version__ = "0.0.1"
__date__ = "20210112"
__maintainer__ = "Andreu Bofill Pumarola"
__email__ = "andreu.bofill01@alumni.upf.edu"
__status__ = "Dev"


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("path_file_csv", type=str)
    args = parser.parse_args()


    if  os.path.isfile(args.path_file_csv):
        project_generator.main(args.path_file_csv)
    else:
        print("\n -------------------------------------------------------------------")
        print(" |The received file has problems (incorrect format or does not exist)|")
        print(" --------------------------------------------------------------------\n")
