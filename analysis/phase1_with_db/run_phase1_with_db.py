import threading
from pymongo import MongoClient


LOG_PATH = '/home/zfk/temp/phase1_release_db_google_com_log_file'

client = MongoClient("mongodb://localhost:27017/")
db = client["phase1"]
undef_prop_dataset_collection = db["undef_prop_dataset"]
phase_info_collection = db["phase_info"]


def add_log_to_undef_prop_dataset(data):
    code_hash = data["code_hash"]
    code_hash_obj = undef_prop_dataset_collection.find_one({"_id": code_hash})
    row_col_str = data["row"] + ", " + data["col"]
    if (code_hash_obj):
        # code_hash already exists, check if key exists
        key_value_dict = code_hash_obj["key_value_dict"]
        if (data["key"] in key_value_dict):
            # key also exists, check if row_col exists
            row_col_list = key_value_dict[data["key"]]
            if row_col_str in row_col_list:
                print(f"Row and col already exists in undef_prop_dataset (Key is {data['key']}, Code hash is {code_hash}).")
            else:
                # Add new row_col_str
                row_col_list.append(row_col_str)
                key_value_dict[data["key"]] = row_col_list
                undef_prop_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": key_value_dict}}, upsert=True)
        else:
            # key does not exist, add it
            key_value_dict[data["key"]] = [row_col_str]
            undef_prop_dataset_collection.update_one({"_id": code_hash}, {"$set": {"key_value_dict": key_value_dict}}, upsert=True)
    else:
        # code_hash does not exist, add it
        undef_prop_dataset_collection.update_one(
            {"_id": code_hash},
            {"$set": {
                "key_value_dict": {
                    data["key"]: [row_col_str]
                }
            }}
        , upsert=True)

def add_log_to_phase_info(data):
    code_hash = data["code_hash"]
    site_obj = phase_info_collection.find_one({"_id": data["site"]})
    row_col_str = data["row"] + ", " + data["col"]
    if (site_obj):
        # site already exists, check if code_hash exists
        code_hash_dict = site_obj["code_hash_dict"]
        if (code_hash in code_hash_dict):
            # code_hash also exists, check if key exists
            key_value_dict = code_hash_dict[code_hash]
            if (data["key"] in key_value_dict):
                # key also exists, check if row_col exists
                row_col_list = key_value_dict[data["key"]][0]
                if row_col_str in row_col_list:
                    print(f"Key already exists in phase_info (Key is {data['key']}, Code hash is {code_hash}Site is {data['site']}).")
                else: 
                    # if row_col does not exist, add it
                    row_col_list.append(row_col_str)
                    code_hash_dict[code_hash] = key_value_dict
                    # TODO: check
                    phase_info_collection.update_one({"_id": data["site"]}, {"$set": {"code_hash_dict": code_hash_dict}}, upsert=True)
            else:
                key_value_dict[data["key"]] = [
                    [row_col_str],
                    data["js"],
                    data["func_name"],
                    data["func"]
                ]
                code_hash_dict[code_hash] = key_value_dict
                phase_info_collection.update_one({"_id": data["site"]}, {"$set": {"code_hash_dict": code_hash_dict}}, upsert=True)
        else:
            key_value_dict = {
                data["key"]: [
                    [row_col_str],
                    data["js"],
                    data["func_name"],
                    data["func"]
                ]
            }
            code_hash_dict[code_hash] = key_value_dict
            phase_info_collection.update_one({"_id": data["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}}, upsert=True)
    else: 
        phase_info_collection.update_one(
            {"_id": data["site"]},
            {"$set": {
                "code_hash_dict": {
                    code_hash: {
                        data["key"]: [
                            [row_col_str],
                            data["js"],
                            data["func_name"],
                            data["func"]
                        ]
                    }
                }
            }}
        , upsert=True)

# multi-threading to add log to two collections 
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
    valid_start_keys = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC"]
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
    
    # add log to two collection through two threads
    thread1 = threading.Thread(target=add_log_to_undef_prop_dataset, args=(data,))
    thread2 = threading.Thread(target=add_log_to_phase_info, args=(data,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join() # wait for the two threads to finish before proceeding to the next log

# read log file line by line to extract the data block
def read_log_file_readline():
    count = 0
    with open(LOG_PATH) as f:
        l = f.readline()
        while l:
            if "ReqJson" in l[0:7]:
                count += 1
                data = {}
                try: 
                    end_index = -3
                    data["code_hash"] = l[len('ReqJson{"code_hash":"'):end_index]
                    data["col"] = f.readline()[len('"col":"'):end_index]
                    data["func"] = f.readline()[len('"func":"'):end_index]
                    data["func_name"] = f.readline()[len('"func_name":"'):end_index]
                    data["js"] = f.readline()[len('"js":"'):end_index]
                    data["key"] = f.readline()[len('"key":"'):end_index]
                    data["phase"] = f.readline()[len('"phase":"'):end_index]
                    data["row"] = f.readline()[len('"row":"'):end_index]
                    data["site"] = f.readline()[len('"site":"'):end_index]
                    data["start_key"] = f.readline()[len('"start_key":"'):end_index]
                    log_phase1_db(data)
                except Exception as e:
                    print(f"Error occurred when extracting data block: {e}")
            l = f.readline()
    print(count)

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
                    data["col"] = lines[i+1][len('"col":"'):end_index]
                    data["func"] = lines[i+2][len('"func":"'):end_index]
                    data["func_name"] = lines[i+3][len('"func_name":"'):end_index]
                    data["js"] = lines[i+4][len('"js":"'):end_index]
                    data["key"] = lines[i+5][len('"key":"'):end_index]
                    data["phase"] = lines[i+6][len('"phase":"'):end_index]
                    data["row"] = lines[i+7][len('"row":"'):end_index]
                    data["site"] = lines[i+8][len('"site":"'):end_index]
                    data["start_key"] = lines[i+9][len('"start_key":"'):end_index]
                    log_phase1_db(data)
                    i += 10
                except Exception as e:
                    print(f"Error occurred when extracting data block: {e}")

if __name__ == '__main__':
    # read_log_file_readlines()
    
    read_log_file_readline()
    
    # test_data = {
    #     "phase": "1",
    #     "start_key": "RTO",
    #     "site": "site2",
        
    #     "func": "func1",
        
    #     "code_hash": "code_hash1",
    #     "key": "key1",
    #     "row": "row1",
    #     "col": "col1",
        
    #     "func": "func1",
    #     "func_name": "func_name1",
    #     "js": "js1",
    # }
    # log_phase1_db(test_data)