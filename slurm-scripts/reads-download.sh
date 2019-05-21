#!/bin/bash
#
#SBATCH --job-name={TENX_SAMPLE}_RDS_DL
#SBATCH --output=%j.out

/usr/bin/env tenx reads download {TENX_SAMPLE}
