#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_NAME="run-supernova"
  export SCRIPT_PATH="${TESTDIR}/${SCRIPT_NAME}"
  export TENXRC_PATH="${TESTDIR}/tenxrc"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f "${SCRIPT_NAME}" "${TESTDIR}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#^ *"\$#echo "$#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_PATH\@#/mnt/disks/data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "run-supernova" {

  run "${BATS_TMPDIR}/bats/run-supernova"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/run-supernova" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "/tmp/bats/dl-reads TEST" ]
  [ "${lines[1]}" == "/tmp/bats/sn-asm TEST" ]
  [ "${lines[2]}" == "/tmp/bats/sn-mkoutput TEST" ]
  [ "${lines[3]}" == "/tmp/bats/run-duration.py TEST" ]
  [ "${lines[4]}" == "/tmp/bats/ul-asm TEST" ]
  [ "${lines[5]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
