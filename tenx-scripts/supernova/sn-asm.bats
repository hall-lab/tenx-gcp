#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_NAME="sn-asm"
  export SCRIPT_PATH="${TESTDIR}/${SCRIPT_NAME}"
  export TENXRC_PATH="${TESTDIR}/tenxrc"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  run cp -f "${SCRIPT_NAME}" "${TESTDIR}"
  [ "${status}" -eq 0 ]
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

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_PATH\@#/mnt/disks/data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "sn-asm FAILS" {

  run "${BATS_TMPDIR}/bats/sn-asm"
  [ "${status}" -eq 1 ]

}

@test "sn-asm" {

  run "${BATS_TMPDIR}/bats/sn-asm" TEST REF
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
