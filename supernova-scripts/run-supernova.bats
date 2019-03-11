#!/usr/bin/env bats

@test "no function given" {
  run bash run-supernova
  [ "${status}" -eq 1 ]
  [ "${lines[0]}" = "ERROR: No function given!" ]
  [ "${lines[1]}" = "USAGE:" ]
	
}

@test "no sample given" {
  run bash run-supernova pipeline
  [ "${status}" -eq 1 ]
  [ "${output}" = "ERROR: No sample given!" ]
	
}

@test "invalid function given" {
  run bash run-supernova blah TEST
  [ "${status}" -eq 1 ]
  [ "${lines[0]}" = "ERROR: Unknown function: blah" ]
  [ "${lines[1]}" = "USAGE:" ]

}

@test "help" {
  run bash run-supernova help
  [ "${status}" -eq 0 ]
  [ "${lines[0]}" = "USAGE:" ]
	
}

@test "copy-and-sed" {

  export TESTDIR="${BATS_TMPDIR}/bats"
  export SUPERNOVA_RUN_PATH="${TESTDIR}/run-supernova"

  run mkdir -p "${TESTDIR}"
  [ "${status}" -eq 0 ]

  run cp -f run-supernova "${TESTDIR}"
  [ "${status}" -eq 0 ]
  chmod 755 "${TESTDIR}/run-supernova"
  [ "${status}" -eq 0 ]

  run sed -i 's/gcloud /echo gcloud /' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's/gsutil /echo gsutil /' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's/supernova run/echo supernova run/' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#source #echo source #' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#supernova mkoutput #echo supernova mkoutput #' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#grep #echo grep #' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@REMOTE_DATA_URL\@#gs://data#' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  run sed -i 's#\@DATA_DIR\@#/tmp/bats#' "${SUPERNOVA_RUN_PATH}"
  [ "${status}" -eq 0 ]
  
}

@test "dl-fastqs" {
  export SUPERNOVA_DATA_PATH="${BATS_TMPDIR}/bats"

  run "${BATS_TMPDIR}/bats/run-supernova" dl-fastqs TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Fetching TEST fastqs from the object store..." ]
  [ "${lines[1]}" == "gsutil ls gs://data/reads/TEST/" ]
  [ "${lines[2]}" == "gsutil -m rsync -r gs://data/reads/TEST/ ." ]
  [ "${lines[3]}" == "Fetching fastqs from the object store...OK" ]
  [ -z "${lines[4]}" ]

  run ls "${BATS_TMPDIR}/bats/reads"
  [ "${status}" -eq 0 ]

}

@test "assemble" {
  export SUPERNOVA_DATA_PATH="${BATS_TMPDIR}/bats"

  run "${BATS_TMPDIR}/bats/run-supernova" assemble TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "source /apps/supernova/sourceme.bash" ]
  [ "${lines[1]}" == "Running supernova..." ]
  [ "${lines[2]}" == "supernova run --id=TEST --fastqs=${SUPERNOVA_DATA_PATH}/reads/TEST --uiport=18080 --nodebugmem --localcores=50 --localmem=400" ]
  [ "${lines[3]}" == "Running supernova...OK" ]
  [ -z "${lines[4]}" ]

  run ls "${SUPERNOVA_DATA_PATH}/assembly"
  [ "${status}" -eq 0 ]

}

@test "mkoutput" {
  export SUPERNOVA_DATA_PATH="${BATS_TMPDIR}/bats"
  mkdir -p "${SUPERNOVA_DATA_PATH}/assembly/TEST"

  run "${BATS_TMPDIR}/bats/run-supernova" mkoutput TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "source /apps/supernova/sourceme.bash" ]
  [ "${lines[1]}" == "Running mkoutput..." ]
  [ "${lines[2]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.raw --style=raw" ]
  [ "${lines[3]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.megabubbles --style=megabubbles" ]
  [ "${lines[4]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.pseudohap2 --style=pseudohap2" ]
  [ "${lines[5]}" == "Running mkoutput...OK" ]

  run ls "${SUPERNOVA_DATA_PATH}/assembly/TEST/mkoutput"
  [ "${status}" -eq 0 ]

}

@test "ul-assembly" {
  export SUPERNOVA_DATA_PATH="${BATS_TMPDIR}/bats"

  run mkdir -p "${SUPERNOVA_DATA_PATH}/assembly/TEST/ASSEMBLER_CS";
  [ "${status}" -eq 0 ]

  run "${BATS_TMPDIR}/bats/run-supernova" ul-assembly TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "Uploading assembly to object store..." ]
  [ "${lines[1]}" == "Checking if the assembly completed..." ]
  [ "${lines[2]}" == "grep -q Pipestance completed successfully _log" ]
  [ "${lines[3]}" == "Removing the ASSEMBLER_CS log sub directory..." ]
  [ "${lines[4]}" == "gsutil -m rsync -r TEST gs://data/assembly/TEST/" ]
  [ "${lines[5]}" == "Uploading assembly to object store...OK" ]
  [ -z "${lines[6]}" ]

  run ls "${SUPERNOVA_DATA_PATH}/assembly/TEST/ASSEMBLER_CS";
  [ "${status}" -ne 0 ]

}

@test "pipeline" {
  export SUPERNOVA_DATA_PATH="${BATS_TMPDIR}/bats"

  run "${BATS_TMPDIR}/bats/run-supernova" pipeline TEST
  [ "${status}" -eq 0 ]

  [ "${lines[0]}" == "source /apps/supernova/sourceme.bash" ]

  [ "${lines[1]}" == "Fetching TEST fastqs from the object store..." ]
  [ "${lines[2]}" == "gsutil ls gs://data/reads/TEST/" ]
  [ "${lines[3]}" == "gsutil -m rsync -r gs://data/reads/TEST/ ." ]
  [ "${lines[4]}" == "Fetching fastqs from the object store...OK" ]

  [ "${lines[5]}" == "Running supernova..." ]
  [ "${lines[6]}" == "supernova run --id=TEST --fastqs=${SUPERNOVA_DATA_PATH}/reads/TEST --uiport=18080 --nodebugmem --localcores=50 --localmem=400" ]
  [ "${lines[7]}" == "Running supernova...OK" ]

  [ "${lines[8]}" == "Running mkoutput..." ]
  [ "${lines[9]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.raw --style=raw" ]
  [ "${lines[10]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.megabubbles --style=megabubbles" ]
  [ "${lines[11]}" == "supernova mkoutput --asmdir=${SUPERNOVA_DATA_PATH}/assembly/TEST/outs/assembly --outprefix=TEST.pseudohap2 --style=pseudohap2" ]
  [ "${lines[12]}" == "Running mkoutput...OK" ]

  [ "${lines[13]}" == "Uploading assembly to object store..." ]
  [ "${lines[14]}" == "Checking if the assembly completed..." ]
  [ "${lines[15]}" == "grep -q Pipestance completed successfully _log" ]
  [ "${lines[16]}" == "Removing the ASSEMBLER_CS log sub directory..." ]
  [ "${lines[17]}" == "gsutil -m rsync -r TEST gs://data/assembly/TEST/" ]
  [ "${lines[18]}" == "Uploading assembly to object store...OK" ]
  [ -z "${lines[19]}" ]

  run ls "${SUPERNOVA_DATA_PATH}/reads"
  [ "${status}" -eq 0 ]
  run ls "${SUPERNOVA_DATA_PATH}/assembly"
  [ "${status}" -eq 0 ]
  run ls "${SUPERNOVA_DATA_PATH}/assembly/TEST/mkoutput"
  [ "${status}" -eq 0 ]
  run ls "${SUPERNOVA_DATA_PATH}/assembly/TEST/ASSEMBLER_CS"
  [ "${status}" -ne 0 ]

}

@test "cleanup" {
  run /bin/rm -rf "${BATS_TMPDIR}/bats"
  run /bin/ls "${BATS_TMPDIR}/bats"
  [ "${status}" -eq 2 ]

}

@test "addition using bc" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]

}

