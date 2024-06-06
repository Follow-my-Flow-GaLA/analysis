#!/bin/bash

PREFIX="record_"
DB_ROOT="/media/datak/inactive/sanchecker/"
ROOT="/media/datak/inactive/sanchecker/"
TARGET_STR="validate_nonxss_phase3_db_" #"oracle_1M_phase2_db_" #"detector_1M_phase3_db_"
TARGET_CRAWL="${TARGET_STR}crawl"
TMP_WRITE_PATH="${TARGET_CRAWL}"
MAX_JOBS=30  # Maximum number of parallel jobs

mkdir -p "${ROOT}${PREFIX}${TMP_WRITE_PATH}"

process_file() {
    local file=$1
    /media/data1/zfk/Documents/capnproto-install/bin/capnp decode \
    /media/data1/zfk/Documents/sanchecker/src/v8/src/taint_tracking/protos/logrecord.capnp \
    TaintLogRecord < "${DB_ROOT}${TARGET_CRAWL}/${file}" > "${ROOT}${PREFIX}${TMP_WRITE_PATH}/${PREFIX}${file}"
}

export -f process_file
export DB_ROOT TARGET_CRAWL ROOT PREFIX TMP_WRITE_PATH

# Main loop
idx=0
while IFS= read -r file; do
    echo "$idx processing $file"
    idx=$((idx + 1))    
    process_file "$file" &

    # Limit number of background jobs
    if [[ $(jobs -r | wc -l) -ge $MAX_JOBS ]]; then
        wait -n  # Wait for at least one job to finish
    fi
done < <(grep . 'list_to_capnp_'${TARGET_STR})

#wait  # Wait for all background jobs to finish

