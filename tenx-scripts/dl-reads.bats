#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_PATH="${TESTDIR}/dl-reads"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  run cp -f dl-reads "${TESTDIR}"
  [ "${status}" -eq 0 ]
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#mkdir#echo mkdir#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#gsutil#echo gsutil#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_PATH\@#/mnt/disks/data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  
}

@test "dl-reads" {

  run "${BATS_TMPDIR}/bats/dl-reads"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/dl-reads" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Fetching TEST fastqs from the object store..." ]
  [ "${lines[1]}" == "mkdir -p /mnt/disks/data/TEST/reads" ]
  [ "${lines[2]}" == "cd /mnt/disks/data/TEST/reads" ]
  [ "${lines[3]}" == "Checking for sample reads remote URL..." ]
  [ "${lines[4]}" == "gsutil ls gs://data/TEST/reads" ]
  [ "${lines[5]}" == "gsutil -m rsync -r gs://data/TEST/reads/ ." ]
  [ "${lines[6]}" == "Fetching fastqs from the object store...OK" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}

