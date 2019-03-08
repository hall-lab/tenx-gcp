#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_PATH="${TESTDIR}/ul-aln"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  run cp -f ul-aln "${TESTDIR}"
  [ "${status}" -eq 0 ]
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"

  run sed -i 's#mkdir#echo mkdir#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#rm#echo rm#' "${SCRIPT_PATH}"
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

@test "dl-aln" {

  run "${BATS_TMPDIR}/bats/ul-aln"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/ul-aln" TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Uploading TEST alignment to the object store..." ]
  [ "${lines[1]}" == "Entering: /mnt/disks/data/TEST/alignment" ]
  [ "${lines[2]}" == "cd /mnt/disks/data/TEST/alignment" ]
  [ "${lines[3]}" == "Removing logging directory ALIGNER_CS or PHASER_SVCALLER_CS prior to upload" ]
  [ "${lines[4]}" == "rm -rf ALIGNER_CS PHASER_SVCALLER_CS" ]
  [ "${lines[5]}" == "Uploading to: gs://data/TEST/alignment" ]
  [ "${lines[6]}" == "gsutil -m rsync -r . gs://data/TEST/alignment" ]
  [ "${lines[7]}" == "Uploading alignment to the object store...OK" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}

