#!/bin/bash
#TENX DOC:  Run the "tenx ref download" command on a slurm cluster
#TENX PARAMS:
#TENX   REF_NAME: with reference in TENX_REMOTE_REFS_URL

#SBATCH -J {{ REF_NAME }}.ref-dl
#SBATCH --nodes=1 --ntasks-per-node=2
#SBATCH --signal=2
#SBATCH --no-requeue
#SBATCH --mem=8G
#SBATCH -o {{ TENX_DATA_PATH }}/logs/{{ REF_NAME }}.ref-dl.out

set -e
tenx ref download {{ REF_NAME }}
