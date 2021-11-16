"""
Make Job Option for MadGraph
____________________________________________
Script to make a MadGraph steering script
"""

import cmath

def make_JO(MHPPR, outfile, dest_dir='.'):
    """
    Writes a standalone MadGraph generation script
    args:
        MHPPR (float): Mass of the right-handed doubly charged Higgs
        outfile (str): The name of the MadGraph generation directory
        dest_dir (str): The directory to save the MadGraph generation script
    """

    job_option_script = \
f"""
import model lrsm_1_3_2_UFO_DCH
define rm h h2 hp2 hm2 n1 n2 n3
define h++ hl++ hr++
define h-- hl-- hr--
define l+ e+ mu+ ta+
define l- e- mu- ta-
generate p p > h++ h--, h++ > l+ l+, h-- > l- l- / rm 
output {outfile}
shower=pythia8
launch
set MHPPR {MHPPR}
set WHPPL auto
set WHPPR auto
"""
    outfile = f"{dest_dir}/mc.aMGPy8EG_HPPR.txt"

    with open(outfile, "w") as file:
        file.write(job_option_script)

    return outfile