#!/bin/bash
#
#SBATCH --job-name={TENX_SAMPLE}_ALN
#SBATCH --output=%j.out

/usr/bin/env tenx alignment align {TENX_SAMPLE}
