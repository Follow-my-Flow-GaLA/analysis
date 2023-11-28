# -*- coding: future_fstrings -*-
#!python3
from __future__ import print_function
import os, re, logging, argparse, codecs, json, glob, difflib, js2py
from tqdm import tqdm
from config import CONFIG
from value_data import data_to_change # CAUTION: check if this file is up-to-date

# Function to generate a dictionary of payload values from records
# output: payload_val_dict = {site: (payload_value, sink_type)}
def gen_payload_val_dict(limit = -1):
    """
    Generate a dictionary of payload values from records.

    Parameters:
    - limit (int): The maximum number of records to process.

    Returns:
    - payload_val_dict (dict): A dictionary containing payload values and their associated sink types.
    """
    payload_val_dict = {}
    
    start_pos = end_pos = -1
    site = content = var_val = sink_type = ""
    
    # keep track of the number of sites with payload_val
    counter = 0
    
    os.chdir(CONFIG.PHASE3_RECORD_PATH)
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

# Function to summarize the information in payload_val_dict
def summarize_payload_val_dict(payload_val_dict):
    """
    Summarize the information in the payload_val_dict.

    Parameters:
    - payload_val_dict (dict): A dictionary containing payload values and their associated sink types.
    """
    site_count = len(payload_val_dict)
    payload_count = 0
    for value in payload_val_dict.values():
        payload_count += len(value)
    print("Number of sites: ", site_count)
    print("Number of payloads: ", payload_count)

# Function to generate a dictionary of payloads and their information
# output: payload_dict = {site: [{var_name, line_num, payload, file_name, sink_type}]}
def gen_payload_dict(payload_val_dict, limit = -1):
    """
    Generate a dictionary of payloads and their information.

    Parameters:
    - payload_val_dict (dict): A dictionary containing payload values and their associated sink types.
    - limit (int): The maximum number of payloads to process.

    Returns:
    - payload_dict (dict): A dictionary containing payloads and their associated information.
    """
    payload_dict = {}
    # keep track of the number of sites
    counter = 0
    for key in payload_val_dict:
        # break when reached counter limit
        if (limit != -1 and counter >= limit):
            break
        counter += 1
        
        # find value of payload_val_dict in data_to_change
        site = 'www.' + '.'.join(key.split('_'))
        site_data = data_to_change[site]
        payload_dict[site] = []
        for pair in payload_val_dict[key]:
            # ignore extensions in varname and filename
            found = [data for data in site_data \
                     if pair[0] == data["payload"] \
                        and CONFIG.SHOULD_EXCLUDE not in data["var_name"] \
                        and CONFIG.SHOULD_EXCLUDE not in data["file_name"]]
            # add sinktype
            for data in found:
                data["sink_type"]= pair[1]
            payload_dict[site].extend(found)
            
    return payload_dict

# Function to summarize the information in payload_dict
def summarize_payload_dict(payload_dict):
    """
    Summarize the information in the payload_dict.

    Parameters:
    - payload_dict (dict): A dictionary containing payloads and their associated information.
    """
    site_count = len(payload_dict)
    print("Number of sites (should be the same as the num above): ", site_count)
    # count num of found, num of not found, num of unique in found
    total_count = 0
    for value in data_to_change.values():
        total_count += len(value)
    print("Total number of element in value_data: ", total_count)
    found_count = 0
    for value in payload_dict.values():
        found_count += len(value)
    print("Number of found: ", found_count)
    not_found_count = total_count - found_count
    print("Number of not found: ", not_found_count)
    unique_combinations = set()
    unique_combo_dict = {}
    for key, value in payload_dict.items():
        for item in value:
            combination = (item["var_name"], item["line_num"], item["file_name"])
            unique_combinations.add(combination)
            combo_str = ', '.join(combination)
            if combo_str not in unique_combo_dict:
                unique_combo_dict[combo_str] = [set(),set()]
            unique_combo_dict[combo_str][0].add(item["payload"])
            unique_combo_dict[combo_str][1].add(key)
    print("Number of unique element: ", len(unique_combinations) )
    for combo in unique_combinations:
        print(combo)
        print(unique_combo_dict[', '.join(combo)])

if __name__ == "__main__":
    print("-- Reading payload value from records -- ")
    payload_val_dict = gen_payload_val_dict()
    summarize_payload_val_dict(payload_val_dict)
    print("-- Find payload value in value_data  -- ")
    payload_dict = gen_payload_dict(payload_val_dict)
    summarize_payload_dict(payload_dict)
    