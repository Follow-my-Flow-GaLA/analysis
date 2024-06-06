#!python3
# from __future__ import print_function
import os, re, logging, argparse, codecs
from analysis.phase3.phase3_config import CONFIG
from tqdm import tqdm
import json
import time

# Function to generate JSON files containing code hashes and additional information
def gen_json(read_path, write_hash_path, write_more_info_path):
    """
    Generate JSON files containing code hashes and additional information.

    Parameters:
    - read_path (str): Path to the input log file.
    - write_hash_path (str): Path to the output JSON file containing code hashes.
    - write_more_info_path (str): Path to the output JSON file containing additional information.

    This function reads code hashes and related information from a log file, filters the data, and then writes it to two JSON files.
    """
    start_time = time.time()
    code_hashmap = {}
    more_info_hashmap = {}
    
    # read codehash
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, read_path), 'r', encoding='utf-8', errors='replace') as f0:
        line_count = 0
        while True:
            line_count += 1
            
            # print the occurance mod 1 billion
            if line_count % 10000000 == 0:
                print("Read codehash reaches ", line_count, " line after ", time.time() - start_time)

            # Get next line from file
            line = f0.readline()
            
            # End of file is reached
            if not line:
                break
            
            # Skip empty line:
            if (line.strip() == "" or line.strip().split()[-1] == "PM" or line.strip().split()[-1] == "AM"):
                continue
            
            # Save code_hash
            # line format: INFO: 10/10/2023 06:42:18 PM htcdev_com_log_file==>(eacfbb4719150d6e96cfb5baeadac007d72ae21ec1b99c09a6264c0fb9f98de1, runtime, /* anonymous */, chrome-extension://mmbeckpicbmkegkoapcgobnnmgbbalko/background.js, 6, 6)
            parts = line.split("==>")
            site = parts[0].split()[-1]
            code_hash = parts[1][1:-2].split(", ")[0]
            
            code_hashmap[code_hash] = {}
            
            if not (site in more_info_hashmap.keys()):
                more_info_hashmap[site] = {}
            more_info_hashmap[site][code_hash] = {}
            
        print("Length of js_info: ", line_count)
    
    # read js_info.log
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, read_path), 'r', encoding='utf-8', errors='replace') as f0:
        line_count = 0
        error_count = 0
        while True:
            line_count += 1
            
            # print the occurance mod 1 billion
            if line_count % 10000000 == 0:
                print("Reach ", line_count, " line after ", time.time() - start_time)

            # Get next line from file
            line = f0.readline()
            
            # End of file is reached
            if not line:
                break
            
            # Skip empty line:
            if (line.strip() == "" or line.strip().split()[-1] == "PM" or line.strip().split()[-1] == "AM"):
                continue
            
            try: 
                # line format: INFO: 10/10/2023 06:42:18 PM htcdev_com_log_file==>(eacfbb4719150d6e96cfb5baeadac007d72ae21ec1b99c09a6264c0fb9f98de1, runtime, /* anonymous */, chrome-extension://mmbeckpicbmkegkoapcgobnnmgbbalko/background.js, 6, 6)
                parts = line.split("==>")
                site = parts[0].split()[-1]
                [code_hash, key_name, func_name, js_name, line_num, col_num] = parts[1][1:-2].split(", ")
                
                # get rid of key_name and js_name exceeding the length of 100 (with error count)
                if len(key_name) > 100 or len(js_name) > 100:
                    error_count += 1
                    continue
                
                # get rid of "extension::"
                if CONFIG.SHOULD_EXCLUDE in key_name or CONFIG.SHOULD_EXCLUDE in js_name:
                    error_count += 1
                    continue
                
                code_hashmap[code_hash][key_name] = str(line_num) + "," + str(col_num)
                more_info_hashmap[site][code_hash][key_name] = [str(line_num) + "," + str(col_num), js_name]
            except KeyboardInterrupt:
                print("KeyboardInterrupt on line ", line_count)
            except:
                error_count += 1
        print("Length of js_info: ", line_count)
        print("Error count: ", error_count)
    
    print("Start cleaning ", time.time() - start_time)
    
    # clean empty value
    cleaned_code_hashmap = {}
    for key,value in code_hashmap.items():
        if len(value) == 0:
            continue
        cleaned_code_hashmap[key] = value
    code_hashmap = cleaned_code_hashmap
    for site,site_dict in more_info_hashmap.items():
        cleaned_site_dict = {}
        for key,value in site_dict.items():
            if len(value) == 0:
                continue
            cleaned_site_dict[key] = value
        more_info_hashmap[site] = cleaned_site_dict
    cleaned_more_info_hashmap = {}
    for key,value in more_info_hashmap.items():
        if len(value) == 0:
            continue
        cleaned_more_info_hashmap[key] = value
    more_info_hashmap = cleaned_more_info_hashmap
        
    print("Start writing ", time.time() - start_time)
    
    # write result
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, write_hash_path), 'w') as fw:
        json.dump(code_hashmap, fw)
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, write_more_info_path), 'w') as fw:
        json.dump(more_info_hashmap, fw)

    print("Finish writing ", time.time() - start_time)
        
if __name__ == "__main__":
    gen_json("logs/js_info.log", "output/undef_prop_dataset.json", "output/phase3_info.json")
