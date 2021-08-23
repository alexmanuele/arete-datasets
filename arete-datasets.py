import glob
import json
import logging
import os
import sys

#from Bio import SeqIO
from executor import execute, ExternalCommand, ExternalCommandFailed

"""////////////////////////////////////////////////////////////////////////////
/// Script to download datasets used in ARETE pipepline.
/// Motivated by limited internet access in HPC compute nodes.
//  Datasets required:
    [X] - Kraken2. Available as .tar with curl
    [ ] - BACMET. Unkown
    [ ] - VF_DB. Unkown
    [X] - CAZy DB. Available as .fna with curl
    [X] - RGI. Available as .tar with curl
    [X] - NCBI AMR HMM. Available as .lib via curl
//
//  More may be added with development.
/////////////////////////////////////////////////////////////////////////////"""

PROGRAM = "arete-datasets"
VERSION = "0.0.1"
STDOUT = 11
STDERR = 12
CACHE_DIR = f'{os.path.expanduser("~")}/.arete'
CACHE_JSON = f'{CACHE_DIR}/datasets.json'
EXPIRATION = 15 # Refresh db info if cache is older than 15 days
logging.addLevelName(STDOUT, "STDOUT")
logging.addLevelName(STDERR, "STDERR")

def check_cache():
    pass

def download_kraken_db():
    print("*"*80)
    s = "*** Download Kraken2 DB"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl https://genome-idx.s3.amazonaws.com/kraken/k2_standard_8gb_20201202.tar.gz --output {CACHE_DIR}/kraken2/k2_standard_8gb_20201202.tar.gz')
    execute(f'mkdir -p {CACHE_DIR}/kraken2/k2_standard_8gb_20201202')
    execute(f'tar xvf {CACHE_DIR}/kraken2/k2_standard_8gb_20201202.tar.gz -C {CACHE_DIR}/kraken2/k2_standard_8gb_20201202')
    print()

def download_cazy_db():
    print("*"*80)
    s = "*** Download CAZy DB"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl https://bcb.unl.edu/dbCAN2/download/CAZyDB.07312020.fa --output {CACHE_DIR}/CAZy/CAZyDB.07312020.fa')
    print()
def download_rgi():
    print("*"*80)
    s = "*** Download RGI/CARD"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl https://card.mcmaster.ca/latest/data --output {CACHE_DIR}/card/card.tar.bz2')
    execute(f'tar xvf {CACHE_DIR}/card/card.tar.bz2 -C {CACHE_DIR}/card')
    fh = open('{0}/card/card.json'.format(CACHE_DIR))
    card=json.load(fh)
    with open('{0}/card/card.version.txt'.format(CACHE_DIR), 'w') as outfh:
        outfh.write(card['_version'])
    print()

def download_ncbi_amr_hmm():
    print("*"*80)
    s = "*** Download NCBI AMR HMM"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinder/data/latest/AMR.LIB -O {CACHE_DIR}/pathracer/AMR.LIB')
    print()

if __name__ == '__main__':
    #### TODO check cache and conditional db download
    # cache...

    #Make directories
    execute(f'mkdir -p {CACHE_DIR}/card')
    execute(f'mkdir -p {CACHE_DIR}/kraken2')
    execute(f'mkdir -p {CACHE_DIR}/CAZy')
    execute(f'mkdir -p {CACHE_DIR}/pathracer')

    #Download data
    download_rgi()
    download_kraken_db()
    download_cazy_db()
    download_ncbi_amr_hmm()
