#!/bin/bash
#
#SBATCH --job-name={TENX_REF}_REF_DL
#SBATCH --output=%j.out

/usr/bin/env tenx ref download {TENX_REF}
