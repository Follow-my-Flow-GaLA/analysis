#!/bin/bash

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
}

# Function to wait for a process to finish
wait_for_process() {
    while is_process_running "$1"; do
        sleep 1
    done
}

# Function to wait for a file to exist and be no longer written into
wait_for_file() {
    local file="$1"

    # Wait for the file to exist
    while [ ! -e "$file" ]; do
        sleep 1
    done

    local size1=0
    local size2=0

    # Wait for the file to be no longer written into
    while true; do
        size1=$(wc -c < "$file")
        sleep 60
        size2=$(wc -c < "$file")

        # If the file size remains constant, assume it is no longer being written into
        if [ "$size1" -eq "$size2" ]; then
            break
        fi
    done
}


# "Phase 3" includes: 
# 1. runs inactive-phase3-auto-recursive.sh and wait till it ends. But I don't know when it will stop running. Provide some code in .sh to help me determine if it stops
# 2. step 1 will generate lots of logs. Call process.py to process the logs
# 3. process.py generates js_info.log in a parallel way. But I don't know when it will stop running. Add some code in .py or in .sh to help me determine if it stops
# 4. After process.py stops, call gen_json.py to generate a json file for future use
# "Phase 4" includes: 
# 5. runs inactive-phase4-auto-recursive.sh and wait till it ends. It will take the json from step 4 as an input.  But I don't know when it will stop running. Provide some code in .sh to help me determine if it stops
# 6. After the sh stops, run filter_filename_from_ls.py and decode_capnp_.sh to decode some logs. Then call strict_match.py to generate a json file for future use

# Workflow for Phase 3:
# 1. detector-phase3-auto-recursive.sh
# 2. Check which flow can reach the sink and which cannot
# 3. Detect new undefined values and gen undef_list in db
# Workflow for Phase 4: 
# 4. oracle-phase4-auto-recursive.sh
# 5. Determine the defined values for undef
# 6. Match the defined with undef in Phase 3 and gen data_to_change in db

for ((i=1; i<=5; i++)); do
    ##### Phase 3 #####
    echo "Running Phase 3 - Iteration $i"

    # Run detector-phase3-auto-recursive.sh
    bash detector-phase3-auto-recursive.sh 0 1000000 2 16 0 2>&1 | grep -vE "Xlib:  extension \"RANDR\" missing on display \".*\"\.|Xlib:  extension \"XInputExtension\" missing on display \".*\"\.|ERROR:zygote_communication_linux.cc\(292\)\] Failed to" | tee -a ./detector_phase3_db_looping.log
    # Wait for the process to finish
    wait_for_process "detector-phase3-auto-recursive.sh"

    # Call process.py to process logs
    echo "python process.py ... "
    python process.py

    # Wait for js_info.log to be generated and is no longer being written into
    wait_for_file "js_info.log"

    # Call gen_json.py to generate a json file
    python3 gen_json.py

    echo "Phase 3 - Iteration $i completed"


    ##### Phase 4 #####
    echo "Running Phase 4 - Iteration $i"

    # Run oracle-phase4-auto-recursive.sh
    bash oracle-phase4-auto-recursive.sh 0 500000 2 16 0 2>&1 | grep -vE "Xlib:  extension \"RANDR\" missing on display \".*\"\.|Xlib:  extension \"XInputExtension\" missing on display \".*\"\.|ERROR:zygote_communication_linux.cc\(292\)\] Failed to" | tee -a ./oracle_phase4_1M_looping.log
    # Wait for the process to finish
    wait_for_process "oracle-phase4-auto-recursive.sh"

    # Rest of Phase 4...

    echo "Phase 4 - Iteration $i completed"
done
