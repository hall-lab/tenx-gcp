#!/bin/bash
set -e
source /apps/supernova/sourceme.bash
mkdir -p /tmp/TESTER
cd /tmp/TESTER
supernova run --id=assembly --fastqs=/tmp/TESTER/reads --uiport=18080 --nodebugmem --localcores=50 --localmem=400
