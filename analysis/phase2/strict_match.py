import os, re, logging, argparse, codecs, json, glob, difflib
from tqdm import tqdm
from datetime import date
from pprint import pprint
from config import CONFIG
import time

# phase 1 dict: { site: {code_hash: {key_name: [line_num, js_name]}}}
# Function to generate a Phase 1 dictionary from a JSON file
def gen_phase1_dict():
    """
    This function reads a JSON file and returns a Phase 1 dictionary.

    Returns:
    - phase1_dict: A Phase 1 dictionary containing site, code hash, and key name information.
    """
    with open(CONFIG.PHASE1_JS_INFO_JSON_PATH) as json_file:
        phase1_dict = json.load(json_file)
    return phase1_dict

# Function to generate a dictionary of payload values from log records
# output: payload_val_dict = {site: (payload_value, sink_type)}
def gen_def_val_dict(limit = -1):
    """
    This function generates a dictionary of payload values from log records.

    Parameters:
    - limit (int): Limit the number of records to process (optional).

    Returns:
    - payload_val_dict: A dictionary containing payload values and their associated site and sink type.
    """
    payload_val_dict = {}
    
    start_pos = end_pos = -1
    site = content = var_val = sink_type = ""
    
    # keep track of the number of sites with payload_val
    counter = 0
    
    os.chdir(CONFIG.PHASE2_RECORD_PATH)
    for fpath in tqdm(glob.iglob("record_*")):
        # break when reached counter limit
        if (limit != -1 and counter >= limit):
            break
        # read record
        inactive_flag = False
        with codecs.open(fpath, mode='r') as ff:
            payload_val_set = set()
            lines = ff.readlines()
            z = fpath.split('_')
            site = '_'.join(z[1:len(z)-3])
            for num, line in enumerate(lines, 0):
                if 'type = inactive' in line: # get start_pos & end_pos
                    if 'start' in line: 
                        start_pos = int(re.search(CONFIG.RECORD_START_REG, line).group(1))
                    else:
                        start_pos = int(re.search(CONFIG.RECORD_START_REG, lines[num-2]).group(1))
                    search_end_pos_str = "".join(lines[num+1:num+6])
                    search_end_pos_result = re.search(CONFIG.RECORD_START_REG, search_end_pos_str)
                    if search_end_pos_result:
                        end_pos = int(search_end_pos_result.group(1))
                    else:
                        end_pos = -1 # the last var is inactive
                    inactive_flag = True
                    continue
                if inactive_flag and 'targetString = (' in line: # extract var_val from content
                    inactive_flag = False
                    content = re.search(CONFIG.RECORD_CONTENT_REG, lines[num+2]).group(1)
                    if "\\" in content:
                        content = eval(f'"{content}"')  
                    if (end_pos == -1):
                        var_val = content[start_pos::]
                    else:
                        var_val = content[start_pos:end_pos]
                    search_sink_type_result = re.search(CONFIG.RECORD_SINKTYPE_REG, "".join(lines[num+3:num+6]))
                    if (search_sink_type_result):
                        sink_type = search_sink_type_result.group(1)
                    else:
                        sink_type = "javascript"
                    if sink_type in ["prototypePollution", "xmlhttprequest", "logical"]:
                        continue
                    payload_val_set.add((var_val, sink_type))
                    continue
        #ff closed
        if len(payload_val_set):
            payload_val_dict[site] = payload_val_set
            counter = counter + 1   
    # all file finished
    return payload_val_dict

# Function to summarize the definition value dictionary
def summarize_def_val_dict(def_val_dict, mode=""):
    """
    This function summarizes the definition value dictionary and provides statistics.

    Parameters:
    - def_val_dict: The dictionary of definition values.
    - mode (str): The mode to run the summary in (optional, "gen_csv" is for generating CSV records).

    Returns:
    If mode is "gen_csv", the function prints records for CSV generation.
    Otherwise, it prints summary statistics.
    """
    print("------------------ below is Defined Value dict stats ----------------")
    if mode == "gen_csv":
        count = 0
        num_gt_1 = 0
        max_num = 0
        for site in def_val_dict:
            set_len = len(def_val_dict[site])
            if set_len > 1:
                num_gt_1 = num_gt_1 + 1
            if set_len > max_num:
                max_num = set_len
            count = count + 1
            record_str = "".join([str(count), ",", site.replace('_','.')])
            print(record_str)
        return
        
    count = 0
    num_gt_1 = 0
    max_num = 0
    for site in def_val_dict:
        set_len = len(def_val_dict[site])
        if set_len > 1:
            num_gt_1 = num_gt_1 + 1
        if set_len > max_num:
            max_num = set_len
        count = count + 1
    print("total number of sites: ", len(def_val_dict))
    print("number of sites with more than 1 def_val: ", num_gt_1)
    print("max num of def_val: ", max_num)
    print("------------------ above is Defined Value dict stats ----------------")

# global variable for summarizing phase2_dict
file_not_found_count = 0
error_count = 0
found_count = 0
flow_not_found_count = 0
web_not_found_count = 0
unterminated_log_count = 0
very_long_string_count = 0

not_found_flow_site = set()
not_found_web_site = set()

# phase 2 Data Structure: { site: {code_hash: {key_name: [def_value, line_num, sink_type]}}}
# Function to generate a Phase 2 dictionary from log records and match with definition values
def gen_phase2_dict(def_val_dict, limit=-1):
    """
    This function generates a Phase 2 dictionary from log records and matches it with definition values.

    Parameters:
    - def_val_dict: The dictionary of definition values.
    - limit (int): Limit the number of records to process (optional).

    Returns:
    - phase_2_dict: A Phase 2 dictionary containing site, code hash, key name, definition value, line number, and sink type information.
    """
    phase_2_dict = {}
    
    global file_not_found_count, error_count, found_count, flow_not_found_count, web_not_found_count, unterminated_log_count, very_long_string_count
    
    global not_found_flow_site, not_found_web_site
    
    counter = 0
    
    for site in def_val_dict:
        if (limit != -1 and counter >= limit):
            break
        fpath = os.path.join(CONFIG.PHASE2_LOG_PATH, site + "_log_file")
        key_value_list = []
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
                        # ln
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
                        
                        for value_sink_pair in def_val_dict[site]:
                            # Approach 1: use mutual match
                            # if value in value_sink_pair[0] or value_sink_pair[0] in value: 
                            
                            # Approach 2: use partial match
                            a = value_sink_pair[0]
                            b = value
                            matcher = difflib.SequenceMatcher(None, a, b)
                            match = matcher.find_longest_match(0, len(a), 0, len(b))
                            if match.size > 0:
                                c = a[match.a:match.a + match.size]
                                found_count = found_count + 1
                                # TODO: record c for future use 
                                key_value_list.append((key, a, value_sink_pair[1], ln, code_hash))
                            else:
                                flow_not_found_count = flow_not_found_count + 1
                                not_found_flow_site.add(site)
        except FileNotFoundError:
            file_not_found_count = file_not_found_count + 1
            continue
        except Exception as e: 
            error_count = error_count + 1
            continue
        if  len(key_value_list):
            phase_2_dict[site] = {}
            for tup in key_value_list:
                if tup[4] not in phase_2_dict[site]:
                    phase_2_dict[site][tup[4]] = {}
                phase_2_dict[site][tup[4]][tup[0]] = (tup[1],tup[3],tup[2])
        else :
            web_not_found_count = web_not_found_count + 1
            not_found_web_site.add(site)
        # ff closed
        counter = counter + 1
        
    return phase_2_dict

# Function to summarize the Phase 2 dictionary and provide statistics
def summarize_phase2_dict(phase_2_dict):
    """
    This function summarizes the Phase 2 dictionary and provides statistics.

    Parameters:
    - phase_2_dict: The Phase 2 dictionary to be summarized.
    """
    print("------------------ below is Phase 2 dict stats ----------------")
    print("phase2_dict length is: ", len(phase_2_dict))
    print("file_not_found_count is: ", file_not_found_count)
    print("error_count is: ", error_count)
    print("found_count is: ", found_count)
    print("flow_not_found_count is: ", flow_not_found_count)
    print("web_not_found_count is: ", web_not_found_count)
    print("unterminated_log_count is: ", unterminated_log_count)
    print("very_long_string_count is: ", very_long_string_count)
    
    print(not_found_web_site)
    print()
    print(not_found_flow_site)
    # with open("11_1_site_with_web_not_found", 'w') as file:
    #     for item in not_found_web_site:
    #         file.write(item + "\n")
    
    # with open("11_1_site_with_flow_not_found", 'w') as file:
    #     for item in not_found_flow_site:
    #         file.write(item + "\n")
            
    print("------------------ above is Phase 2 dict stats ----------------")

# Function to perform strict matching with dummy value
def strict_match_with_dummy_value (phase_1_dict, phase_2_dict):
    """
    This function performs strict matching between Phase 1 and Phase 2 dictionaries with a dummy value.

    Parameters:
    - phase_1_dict: The Phase 1 dictionary.
    - phase_2_dict: The Phase 2 dictionary.

    Returns:
    - match_result_dict: A dictionary containing matched data.
    """
    start_time = time.time()
    match_result_dict = {}
    for site, codehash_dict in tqdm(phase_1_dict.items()):
        for codehash, key_dict in codehash_dict.items():
            for key, value in key_dict.items():
                result_site = "www." + site.replace('_', ".")
                result_dict = {
                    "var_name": key, 
                    "payload": ["dummy"], 
                    "line_num": value[0], 
                    "file_name": value[1]
                }
                # check if value exist in phase_2
                if phase_2_dict.get(site) and phase_2_dict[site].get(codehash) and phase_2_dict[site][codehash].get(key):
                    value_2 = phase_2_dict[site][codehash][key]
                    result_dict["payload"][0] = value_2[0]
                # store data do match_result
                if match_result_dict.get(result_site):
                    each_site_list = match_result_dict[result_site]
                    for each_data_dict in each_site_list:
                        # If all other data match but payload, put the payloads into the same list
                        if each_data_dict["var_name"] == result_dict["var_name"] and \
                            each_data_dict["line_num"] == result_dict["line_num"] and \
                                each_data_dict["file_name"] == result_dict["file_name"]:
                                    payload_value = result_dict["payload"][0]
                                    if payload_value != "dummy":
                                        each_data_dict["payload"].append(payload_value)
                        else:
                            each_site_list.append(result_dict)
                else:
                    match_result_dict[result_site] = [result_dict]
    for site_list in match_result_dict.values():
        for each_info_dict in site_list:
            each_info_dict["payload"] = min(each_info_dict["payload"], key=len)
    print("time used: ", time.time() - start_time)
    return match_result_dict

# Function to perform strict matching between Phase 1 and Phase 2 dictionaries
def strict_match (phase_1_dict, phase_2_dict, mode="", save_path="/home/zfk/Documents/inject_pp_extension/value_data.js") :
    """
    This function performs strict matching between Phase 1 and Phase 2 dictionaries.

    Parameters:
    - phase_1_dict: The Phase 1 dictionary.
    - phase_2_dict: The Phase 2 dictionary.
    - mode (str): The mode to run the matching process (optional, "save" is for saving the result).
    - save_path (str): The file path to save the result (optional).

    Returns:
    - match_result_dict: A dictionary containing matched data.
    """
    # phase 1 dict: { site: {code_hash: {key_name: [line_num, js_name]}}}
    # phase 2 dict: { site: {code_hash: {key_name: [def_value, line_num, sink_type]}}}
    '''
    Output format: data_to_change={
        "mcafee.com": [{
            "var_name": "src", 
            "payload": "data:,debugger;//",
            "line_num": "9", 
            "file_name": "https://tags.tiqcdn.com/utag/mcafee/consumer-main/prod/utag.js"
        }], 
        "www.brother-usa.com": [{
            "var_name": "src", 
            "payload": "data:,debugger;//",
            "line_num": "9", 
            "file_name": "https://tags.tiqcdn.com/utag/brother/projectjanus/prod/utag.js"
        }]
    }
    '''
    match_result_dict = {}
    # print("start matching")
    for phase_1_site, phase_1_code_hash_dict in tqdm(phase_1_dict.items()):
        for phase_2_site, phase_2_code_hash_dict in phase_2_dict.items():
            for phase_2_code_hash, phase_2_varname_dict in phase_2_code_hash_dict.items():
                if phase_2_code_hash in phase_1_code_hash_dict.keys():
                    # print("code hash matched")
                    phase_1_varname_dict = phase_1_code_hash_dict[phase_2_code_hash]
                    for phase_2_varname in phase_2_varname_dict.keys():
                        if phase_2_varname in phase_1_varname_dict:
                            # print("varname matched")
                            result_site = "www." + phase_1_site.replace('_', ".")
                            result_dict = {
                                "var_name": phase_2_varname, 
                                "payload": [phase_2_varname_dict[phase_2_varname][0]], 
                                "line_num": phase_2_varname_dict[phase_2_varname][1], 
                                "file_name": phase_1_varname_dict[phase_2_varname][1]
                            }
                            if result_site in match_result_dict.keys():
                                each_site_list = match_result_dict[result_site]
                                data_dict_found = False
                                for each_data_dict in each_site_list:
                                    # If all other data match but payload, put the payloads into the same list
                                    if each_data_dict["var_name"] == result_dict["var_name"] and \
                                        each_data_dict["line_num"] == result_dict["line_num"] and \
                                            each_data_dict["file_name"] == result_dict["file_name"]:
                                                each_data_dict["payload"].append(phase_2_varname_dict[phase_2_varname][0])
                                                data_dict_found = True          
                                if not data_dict_found:    
                                    each_site_list.append(result_dict)
                            else:
                                match_result_dict[result_site] = [result_dict]
                            

    for site_list in match_result_dict.values():
        for each_info_dict in site_list:
            each_info_dict["payload"] = min(each_info_dict["payload"], key=len)
    if mode == "save":
        with open(save_path, "w") as fw:
            fw.write("data_to_change=")
            json.dump(match_result_dict, fw)
    return match_result_dict


if __name__ == "__main__":
    print("Generating Phase 1 dict ...")
    phase_1_dict = gen_phase1_dict()
    print("Phase 1 dict length is ", len(phase_1_dict))
    
    print("Generating Payload Value dict ...")
    def_val_dict = gen_def_val_dict()
    summarize_def_val_dict(def_val_dict)
    
    print("Generating Phase 2 dict ...")
    phase_2_dict = gen_phase2_dict(def_val_dict, limit=-1)
    summarize_phase2_dict(phase_2_dict)
   
    print("Generating result (strict match) dict ...")
    result_dict = strict_match (phase_1_dict, phase_2_dict, mode="")
    # result_dict = strict_match_with_dummy_value (phase_1_dict, phase_2_dict)
    print("result_dict length is: ", len(result_dict))
    
    with open("/home/zfk/Documents/inject_pp_extension/value_data_test.js", "w") as fw:
        fw.write("data_to_change=")
        json.dump(result_dict, fw)
