#!/bin/bash
#
#SBATCH --job-name={TENX_SAMPLE}_UL_ALN
#SBATCH --output=%j.out

/usr/bin/env tenx alignment upload {TENX_SAMPLE}
