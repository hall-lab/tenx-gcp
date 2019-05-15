#!/bin/bash
set -e
source /apps/supernova/sourceme.bash
echo Running mkoutput...
echo Entering /tmp/TESTER/assembly/mkoutput
mkdir -p /tmp/TESTER/assembly/mkoutput
cd /tmp/TESTER/assembly/mkoutput
echo Running mkoutput raw...
supernova mkoutput --asmdir=/tmp/TESTER/assembly/outs/assembly --outprefix=TESTER.raw --style=raw
echo Running mkoutput megabubbles...
supernova mkoutput --asmdir=/tmp/TESTER/assembly/outs/assembly --outprefix=TESTER.megabubbles --style=megabubbles
echo Running mkoutput pseudohap2...
supernova mkoutput --asmdir=/tmp/TESTER/assembly/outs/assembly --outprefix=TESTER.pseudohap2 --style=pseudohap2
echo Running mkoutput...OK
