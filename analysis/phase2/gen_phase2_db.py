import os, re, codecs, glob, difflib
from tqdm import tqdm
from config import CONFIG
from pymongo import MongoClient
import sys

record_reader_path = '/media/datak/inactive/analysis/phase3'
sys.path.append(record_reader_path)
from record_reader import get_sink_val_list

### Note: row_col is in the format of "row,col"

client = MongoClient("mongodb://localhost:27017/")
db = client["phase2"]
# for sink_flow: those flows that matched to sinks
def_val_dataset_collection = db["def_val_dataset"]# corresponding to sink_val_dataset
phase_info_collection = db["phase_info"] # corresponding to sink_flow
# for failed_flow: those flows that failed to match to sinks
failed_val_dataset_collection = db["failed_val_dataset"]
failed_flow_collection = db["failed_flow"]

# global variable for summarizing phase2_dict
file_not_found_count = 0
error_count = 0
unterminated_log_count = 0
very_long_string_count = 0

db_post_error_count = 0

# Function to generate a set of payload values from record
# output: payload_val_set = [(payload_value, sink_type)]
def get_payload_val_set(site, fpath):
    payload_val_set = set()
    inactive_flag = False
    start_pos = end_pos = -1
    var_val = sink_type = ""
    
    with codecs.open(fpath, mode='r') as ff:
        lines = ff.readlines()
        pos_list = []
        for num, line in enumerate(lines, 0):
            if 'type = inactive' in line: # get start_pos & end_pos
                if 'start' in line: 
                    start_pos = int(re.search(CONFIG.RECORD_START_REG, line).group(1))
                else:
                    start_pos = int(re.search(CONFIG.RECORD_START_REG, lines[num-2]).group(1))
                search_end_pos_str = "".join(lines[num+1:num+6])
                # next start_pos is the end_pos for last entree
                search_end_pos_result = re.search(CONFIG.RECORD_START_REG, search_end_pos_str)
                if search_end_pos_result:
                    end_pos = int(search_end_pos_result.group(1))
                else:
                    end_pos = 4294967295 # the last var is inactive
                inactive_flag = True
                pos_list.append((start_pos, end_pos))
                continue
            
            if inactive_flag and 'targetString = (' in line: # extract var_val from content
                inactive_flag = False
                content_list = []
                current_pos_list = pos_list
                pos_list = []
                # Find sink_type line first
                for sink_line_num, temp_line in enumerate(lines[ num+2 : ]):
                    search_sink_type_result = re.search(CONFIG.RECORD_SINKTYPE_REG, temp_line)
                    if (search_sink_type_result):
                        sink_type = search_sink_type_result.group(1)
                        break
                else:
                    # No sink_type provided. Abort
                    print(f"Warning: Website {site} in {fpath} finds no sink_type from line {num}")
                    continue
                
                if sink_type in ["prototypePollution", "xmlhttprequest", "logical"]:
                    continue
                
                # Search for contents within that block: lines[ num+2 : sink_line_num ]
                sink_line_num += num + 2
                content_matches = re.findall(CONFIG.RECORD_CONTENT_REG, ''.join(lines[ num+2 : sink_line_num ]))
                if not content_matches:
                    print(f"Warning: Website {site} in {fpath} finds no contents in line {num+2} to {sink_line_num}")
                    continue
                
                for each_content, is_one_byte in content_matches:
                    if is_one_byte == 'false':
                        # Two-byte string. needs encoding
                        each_content = each_content.replace('\\x00','')
                        if "\\x" in each_content:
                            try:
                                bytes(each_content, encoding='latin-1').decode('utf-16le')
                            except (UnicodeDecodeError, ValueError) as e:
                                print(f"Error: Website {site} in {fpath} cannot handle two-byte {each_content} in line {num+2}")
                    if "\\" in each_content:
                        each_content = eval(f'"{each_content}"') 
                    content_list.append(each_content) 
                content_list = ''.join(content_list)
                
                for start_pos, end_pos in current_pos_list:
                    try:
                        var_val = content_list[int(start_pos): int(end_pos)]
                        payload_val_set.add((var_val, sink_type))  
                    except ValueError:
                        print(f"ValueError: {start_pos} or {end_pos} failed to str->int! Website {site} in {fpath} in line {num+2}. ")
                        continue                  
                current_pos_list = []
                continue
    return payload_val_set

# Function to generate a Phase 2 dictionary (of a site) from log files and match with payload values
# output: phase_2_dict: {code_hash: {key_name: [defined_value, row_col, sink_type]}}
def get_phase2_dict(site, sink_val_list, flow_found_dict):
    global file_not_found_count, error_count, unterminated_log_count, very_long_string_count
    
    phase_2_dict = {}
    failed_flow_dict = {}
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
                        unterminated_log_count = unterminated_log_count + 1
                        continue
                    log_str = "".join(lines[num:end_ln+1]) if num < end_ln else line
                    
                    # clean log str
                    log_str = re.sub(r'\[[0-9:\/]+:.*?CONSOLE\((\d+)\)\](.|\n)*?\(\1\)\n', "", log_str)
                    log_str = re.sub(r'\[[0-9:\/]+:.*?\].*?\n', "", log_str)
                    
                    # check very_long_string
                    if (re.search(r'<Very long string\[\d+?\]>', log_str) != None):
                        very_long_string_count = very_long_string_count + 1
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
                            flow_found = True
                            flow_found_dict[payload_val] = True
                        else: 
                            # store in failed_flow_dict
                            if code_hash in failed_flow_dict:
                                if key in failed_flow_dict[code_hash]:
                                    pass
                                else:
                                    failed_flow_dict[code_hash][key] = [value, ln, sink_type]
                            else:
                                failed_flow_dict[code_hash] = {key: [value, ln, sink_type]}
                            
                    if flow_found:
                        found_count = found_count + 1
                    else:
                        # not_found_flow_site.add(site)
                        flow_not_found_count = flow_not_found_count + 1
                        # not_found_flow_value.add((value,payload_val))               
    except FileNotFoundError:
        file_not_found_count = file_not_found_count + 1
    except Exception as e: 
        error_count = error_count + 1
        
    return phase_2_dict, failed_flow_dict

# Function to send post request to store phase_2_dict in db
def send_post_request(site, phase_2_dict, failed_flow_dict):
    global db_post_error_count
    
    # send the entire phase_2_dict to phase_info 
    try:
        phase_info_collection.update_one(
            {"_id": site},
            {"$set": {
                "code_hash_dict": phase_2_dict
            }}
        , upsert=True)
        failed_flow_collection.update_one(
            {"_id": site},
            {"$set": {
                "code_hash_dict": failed_flow_dict
            }}
        , upsert=True)
    except Exception as e:
        print(f"Exception occurred: {e}")
        db_post_error_count = db_post_error_count + 1
        
    # send each code_hash to def_val_dataset
    for code_hash, key_value_list in phase_2_dict.items():
        for key, value_list in key_value_list.items():
            value = value_list[0]
            sink_type = value_list[2]
            # TODO: make this atomic 
            try: 
                code_hash_obj = def_val_dataset_collection.find_one({"_id": code_hash})
                if code_hash_obj:
                    # check if key exists
                    if key in code_hash_obj["key_value_dict"]:
                        if (len(code_hash_obj["key_value_dict"][key]["value"]) > len(value)) and len(value) > 3:
                            code_hash_obj["key_value_dict"][key] = {
                                "value": value,
                                "sink_type": sink_type,
                                "site": site
                            }
                            def_val_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}})
                        else:
                            pass
                    else:
                        code_hash_obj["key_value_dict"][key] = {
                            "value": value,
                            "sink_type": sink_type,
                            "site": site
                        }
                        def_val_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}})
                else:
                    def_val_dataset_collection.update_one(
                        {"_id": code_hash},
                        {"$set": {
                            "key_value_dict": {
                                key: {
                                    "value": value,
                                    "sink_type": sink_type,
                                    "site": site
                                }
                            }
                        }}
                    , upsert=True)
            except Exception as e:
                print(f"Exception occurred: {e}")
                db_post_error_count = db_post_error_count + 1
    
    # send each code_hash to failed_val_dataset
    for code_hash, key_value_list in failed_flow_dict.items():
        for key, value_list in key_value_list.items():
            value = value_list[0]
            sink_type = value_list[2]
            # TODO: make this atomic
            try:
                code_hash_obj = failed_val_dataset_collection.find_one({"_id": code_hash})
                if code_hash_obj:
                    # check if key exists
                    if key in code_hash_obj["key_value_dict"]:
                        if (len(code_hash_obj["key_value_dict"][key]["value"]) > len(value)):
                            code_hash_obj["key_value_dict"][key] = {
                                "value": value,
                                "sink_type": sink_type,
                                "site": site
                            }
                            failed_val_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}})
                        else:
                            pass
                    else:
                        code_hash_obj["key_value_dict"][key] = {
                            "value": value,
                            "sink_type": sink_type,
                            "site": site
                        }
                        failed_val_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}})
                else:
                    failed_val_dataset_collection.update_one(
                        {"_id": code_hash},
                        {"$set": {
                            "key_value_dict": {
                                key: {
                                    "value": value,
                                    "sink_type": sink_type,
                                    "site": site
                                }
                            }
                        }}
                    , upsert=True)
            except Exception as e:
                print(f"Exception occurred: {e}")
                db_post_error_count = db_post_error_count + 1
                
                
if __name__ == "__main__":
    os.chdir(CONFIG.PHASE2_RECORD_PATH)
    for fpath in tqdm(glob.iglob( "record_*" )):
        z = fpath.split('_')
        site = '_'.join(z[1:len(z)-3])
        # read record file
        sink_val_list = get_sink_val_list(site, fpath)
        # set up payload_dict to check if flow is found 
        flow_found_dict = {}
        for sink_val in sink_val_list:
            flow_found_dict[sink_val["sink_payload"]] = False
        # read log file 
        phase_2_dict, failed_flow_dict = get_phase2_dict(site, sink_val_list, flow_found_dict)
        # count flow found and not found 
        flow_found_count = 0
        flow_not_found_count = 0
        for sink_val in sink_val_list:
            if flow_found_dict[sink_val["sink_payload"]]:
                flow_found_count = flow_found_count + 1
            else:
                flow_not_found_count = flow_not_found_count + 1
        if (flow_not_found_count > 0):
            print("", site, " flow_found_count is: ", flow_found_count, " flow_not_found_count is: ", flow_not_found_count)
        # store in db
        send_post_request(site, phase_2_dict, failed_flow_dict)
    print("---------------------------------")
    print("file_not_found_count is: ", file_not_found_count)
    print("error_count is: ", error_count)
    print("unterminated_log_count is: ", unterminated_log_count)
    print("very_long_string_count is: ", very_long_string_count)
    print("db_post_error_count is: ", db_post_error_count)
    print("---------------------------------")