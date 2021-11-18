#!/bin/python3
"""
Generate Doubly Charged Higgs processes
_____________________________________________________________________
Run standalone MadGraph on ht condor batch system
Example Usage:
python3 generate_MLRSM_DCH.py 700 -batch=True
Condor documentation:
https://batchdocs.web.cern.ch/local/quick.html
"""

import os
import sys
import argparse
from make_HPPR_JO import make_JO
from datetime import datetime


def make_dir(path, extn=""):
    """
    Function to make a new directory - if directory already exists will create a new unique directory using time/date
    args:
        path (str): Path to directory to be created
    returns:
        path (str): Returns the path to the directory created 
    """

    if extn != "":
        path += "_" + str(extn)

    try:
        os.mkdir(path)
    except OSError:
        now = datetime.now()
        path = path + "_" + now.strftime("%Y-%m-%d_%H.%M.%S")
        make_dir(path)
    return path

def write_batch_script(args):
    """
    Write batch system executable
    This copies the python scripts and MadGraph to condor directory and runs the code like it would locally
    At the end it copies everything back to this directory (use rsync so that uou don't have to copy MG back)
    Note: Do not write a block comment to run_generation.sh - this will cause job to fail
    args: 
        args: arguements for generate_MLRSM_DCH.py (don't set -batch=True !)
    returns:
        None
    """
    current_dir = os.getcwd()
    command = f"#!/bin/bash \n"
    command += f"cp -r ../{current_dir}/*.py . \n"
    command += f"cp -r ../{current_dir}/MG5_aMC_v3_1_1 . \n"
    command += f"python3 generate_MLRSM_DCH.py {args.MHPPR} | tee {args.MHPPR}.log \n"
    command += f"rsync -av --progress * {current_dir} --exclude MG5_aMC_v3_1_1"
    # command += f"cp -r * {current_dir} \n"
    with open("run_generation.sh", 'w') as exe:
        exe.write(command)

def main():

    # Get user arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("MHPPR", help="Mass of HR++ boson in GeV", type=float)
    parser.add_argument("-batch", help="Use ht condor batch system", type=bool, default=False)
    args = parser.parse_args()

    # Make a new directory to run in and move into it
    new_dir = f"run_{args.MHPPR}"
    start_dir = os.getcwd()
    if args.batch is True:
        new_dir = f"batch_{args.MHPPR}"
    os.system(f"mkdir {new_dir}")
    os.chdir(new_dir)

    # If running on batch system
    if args.batch:
        write_batch_script(args)
        os.system("cp run_generation.sh ~ ")
        os.system(f"cp ../htc_generation.submit ~")
        os.chdir(os.path.expanduser('~'))
        # os.system(f"condor_submit htc_generation.submit -batch-name generate_MHPPR_{args.MHPPR}")
        sys.exit(0)

    # Make MadGraph steering script
    outfile = f"MG5aMC_SSmumujj_MHPPR_{args.MHPPR}"
    generation_script = make_JO(args.MHPPR, outfile)
    
    # Run event generation. Note python2 usage since setting conda enviroments up on condor isn't straightforward
    os.system(f"python2 ../MG5_aMC_v3_1_1/bin/mg5_aMC {generation_script} | tee {args.MHPPR}_generation.log")
    sys.exit(0)
    

if __name__ == "__main__":
    main()

  


