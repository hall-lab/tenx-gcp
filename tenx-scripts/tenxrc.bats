#!/usr/bin/env bats

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SCRIPT_PATH="${TESTDIR}/tenxrc"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]
  run cp -f tenxrc "${TESTDIR}"
  [ "${status}" -eq 0 ]

  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_PATH\@#/mnt/disks/data#' "${SCRIPT_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "source tenxrc no sample/ref" {

  source "${BATS_TMPDIR}/bats/tenxrc"

  [ "${TENX_SAMPLE_PATH}" == "" ]
  [ "${TENX_ALN_PATH}" == "" ]
  [ "${TENX_ASM_PATH}" == "" ]
  [ "${TENX_RDS_PATH}" == "" ]
  [ "${TENX_REF_PATH}" == "" ]
  [ "${TENX_REFS_PATH}" == "/mnt/disks/data/references" ]

  [ "${TENX_SAMPLE_URL}" == "" ]
  [ "${TENX_ALN_URL}" == "" ]
  [ "${TENX_ASM_URL}" == "" ]
  [ "${TENX_RDS_URL}" == "" ]
  [ "${TENX_REF_URL}" == "" ]

}

@test "source tenxrc" {

  export TENX_SAMPLE=TEST
  export TENX_REFNAME=REF
  source "${BATS_TMPDIR}/bats/tenxrc"
  
  [ "${TENX_SAMPLE_PATH}" == "/mnt/disks/data/TEST" ]
  [ "${TENX_ALN_PATH}" == "/mnt/disks/data/TEST/alignment" ]
  [ "${TENX_ASM_PATH}" == "/mnt/disks/data/TEST/assembly" ]
  [ "${TENX_RDS_PATH}" == "/mnt/disks/data/TEST/reads" ]
  [ "${TENX_REF_PATH}" == "/mnt/disks/data/references/REF" ]
  [ "${TENX_REFS_PATH}" == "/mnt/disks/data/references" ]

  [ "${TENX_SAMPLE_URL}" == "gs://data/TEST" ]
  [ "${TENX_ALN_URL}" == "gs://data/TEST/alignment" ]
  [ "${TENX_ASM_URL}" == "gs://data/TEST/assembly" ]
  [ "${TENX_RDS_URL}" == "gs://data/TEST/reads" ]
  [ "${TENX_REF_URL}" == "gs://data/references/REF.tar.gz" ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}
