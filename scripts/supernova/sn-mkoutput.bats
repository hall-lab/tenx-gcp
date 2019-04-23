#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  # test script
  export SCRIPT_PATH="${TESTDIR}/sn-mkoutput"
  run cp -f sn-mkoutput "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#source /apps/sup#echo source /apps/sup#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#mkdir#echo mkdir#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#^supernova#echo supernova#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  # tenxrc
  run cp -f ../tenxrc "${TESTDIR}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/mnt/disks/data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]

}

@test "mkoutput" {

  run "${BATS_TMPDIR}/bats/sn-mkoutput"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/sn-mkoutput" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "source /apps/supernova/sourceme.bash" ]
  [ "${lines[1]}" == "Running mkoutput..." ]
  [ "${lines[2]}" == "Entering /mnt/disks/data/TEST/assembly/mkoutput" ]
  [ "${lines[3]}" == "mkdir -p /mnt/disks/data/TEST/assembly/mkoutput" ]
  [ "${lines[4]}" == "cd /mnt/disks/data/TEST/assembly/mkoutput" ]
  [ "${lines[5]}" == "Running mkoutput raw..." ]
  [ "${lines[6]}" == "supernova mkoutput --asmdir=/mnt/disks/data/TEST/assembly/outs/assembly --outprefix=TEST.raw --style=raw" ]
  [ "${lines[7]}" == "Running mkoutput megabubbles..." ]
  [ "${lines[8]}" == "supernova mkoutput --asmdir=/mnt/disks/data/TEST/assembly/outs/assembly --outprefix=TEST.megabubbles --style=megabubbles" ]
  [ "${lines[9]}" == "Running mkoutput pseudohap2..." ]
  [ "${lines[10]}" == "supernova mkoutput --asmdir=/mnt/disks/data/TEST/assembly/outs/assembly --outprefix=TEST.pseudohap2 --style=pseudohap2" ]
  [ "${lines[11]}" == "Running mkoutput...OK" ]
  [ "${lines[12]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
