#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_PATH="${TESTDIR}/dl-ref"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  run cp -f dl-ref "${TESTDIR}"
  [ "${status}" -eq 0 ]
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#gsutil#echo gsutil#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#rm#echo rm#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#tar #echo tar #' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_PATH\@#/mnt/disks/data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  
}

@test "dl-ref" {

  run "${BATS_TMPDIR}/bats/dl-ref"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/dl-ref" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Fetching TEST reference from the object store..." ]
  [ "${lines[1]}" == "Checking reference remote URL: gs://data/references/TEST.tar.gz" ]
  [ "${lines[2]}" == "gsutil ls gs://data/references/TEST.tar.gz" ]
  [ "${lines[3]}" == "Entering /mnt/disks/data/references" ]
  [ "${lines[4]}" == "cd /mnt/disks/data/references" ]
  [ "${lines[5]}" == "gsutil -m rsync -r gs://data/references/TEST.tar.gz ." ]
  [ "${lines[6]}" == "Untarring TEST.tar.gz ..." ]
  [ "${lines[7]}" == "tar -xvvfz TEST.tar.gz" ]
  [ "${lines[8]}" == "rm -f TEST.tar.gz" ]
  [ "${lines[9]}" == "Fetching reference from the object store...OK" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}

