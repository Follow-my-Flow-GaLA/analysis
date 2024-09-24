import os, re, codecs, glob, difflib
from tqdm import tqdm
from collections import Counter
import sys
import hashlib

config_path = '/media/datak/inactive/analysis/phase2'
sys.path.append(config_path)
from config import CONFIG

record_reader_path = '/media/datak/inactive/analysis/phase3'
sys.path.append(record_reader_path)
from record_reader import get_sink_val_list

### Note: row_col is in the format of "row,col"

# global variable for summarizing phase2_dict
error_count = 0
def_val_dataset = {}
number_of_def_val = 0
number_of_key = 0

# Function to generate a Phase 2 dictionary (of a site) from log files and match with payload values
# output: phase_2_dict: {code_hash: {key_name: [defined_value, row_col, sink_type]}}
def get_phase2_dict(site, sink_val_list):   
    global error_count 
    phase_2_dict = {}
    fpath = os.path.join(CONFIG.PHASE2_LOG_PATH, site + "_log_file")
    
    try: 
        with codecs.open(fpath, mode='r', encoding='utf-8', errors='replace') as ff:
            lines = ff.readlines()
            for num, line in enumerate(lines, 0):
                if 'StartingLog...'in line:
                    # get the entire log str and clean it
                    end_ln = num
                    while (end_ln < len(lines) and "LogEn" not in lines[end_ln]): # LogEn is used for now to handle interruption
                        end_ln = end_ln + 1
                    if end_ln == len(lines):
                        continue
                    log_str = "".join(lines[num:end_ln+1]) if num < end_ln else line
                    
                    # clean log str
                    log_str = re.sub(r'\[[0-9:\/]+:.*?CONSOLE\((\d+)\)\](.|\n)*?\(\1\)\n', "", log_str)
                    log_str = re.sub(r'\[[0-9:\/]+:.*?\].*?\n', "", log_str)
                    
                    # check very_long_string
                    if (re.search(r'<Very long string\[\d+?\]>', log_str) != None):
                        continue
                    
                    # key and value
                    search_key_value_result = re.search(CONFIG.LOG_KEY_VALUE_REG, log_str)
                    if search_key_value_result == None:
                        print(site, " ERROR! Key_VALUE not found!", num, log_str)
                        error_count = error_count + 1
                        continue
                    key = search_key_value_result.group(1)
                    value = search_key_value_result.group(3)
                    # ln: row,col
                    search_ln_result = re.search(CONFIG.LOG_LN_REG, log_str)
                    if search_ln_result == None:
                        print(site, " ERROR! LN not found!", num, log_str)
                        error_count = error_count + 1
                        continue
                    ln = search_ln_result.group(1)
                    # codehash
                    search_codehash_result = re.search(CONFIG.LOG_CODEHASH_REG, log_str)
                    if search_codehash_result == None:
                        print(site, " ERROR! CODEHASH not found!", num, log_str)
                        error_count = error_count + 1
                        continue
                    code_hash = search_codehash_result.group(1)
                    
                    flow_found = False
                    
                    for sink_val in sink_val_list:
                        payload_val = sink_val["sink_payload"]
                        sink_type = sink_val["sink_type"]
                        # Approach 1: use mutual match
                        # if value in payload_val or payload_val in value: 
                        
                        # Approach 2: use partial match
                        matcher = difflib.SequenceMatcher(None, payload_val, value)
                        match = matcher.find_longest_match(0, len(payload_val), 0, len(value))
                        if match.size > 0:
                            # TODO: record c for future use 
                            # c = a[match.a:match.a + match.size]
                            # store in phase_2_dict
                            if code_hash in phase_2_dict:
                                if key in phase_2_dict[code_hash]:
                                    pass
                                else:
                                    phase_2_dict[code_hash][key] = [value, ln, sink_type]
                            else:
                                phase_2_dict[code_hash] = {key: [value, ln, sink_type]}
    except Exception as e: 
        print(site, " ERROR! Exception occurred!", e)
        error_count = error_count + 1
        
    return phase_2_dict             
   
# def_val_dataset: {code_hash+key_name: set of defined_values}
def store_in_def_val_dataset(phase_2_dict):
    global def_val_dataset, number_of_def_val, number_of_key
    for code_hash in phase_2_dict:
        for key in phase_2_dict[code_hash]:
            data = code_hash + key
            def_val = phase_2_dict[code_hash][key][0]
            
            # hash data
            hash_object = hashlib.sha256()
            hash_object.update(data.encode('utf-8'))
            hashed_string = hash_object.hexdigest()
            
            if hashed_string in def_val_dataset:
                if def_val in def_val_dataset[hashed_string]:
                    pass
                else:
                    def_val_dataset[hashed_string].add(def_val)
                    number_of_def_val = number_of_def_val + 1
            else:
                def_val_dataset[hashed_string] = {def_val}
                number_of_key = number_of_key + 1
                number_of_def_val = number_of_def_val + 1
            
             
if __name__ == "__main__":
    try:
        os.chdir(CONFIG.PHASE2_RECORD_PATH)
        
        for fpath in tqdm(glob.iglob("record_*")):
            z = fpath.split('_')
            site = '_'.join(z[1:len(z)-3])
            
            # Check if record file is empty
            if os.path.getsize(fpath) == 0:
                continue 
            
            # Construct log file path and check if it exists and is empty
            log_fpath = os.path.join(CONFIG.PHASE2_LOG_PATH, site + "_log_file")
            if not os.path.exists(log_fpath) or os.path.getsize(log_fpath) == 0:
                continue 
            
            # Read record file
            sink_val_list = get_sink_val_list(site, fpath)
            
            # Read log file 
            phase_2_dict = get_phase2_dict(site, sink_val_list)
            
            # Store in def_val_dataset
            store_in_def_val_dataset(phase_2_dict)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Printing current status...")
    finally:
        value_counts = [len(values) for values in def_val_dataset.values()]
        distribution = Counter(value_counts)
        sorted_distribution = sorted(distribution.items())
        print("---------------------------------\nThe distribution is:\n")
        print(sorted_distribution)
        # Print the summary output regardless of interruption
        print("---------------------------------")
        print("error_count is: ", error_count)
        print("number_of_def_val is: ", number_of_def_val)
        print("number_of_key is: ", number_of_key)
        print("---------------------------------")