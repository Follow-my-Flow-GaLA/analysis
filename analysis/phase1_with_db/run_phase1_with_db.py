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

import threading
from pymongo import MongoClient

PRINT_WARNING = False
PRINT_ERROR = True

SITE = 'google.com'
LOG_PATH = '/home/zfk/temp/phase1_release_db_' + SITE.replace(".", "_") + '_log_file'

client = MongoClient("mongodb://localhost:27017/")
db = client["phase1"]
undef_prop_dataset_collection = db["undef_prop_dataset"]
phase_info_collection = db["phase_info"]
code_hash_dataset_collection = db["code_hash_dataset"]

# in-memory data structure to store phase_info and undef_prop_dataset
phase_info = {}
undef_prop_dataset = {}
code_hash_dataset = {}

# the following three functions are used to merge in-memory data to collections
def add_undef_prop_dataset_to_db():
    for code_hash, in_memory_key_dict in undef_prop_dataset.items():
        code_hash_obj = undef_prop_dataset_collection.find_one({"_id": code_hash})
        if code_hash_obj:
            db_key_dict = code_hash_obj["key_dict"]
            for key in in_memory_key_dict.keys():
                if key in db_key_dict:
                    db_key_dict[key] = list(set(db_key_dict[key] + in_memory_key_dict[key]))
                else:
                    db_key_dict[key] = in_memory_key_dict[key]
            undef_prop_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_dict": db_key_dict}}, upsert=True)
        else:
            undef_prop_dataset_collection.update_one(
                {"_id": code_hash},
                {"$set": {
                    "key_dict": undef_prop_dataset[code_hash]
                }}
            , upsert=True)

def add_phase_info_to_db():
    phase_info_collection.update_one(
        {"_id": SITE.replace(".", "_")},
        {"$set": {
            "code_hash_dict": phase_info
        }}
    , upsert=True)

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
                if PRINT_WARNING: print(f"Warning: In-memory undef_prop_dataset (Key is {key}, row and col is {row_col_str}, Code hash is {code_hash}).")
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
            print(f"Field {field} is missing in the log data: {data}")
            return
        
    # check phase
    if data["phase"] != "1":
        print(f"Phase is not 1: {data}")
        return
    
    # check start_key
    valid_start_keys = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC", "JRGE", "JRG"]
    if data["start_key"] not in valid_start_keys:
        print(f"Invalid start key: {data}")
        return
    
    # sanitize site, change dots to underscores
    data["site"] = data["site"].replace(".", "_")
    # sanitize all other fields, change dots to \\2E, change dollar signs to \\24
    data["key"] = data["key"].replace(".", "\\2E").replace("$", "\\24")
    data["func_name"] = data["func_name"].replace(".", "\\2E").replace("$", "\\24")
    data["js"] = data["js"].replace(".", "\\2E").replace("$", "\\24")
    data["func"] = data["func"].replace(".", "\\2E").replace("$", "\\24")

    # add log to the in-memory data structures
    add_log_to_undef_prop_dataset(data)
    add_log_to_phase_info(data)
    add_log_to_code_hash_dataset(data)

# read log and extract data blocks
def read_log_file_readlines():
    count = 0
    with open(LOG_PATH) as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if "ReqJson" in lines[i][0:7]:
                count += 1
                data = {}
                try: 
                    end_index = -3
                    data["code_hash"] = lines[i][len('ReqJson{"code_hash":"'):end_index]
                    i += 1
                    data["col"] = lines[i][len('"col":"'):end_index]
                    i += 1
                    data["func"] = lines[i][len('"func":"'):end_index]
                    i += 1
                    # func can be multi-line
                    while len(lines[i]) < len('"func_name":"') and lines[0:len('"func_name":"')] != '"func_name":"':
                        data["func"] += lines[i]
                        i += 1
                    data["func_name"] = lines[i][len('"func_name":"'):end_index]
                    i += 1
                    data["js"] = lines[i][len('"js":"'):end_index]
                    i += 1
                    data["key"] = lines[i][len('"key":"'):end_index]
                    i += 1
                    data["phase"] = lines[i][len('"phase":"'):end_index]
                    i += 1
                    data["row"] = lines[i][len('"row":"'):end_index]
                    i += 1
                    data["site"] = lines[i][len('"site":"'):end_index]
                    i += 1
                    data["start_key"] = lines[i][len('"start_key":"'):end_index]
                    i += 1
                    log_phase1_db(data)
                except Exception as e:
                    # Note: it is normal that the last line of the log file is not a complete data block
                    #       Therefore, we check if the error is out of index caused by the last line
                    if i >= len(lines):
                        if PRINT_WARNING: print(f"Warning: Last line is not a complete data block.")
                    else:
                        print(f"Error occurred when extracting data block: {e}")
    print(count)

if __name__ == '__main__':
    # approach 1: read log file line by line by readline()
    # Caution: the problem with multi-line func field hasn't been fixed in this approach
    #          For function code, check github commit e5f6ff20c960161d25c3b300caaa93905ef9915a
    # approach 2: read log file line by line by readlines() and save them in memory
    read_log_file_readlines()
    
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