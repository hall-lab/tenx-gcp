#!/bin/bash
#
#SBATCH --job-name={TENX_SAMPLE}_ALN_PIPE
#SBATCH --output=%j.out

/usr/bin/env tenx alignment pipeline {TENX_SAMPLE} {TENX_REF}
