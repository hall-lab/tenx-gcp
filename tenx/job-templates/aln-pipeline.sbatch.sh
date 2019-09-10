#!/bin/bash
# PURPOSE:  Run the "tenx aln pipeline" command on a slurm cluster
# REQUIRES: SAMPLE_NAME (with reads in TENX_DATA_PATH or TENX_REMOTE_DATA_URL)
#           REF_NAME (with reference in TENX_DATA_PATH)
#
#SBATCH -J {{ SAMPLE_NAME }}.aln
#SBATCH --nodes=1 --ntasks-per-node=2
#SBATCH --signal=2
#SBATCH --no-requeue
#SBATCH --mem=8G
#SBATCH -o logs/{{ SAMPLE_NAME }}.aln.out

set -e
. /etc/profile.d/longranger.sh
tenx aln pipeline {{ SAMPLE_NAME }} {{ REF_NAME }}
