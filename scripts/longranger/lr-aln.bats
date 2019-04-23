#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  # test script
  export SCRIPT_NAME="lr-aln"
  export SCRIPT_PATH="${TESTDIR}/${SCRIPT_NAME}"
  run cp -f "${SCRIPT_NAME}" "${TESTDIR}"
  [ "${status}" -eq 0 ]
  chmod 755 "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#mkdir#echo mkdir#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#cd#echo cd#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#gsutil#echo gsutil#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#/apps/tenx-scripts#/tmp/bats#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#source /apps#echo source /apps#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#longranger#echo longranger#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]

  #tenxrc
  export TENXRC_PATH="${TESTDIR}/tenxrc"
  run cp -f ../tenxrc "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/mnt/disks/data#' "${TENXRC_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "lr-aln FAILS" {

  run "${BATS_TMPDIR}/bats/lr-aln"
  [ "${status}" -eq 1 ]

  run "${BATS_TMPDIR}/bats/lr-aln" TEST
  [ "${status}" -eq 1 ]

}

@test "lr-aln align" {

  run "${BATS_TMPDIR}/bats/lr-aln" TEST REF
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "mkdir -p /mnt/disks/data/TEST/alignment" ]
  [ "${lines[1]}" == "cd /mnt/disks/data/TEST/alignment" ]
  [ "${lines[2]}" == "source /apps/echo longranger/sourceme.bash" ]
  [ "${lines[3]}" == "longranger align --id=TEST --sample=TEST --fastqs=/mnt/disks/data/TEST/reads --reference=/mnt/disks/data/references/REF --jobmode=slurm --uiport=18080 --localmem=6 --localcores=1" ]
  [ "${lines[4]}" == "" ]

}

@test "lr-aln wgs" {

  run "${BATS_TMPDIR}/bats/lr-aln" TEST REF freebayes
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "mkdir -p /mnt/disks/data/TEST/alignment" ]
  [ "${lines[1]}" == "cd /mnt/disks/data/TEST/alignment" ]
  [ "${lines[2]}" == "source /apps/echo longranger/sourceme.bash" ]
  [ "${lines[3]}" == "longranger wgs --id=TEST --sample=TEST --fastqs=/mnt/disks/data/TEST/reads --reference=/mnt/disks/data/references/REF --jobmode=slurm --uiport=18080 --localmem=6 --localcores=1 --vcmode=freebayes" ]
  [ "${lines[4]}" == "" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
