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

for ((i=1; i<=5; i++)); do
    # Phase 3
    echo "Running Phase 3 - Iteration $i"

    # Run inactive-phase3-auto-recursive.sh
    bash /media/datak/inactive/sanchecker/src/inactive-phase3-auto-recursive.sh 0 10000 2 12 0 2>&1 | tee -a ./inactive_phase3_crawling.log &

    # Wait for the process to finish
    wait_for_process "inactive-phase3-auto-recursive.sh"

    # Call process.py to process logs
    echo "python process.py ... "
    python process.py

    # Wait for js_info.log to be generated and is no longer being written into
    wait_for_file "js_info.log"

    # Call gen_json.py to generate a json file
    python3 gen_json.py

    echo "Phase 3 - Iteration $i completed"


    ##### Phase 4
    echo "Running Phase 4 - Iteration $i"

    # Run inactive-phase4-auto-recursive.sh
    bash /media/datak/inactive/sanchecker/src/inactive-phase4-auto-recursive.sh 0 10000 2 12 0 2>&1 | tee -a ./inactive_phase4_crawling.log &

    # Wait for the process to finish
    wait_for_process "inactive-phase4-auto-recursive.sh"

    # Rest of Phase 4...

    echo "Phase 4 - Iteration $i completed"
done
