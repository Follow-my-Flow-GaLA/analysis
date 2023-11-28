#!/bin/bash
# sudo bash ./trim_useless_log.sh rm_files

SCAN_ROOT_PATH="/media/datak/inactive/sanchecker/src/inactive_0to100k_phase1_logs"

# Excluding logs with `extensions::` in its key or func name
PARSE_LOG_REG="(?:RTO|RAP0|RAP1|JRGDP|OGPWII|GPWFAC) KeyIs .*?<.*?: .*?extensions::.*?>\n=== JS Info ===\n(?:Skip Non-JS;\n)*.*? \[.*?extensions::.*?:\d+:\d+\]\n--------- s o u r c e   c o d e ---------\n.*?\n-----------------------------------------\n (?:RTOEnd|RAP0End|RAP1End|JRGDPEnd|OGPWIIEnd|GPWFACEnd)"

mode=$1

if (($mode == "rm_lines"))
then
    idx=1
    for file in "$SCAN_ROOT_PATH"/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Use sed to remove lines matching the regular expression
        # Create a backup of the original file with a .bak extension
        sed -E -i.bak "/$PARSE_LOG_REG/d" "$file" # TODO: error here
        
        # Remove the backup file
        rm "$file.bak"
        
        echo "Processed: $idx $file"
        ((idx++))
    fi
    done

elif (($mode == "rm_files"))
then
    jq -r 'keys[] | gsub("\\.", "_")' output/phase1_info.json > output/file_phase1_to_keep_list.txt
    comm -3 <(find $SCAN_ROOT_PATH -type f -exec basename {} \; | sort) <(sort output/file_phase1_to_keep_list.txt) | xargs -I {} rm $SCAN_ROOT_PATH/{}
fi