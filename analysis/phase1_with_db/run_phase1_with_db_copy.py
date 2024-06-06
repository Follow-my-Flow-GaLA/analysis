'''
Database schema: (local mongodb server)
1. phase_info
    `_id` : google.com
    `code_hash_dict`:  Object
        6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c: 
            google: Array(2)
                `0` : Array(2)
                    `0` : 2, 25
                    `1` : https://www.google.com/?K1.K2=V
                    `2` :  /* anonymous */
                `1` : Array(2)
                    `0` : 6, 35
                    `1` : https://www.google.com/?K1.K2=V
                    `2` :  /* anonymous */

2. undef_prop_dataset
    `_id` : 6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c
    `key_dict` : Object
        google: Array(2)
            `0` : 2, 25
            `1` : 6, 35

3. code_hash_dataset
    `_id` : 6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c
    `func` : function (){var a;(null==(a=window.google)?0:a.stvsc)?google.kEI=_g.kEI:window.google=_g;}
'''

'''
in-memory data structure: (site-level data)
1. phase_info
{
    6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c: 
    {
        google: [["2, 25", "6, 35"], "https://www.google.com/?K1.K2=V", "/* anonymous */"]
    }
}

2. undef_prop_dataset
{
    6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c:
    {
        google: ["2, 25", "6, 35"]
    }
}

3. code_hash_dataset
{
    6bbd8da210db29b158afeb5f686d053e113fc3efbdfb60823d37a1c6c95bbd5c: function (){var a;(null==(a=window.google)?0:a.stvsc)?google.kEI=_g.kEI:window.google=_g;}
}
'''

import threading, argparse, codecs
from pymongo import MongoClient
import pymongo

SITE = "mountvernon.org"
LOG_PATH = '/media/datak/inactive/sanchecker/src/detector_1M_phase1_db_logs/' + SITE.replace(".", "_", 1) + '_log_file'

client = MongoClient("mongodb://localhost:27017/")
db = client["phase1"]
undef_prop_dataset_collection = db["undef_prop_dataset"]
phase_info_collection = db["phase_info"]
code_hash_dataset_collection = db["code_hash_dataset"]

# in-memory data structure to store phase_info and undef_prop_dataset
phase_info = {}
undef_prop_dataset = {}
code_hash_dataset = {}

PRINT_WARNING = False
PRINT_ERROR = True

# the following three functions are used to merge in-memory data to collections
def add_undef_prop_dataset_to_db():
    for code_hash, in_memory_key_dict in undef_prop_dataset.items():
        # setOnInsert for code_hash that doesn't exist
        try: 
            undef_prop_dataset_collection.update_one(
                {"_id": code_hash},
                {"$setOnInsert": {
                    "key_dict": in_memory_key_dict
                }},
                upsert=True
            )
        except pymongo.errors.WriteError as e:
            if PRINT_ERROR: 
                print(f"{SITE}: pymongo.errors.WriteError (document exceeding 16777216) in add_undef_prop_dataset_to_db (line:76): {code_hash}: {e}")
            
        # addToSet for code_hash that exists
        for key, row_col_list in in_memory_key_dict.items():
            if key: # check if key is not empty
                try: 
                    undef_prop_dataset_collection.update_one(
                        {"_id": code_hash},
                        {"$addToSet": {
                            f"key_dict.{key}": {"$each": row_col_list}
                        }}
                    )
                except pymongo.errors.WriteError as e:
                    if PRINT_ERROR: 
                        print(f"{SITE}: add_undef_prop_dataset_to_db pymongo.errors.WriteError: {code_hash}")
            else:
                if PRINT_ERROR: 
                    print(f"{SITE}: Error: Key is empty for code hash {code_hash}.")
        

def add_phase_info_to_db():
    try: 
        phase_info_collection.update_one(
            {"_id": SITE.replace(".", "_")},
            {"$set": {
                "code_hash_dict": phase_info
            }}
        , upsert=True)
    except pymongo.errors.WriteError as e:
        if PRINT_ERROR: 
            print(f"{SITE}: add_phase_info_to_db pymongo.errors.WriteError: {e}")
    except Exception as e:
        if PRINT_ERROR: 
            print(f"{SITE}: add_phase_info_to_db: {e}")

def add_code_hash_dataset_to_db():
    for code_hash in code_hash_dataset.keys():
        code_hash_obj = code_hash_dataset_collection.find_one({"_id": code_hash})
        if not code_hash_obj:
            code_hash_dataset_collection.update_one(
                {"_id": code_hash},
                {"$set": {
                    "func": code_hash_dataset[code_hash]
                }}
            , upsert=True)

# the following three functions are used to add log to the in-memory data structures
def add_log_to_undef_prop_dataset(data):
    code_hash = data["code_hash"]
    key = data["key"]
    row_col_str = data["row"] + ", " + data["col"]
    if code_hash in undef_prop_dataset:
        if key in undef_prop_dataset[code_hash]:
            if row_col_str in undef_prop_dataset[code_hash][key]:
                if PRINT_WARNING: 
                    print(f"Warning: In-memory undef_prop_dataset (Key is {key}, row and col is {row_col_str}, Code hash is {code_hash}).")
            else:
                undef_prop_dataset[code_hash][key].append(row_col_str)
        else:
            undef_prop_dataset[code_hash][key] = [row_col_str]
    else:
        undef_prop_dataset[code_hash] = {
            key: [row_col_str]
        }

def add_log_to_phase_info(data):
    code_hash = data["code_hash"]
    key = data["key"]
    row_col_str = data["row"] + ", " + data["col"]
    if code_hash in phase_info:
        if key in phase_info[code_hash]:
            if row_col_str in phase_info[code_hash][key][0]:
                if PRINT_WARNING: print(f"Warning: In-memory phase_info (Key is {key}, row and col is {row_col_str}, Code hash is {code_hash}).")
            else:
                phase_info[code_hash][key][0].append(row_col_str)
        else:
            phase_info[code_hash][key] = [[row_col_str], data["js"], data["func_name"]]
    else:
        phase_info[code_hash] = {
            key: [[row_col_str], data["js"], data["func_name"]]
        }

def add_log_to_code_hash_dataset(data):
    code_hash = data["code_hash"]
    if code_hash in code_hash_dataset:
        if PRINT_WARNING: print(f"Warning: In-memory code_hash_dataset (Code hash is {code_hash}).")
    else:
        code_hash_dataset[code_hash] = data["func"]

# validate data blocks from log file and add them to the in-memory data structures
def log_phase1_db(data):
    # check fields
    required_fields = ['code_hash', 'phase', 'start_key', 'site', 'key', 'func_name', 'js', 'row', 'col', 'func']
    for field in required_fields:
        if field not in data:
            print(f"{SITE}: Field {field} is missing in the log data: {data}")
            return
        
    # check phase
    if data["phase"] != "1":
        print(f"{SITE}: Phase is not 1: {data}")
        return
    
    # check start_key
    valid_start_keys = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC", "JRGE", "JRG"]
    if data["start_key"] not in valid_start_keys:
        print(f"{SITE}: Invalid start key: {data}")
        return
    
    # sanitize site, change dots to underscores
    data["site"] = data["site"].replace(".", "_")
    # sanitize all other fields, change dots to \\2E, change dollar signs to \\24
    data["key"] = data["key"].replace(".", "\\2E").replace("$", "\\24")
    data["func_name"] = data["func_name"].replace(".", "\\2E").replace("$", "\\24")
    data["js"] = data["js"].replace(".", "\\2E").replace("$", "\\24")
    data["func"] = data["func"].replace(".", "\\2E").replace("$", "\\24")

    # remove extremely long data
    if len(data["key"]) > 1000 or len(data["func"]) > 100000:
        print(f"{SITE}: Long data: {data}")
        return
        
    # add log to the in-memory data structures
    add_log_to_undef_prop_dataset(data)
    add_log_to_phase_info(data)
    add_log_to_code_hash_dataset(data)

# read log and extract data blocks 
def process_log():
    with codecs.open(LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
        buffer = "" 
        end_index = -3
        incomplete_data_block = True
        using_buffer = False
        data = {}
        for line in f:
            if line.startswith('ReqJson{"code_hash":"'):
                data = {}
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                incomplete_data_block = False
                data["code_hash"] = line[21:end_index] # 21 == len('ReqJson{"code_hash":"')
            elif line.startswith('"col":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["col"] = line[7:end_index] # 7 == len('"col":"')
            elif line.startswith('"func":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    # Multi-line func case
                    using_buffer = True
                    buffer += line[8:] # 8 == len('"func":"')
                    continue
                # Single-line func case: save into data directly
                data["func"] = line[8:end_index] 
            elif line.startswith('"func_name":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["func_name"] = line[13:end_index] # 13 == len('"func_name":"')
            elif line.startswith('"js":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["js"] = line[6:end_index] # 6 == len('"js":"')
            elif line.startswith('"key":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["key"] = line[7:end_index] # 7 == len('"key":"')
            elif line.startswith('"phase":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["phase"] = line[9:end_index] # 9 == len('"phase":"')
            elif line.startswith('"row":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["row"] = line[7:end_index] # 7 == len('"row":"')
            elif line.startswith('"site":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["site"] = line[8:end_index] # 8 == len('"site":"')
            elif line.startswith('"start_key":"') and not incomplete_data_block:
                if not line.endswith('",\n'):
                    incomplete_data_block = True
                    continue
                data["start_key"] = line[13:end_index] # 13 == len('"start_key":"')
            elif line.startswith('}ReqEnd') and not incomplete_data_block:
                
                log_phase1_db(data)
                # Initialization
                incomplete_data_block = True
            
            elif using_buffer and not incomplete_data_block:
                if not line.endswith('",\n'):
                    # Multi-line func case is using buffer and not ending
                    buffer += line
                    continue
                else:
                    # Multi-line func ends
                    buffer += line[:end_index]
                    data["func"] = buffer
                    buffer = "" # Reset for the next buffer
                    using_buffer = False
                
                
            # # Append line to buffer, checking for the end of a buffer
            # buffer += line
            # if line.strip().endswith('ReqEnd'):
            #     process_buffer(data, buffer)
            #     buffer = ""  # Reset for the next buffer
    
def run():
    process_log()
    
    # merge in-memory datasets to collections through multi threads
    thread1 = threading.Thread(target=add_undef_prop_dataset_to_db)
    thread2 = threading.Thread(target=add_phase_info_to_db)
    thread3 = threading.Thread(target=add_code_hash_dataset_to_db)
    
    thread1.start()
    thread2.start()
    thread3.start()
    
    thread1.join()
    thread2.join()
    thread3.join() # wait for the all threads to finish before ending the program

if __name__ == '__main__':
    print(LOG_PATH)
    # run()
