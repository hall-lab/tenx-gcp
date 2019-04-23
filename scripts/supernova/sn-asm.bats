#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  # test script
  export SCRIPT_PATH="${TESTDIR}/sn-asm"
  run cp -f "sn-asm" "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

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
  export TENXRC_PATH="${TESTDIR}/tenxrc"
  run cp -f ../tenxrc "${TESTDIR}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/mnt/disks/data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "sn-asm" {

  run "${BATS_TMPDIR}/bats/sn-asm"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/sn-asm" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "source /apps/supernova/sourceme.bash" ]
  [ "${lines[1]}" == "mkdir -p /mnt/disks/data/TEST" ]
  [ "${lines[2]}" == "cd /mnt/disks/data/TEST" ]
  [ "${lines[3]}" == "supernova run --id=assembly --fastqs=/mnt/disks/data/TEST/reads --uiport=18080 --nodebugmem --localcores=50 --localmem=400" ]
  [ "${lines[4]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
