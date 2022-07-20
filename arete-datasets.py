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
    [X] - BACMET.
    [X] - VF_DB.
    [X] - CAZy DB. Available as .fna with curl
    [X] - RGI. Available as .tar with curl

//
//  More may be added with development.
/////////////////////////////////////////////////////////////////////////////"""

PROGRAM = "arete-datasets"
VERSION = "0.0.2"
STDOUT = 11
STDERR = 12

logging.addLevelName(STDOUT, "STDOUT")
logging.addLevelName(STDERR, "STDERR")

def check_cache():
    pass

def download_kraken_db(cache_dir):
    print("*"*80)
    s = "*** Download Kraken2 DB"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl https://genome-idx.s3.amazonaws.com/kraken/k2_standard_8gb_20201202.tar.gz --output {cache_dir}/k2_standard_8gb_20201202.tar.gz')
    execute(f'mkdir -p {cache_dir}/k2_standard_8gb_20201202')
    execute(f'tar xvf {cache_dir}/k2_standard_8gb_20201202.tar.gz -C {cache_dir}/k2_standard_8gb_20201202')
    print()

def download_cazy_db(cache_dir):
    print("*"*80)
    s = "*** Download CAZy DB"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    cmd = "curl https://bcb.unl.edu/dbCAN2/download/CAZyDB.07312020.fa --output {0}/CAZyDB.07312020.fa".format(cache_dir)
    execute(cmd)
    print()

def download_vfdb(cache_dir):
    print("*"*80)
    s = "*** Download VFDB"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl http://www.mgc.ac.cn/VFs/Down/VFDB_setB_pro.fas.gz --output {cache_dir}/VFDB_setB_pro.fas.gz')
    print()

def download_bacmet(cache_dir):
    print("*"*80)
    s = "*** Download BacMET"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    execute(f'curl http://bacmet.biomedicine.gu.se/download/BacMet2_predicted_database.fasta.gz --output {cache_dir}/BacMet2_predicted_database.fasta.gz')
    print()

def download_rgi(cache_dir):
    print("*"*80)
    s = "*** Download RGI/CARD"
    print(s, " "*(75- len(s)), "***")
    print("*"*80)
    curl_cmd = 'curl https://card.mcmaster.ca/latest/data --output {0}/card.tar.bz2'.format(cache_dir)
    tar_cmd = 'tar xvf {0}/card.tar.bz2 --directory {0}'.format(cache_dir)
    execute(curl_cmd)
    execute(tar_cmd)
    fh = open('{0}/card.json'.format(cache_dir))
    card=json.load(fh)
    with open('{0}/card.version.txt'.format(cache_dir), 'w') as outfh:
        outfh.write(card['_version'])
    print()

if __name__ == '__main__':
    pipeline_path = sys.argv[1]

    execute(f'mkdir -p {pipeline_path}/dbcache')
    execute(f'mkdir -p {pipeline_path}/container_cache')

    cache_dir = "{0}/dbcache".format(pipeline_path)
    print("+++")
    print(cache_dir)
    print("+++")

    #Download data
    download_rgi(cache_dir)
    download_kraken_db(cache_dir)
    download_cazy_db(cache_dir)
    download_bacmet(cache_dir)
    download_vfdb(cache_dir)
