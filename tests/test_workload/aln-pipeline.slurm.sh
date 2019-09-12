#!/bin/bash
#TENX DOC: Run the "tenx aln pipeline" command on a slurm cluster
#TENX PARAMS:
#TENX - SAMPLE_NAME: with reads in TENX_DATA_PATH or TENX_REMOTE_DATA_URL
#TENX   REF_NAME: with reference in TENX_DATA_PATH
#
#SBATCH -J __SAMPLE__.aln
#SBATCH --nodes=1 --ntasks-per-node=2
#SBATCH --signal=2
#SBATCH --no-requeue
#SBATCH --mem=8G
#SBATCH -o /logs/__SAMPLE__.aln.out

set -e
. /etc/profile.d/longranger.sh
tenx aln pipeline __SAMPLE__ __REF__
