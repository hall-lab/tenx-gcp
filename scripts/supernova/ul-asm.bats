#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  # test script
  export SCRIPT_PATH="${TESTDIR}/ul-asm"
  run cp -f ul-asm "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#rm#echo rm#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#gsutil#echo gsutil#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  # tenxrc
  run cp -f ../tenxrc "${TESTDIR}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/mnt/disks/data#' "${TESTDIR}/tenxrc"
  [ "${status}" -eq 0 ]
  
}

@test "dl-asm" {

  run "${BATS_TMPDIR}/bats/ul-asm"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/ul-asm" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Uploading TEST assembly to the object store..." ]
  [ "${lines[1]}" == "Entering: /mnt/disks/data/TEST/assembly" ]
  [ "${lines[2]}" == "cd /mnt/disks/data/TEST/assembly" ]
  [ "${lines[3]}" == "Removing logging directory ASSEMBLER_CS prior to upload" ]
  [ "${lines[4]}" == "rm -rf ASSEMBLER_CS" ]
  [ "${lines[5]}" == "Uploading to: gs://data/TEST/assembly" ]
  [ "${lines[6]}" == "gsutil -m rsync -r . gs://data/TEST/assembly" ]
  [ "${lines[7]}" == "Uploading assembly to the object store...OK" ]
  [ "${lines[8]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
