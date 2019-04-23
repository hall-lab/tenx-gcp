#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  # test script
  export SCRIPT_NAME="run-lr"
  export SCRIPT_PATH="${TESTDIR}/${SCRIPT_NAME}"
  run cp -f "${SCRIPT_NAME}" "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#^ *"\$#echo "$#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  # tenxrc
  export TENXRC_PATH="${TESTDIR}/tenxrc"
  run cp -f ../tenxrc "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/mnt/disks/data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "run-lr FAILS" {

  run "${BATS_TMPDIR}/bats/run-lr"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/run-lr" TEST
  [ "${status}" -eq 1 ]

}

@test "run-lr align" {

  run "${BATS_TMPDIR}/bats/run-lr" TEST REF
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "/tmp/bats/dl-reads TEST" ]
  [ "${lines[1]}" == "/tmp/bats/dl-ref REF" ]
  [ "${lines[2]}" == "/tmp/bats/lr-aln TEST REF" ]
  [ "${lines[3]}" == "/tmp/bats/run-duration.py TEST" ]
  [ "${lines[4]}" == "/tmp/bats/ul-aln TEST" ]
  [ "${lines[5]}" == "" ]

}

@test "run-lr wgs" {

  run "${BATS_TMPDIR}/bats/run-lr" TEST REF VCMODE
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "/tmp/bats/dl-reads TEST" ]
  [ "${lines[1]}" == "/tmp/bats/dl-ref REF" ]
  [ "${lines[2]}" == "/tmp/bats/lr-aln TEST REF VCMODE" ]
  [ "${lines[3]}" == "/tmp/bats/run-duration.py TEST" ]
  [ "${lines[4]}" == "/tmp/bats/ul-aln TEST" ]
  [ "${lines[5]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}

