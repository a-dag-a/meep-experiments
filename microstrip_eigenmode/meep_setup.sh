#!/bin/bash
# Simple setup script for VCl environment
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p /home/bgpillai/miniconda
export PATH= /home/bgpillai/miniconda/bin:$PATH


# conda init

# Call conda init once to setup the shell
~/miniconda/bin/conda init

# Serial variant of pymeep
# conda create -n mp -c conda-forge pymeep pymeep-extras


# Parallel variant of pymeep
conda create -n pmp -c conda-forge pymeep=*=mpi_mpich_*
#conda activate pmp

