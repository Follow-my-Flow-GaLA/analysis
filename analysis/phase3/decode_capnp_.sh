#!/bin/bash
# To run: sudo bash decode_capnp_.sh

PREFIX="record_"
ROOT="/media/datak/inactive/sanchecker/"
TARGET_STR="inactive_notemplate_phase3_iter2_partial_" 
TARGET_CRAWL=${TARGET_STR}"crawl"

TMP_WRITE_PATH=${TARGET_CRAWL}
mkdir -p ${ROOT}${PREFIX}${TMP_WRITE_PATH}

while IFS=, read -r log_name
do
    # ls -lh '/home/zfk/Documents/sanchecker/check_pp_pattern1_0to600kplus_crawl/'${log_name}
    /media/data1/zfk/Documents/capnproto-install/bin/capnp decode \
    /media/data1/zfk/Documents/sanchecker/src/v8/src/taint_tracking/protos/logrecord.capnp \
    TaintLogRecord < ${ROOT}${TARGET_CRAWL}/${log_name} > ${ROOT}${PREFIX}${TMP_WRITE_PATH}/${PREFIX}${log_name}
done < <(grep . 'list_to_capnp_'${TARGET_STR})  
