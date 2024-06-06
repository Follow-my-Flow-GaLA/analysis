import threading, argparse, codecs
from pymongo import MongoClient
import pymongo

class LogProcessor: 
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
    def __init__(self, site='google.com', log_path=None, error_logger=None, long_data_logger=None):
        self.SITE = site
        self.LOG_PATH = log_path if log_path else '/home/zfk/temp/phase1_release_db_' + self.SITE.replace(".", "_", 1) + '_log_file'
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["phase1"]
        self.undef_prop_dataset_collection = self.db["undef_prop_dataset"]
        self.phase_info_collection = self.db["phase_info"]
        self.code_hash_dataset_collection = self.db["code_hash_dataset"]
        
        # in-memory data structure to store phase_info and undef_prop_dataset
        self.phase_info = {}
        self.undef_prop_dataset = {}
        self.code_hash_dataset = {}
        
        self.PRINT_WARNING = False
        self.PRINT_ERROR = True
        self.error_logger = error_logger
        self.long_data_logger = long_data_logger

    # the following three functions are used to merge in-memory data to collections
    def add_undef_prop_dataset_to_db(self):
        for code_hash, in_memory_key_dict in self.undef_prop_dataset.items():
            # setOnInsert for code_hash that doesn't exist
            try: 
                self.undef_prop_dataset_collection.update_one(
                    {"_id": code_hash},
                    {"$setOnInsert": {
                        "key_dict": in_memory_key_dict
                    }},
                    upsert=True
                )
            except pymongo.errors.WriteError as e:
                if self.PRINT_ERROR: 
                    self.error_logger.info(f"{self.site}: pymongo.errors.WriteError (document exceeding 16777216) in add_undef_prop_dataset_to_db (line:76): {code_hash}: {e}")
                
            # addToSet for code_hash that exists
            for key, row_col_list in in_memory_key_dict.items():
                if key: # check if key is not empty
                    try: 
                        self.undef_prop_dataset_collection.update_one(
                            {"_id": code_hash},
                            {"$addToSet": {
                                f"key_dict.{key}": {"$each": row_col_list}
                            }}
                        )
                    except pymongo.errors.WriteError as e:
                        if self.PRINT_ERROR: 
                            self.error_logger.info(f"{self.SITE}: add_undef_prop_dataset_to_db pymongo.errors.WriteError: {code_hash}")
                else:
                    if self.PRINT_ERROR: 
                        self.error_logger.info(f"{self.SITE}: Error: Key is empty for code hash {code_hash}.")
            

    def add_phase_info_to_db(self):
        try: 
            self.phase_info_collection.update_one(
                {"_id": self.SITE.replace(".", "_")},
                {"$set": {
                    "code_hash_dict": self.phase_info
                }}
            , upsert=True)
        except pymongo.errors.WriteError as e:
            if self.PRINT_ERROR: 
                self.error_logger.info(f"{self.SITE}: add_phase_info_to_db pymongo.errors.WriteError: {e}")
        except Exception as e:
            if self.PRINT_ERROR: 
                self.error_logger.info(f"{self.SITE}: add_phase_info_to_db: {e}")

    def add_code_hash_dataset_to_db(self):
        for code_hash in self.code_hash_dataset.keys():
            code_hash_obj = self.code_hash_dataset_collection.find_one({"_id": code_hash})
            if not code_hash_obj:
                self.code_hash_dataset_collection.update_one(
                    {"_id": code_hash},
                    {"$set": {
                        "func": self.code_hash_dataset[code_hash]
                    }}
                , upsert=True)

    # the following three functions are used to add log to the in-memory data structures
    def add_log_to_undef_prop_dataset(self, data):
        code_hash = data["code_hash"]
        key = data["key"]
        row_col_str = data["row"] + ", " + data["col"]
        if code_hash in self.undef_prop_dataset:
            if key in self.undef_prop_dataset[code_hash]:
                if row_col_str in self.undef_prop_dataset[code_hash][key]:
                    if self.PRINT_WARNING: 
                        print(f"Warning: In-memory undef_prop_dataset (Key is {key}, row and col is {row_col_str}, Code hash is {code_hash}).")
                else:
                    self.undef_prop_dataset[code_hash][key].append(row_col_str)
            else:
                self.undef_prop_dataset[code_hash][key] = [row_col_str]
        else:
            self.undef_prop_dataset[code_hash] = {
                key: [row_col_str]
            }

    def add_log_to_phase_info(self, data):
        code_hash = data["code_hash"]
        key = data["key"]
        row_col_str = data["row"] + ", " + data["col"]
        if code_hash in self.phase_info:
            if key in self.phase_info[code_hash]:
                if row_col_str in self.phase_info[code_hash][key][0]:
                    if self.PRINT_WARNING: print(f"Warning: In-memory phase_info (Key is {key}, row and col is {row_col_str}, Code hash is {code_hash}).")
                else:
                    self.phase_info[code_hash][key][0].append(row_col_str)
            else:
                self.phase_info[code_hash][key] = [[row_col_str], data["js"], data["func_name"]]
        else:
            self.phase_info[code_hash] = {
                key: [[row_col_str], data["js"], data["func_name"]]
            }

    def add_log_to_code_hash_dataset(self, data):
        code_hash = data["code_hash"]
        if code_hash in self.code_hash_dataset:
            if self.PRINT_WARNING: print(f"Warning: In-memory code_hash_dataset (Code hash is {code_hash}).")
        else:
            self.code_hash_dataset[code_hash] = data["func"]

    # validate data blocks from log file and add them to the in-memory data structures
    def log_phase1_db(self, data):
        # check fields
        required_fields = ['code_hash', 'phase', 'start_key', 'site', 'key', 'func_name', 'js', 'row', 'col', 'func']
        for field in required_fields:
            if field not in data:
                self.error_logger.info(f"{self.SITE}: Field {field} is missing in the log data: {data}")
                return
            
        # check phase
        if data["phase"] != "1":
            self.error_logger.info(f"{self.SITE}: Phase is not 1: {data}")
            return
        
        # check start_key
        valid_start_keys = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC", "JRGE", "JRG"]
        if data["start_key"] not in valid_start_keys:
            self.error_logger.info(f"{self.SITE}: Invalid start key: {data}")
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
            self.long_data_logger.info(f"{self.SITE}: Long data: {data}")
            return
            
        # add log to the in-memory data structures
        self.add_log_to_undef_prop_dataset(data)
        self.add_log_to_phase_info(data)
        self.add_log_to_code_hash_dataset(data)

    # read log and extract data blocks
    def read_log_file_readlines(self):
        count = 0
        with codecs.open(self.LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
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
                        self.log_phase1_db(data)
                    except Exception as e:
                        # Note: it is normal that the last line of the log file is not a complete data block
                        #       Therefore, we check if the error is out of index caused by the last line
                        if i >= len(lines):
                            if self.PRINT_WARNING: 
                                print(f"Warning: Last line is not a complete data block.")
                        else:
                            self.error_logger.info(f"{self.SITE}: Error occurred when extracting data block: {e}")
        
    def process_log(self):
        with codecs.open(self.LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
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
                    
                    self.log_phase1_db(data)
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
                #     self.process_buffer(data, buffer)
                #     buffer = ""  # Reset for the next buffer
       
    def run(self):
        # self.read_log_file_readlines()
        self.process_log()
        
        # merge in-memory datasets to collections through multi threads
        thread1 = threading.Thread(target=self.add_undef_prop_dataset_to_db)
        thread2 = threading.Thread(target=self.add_phase_info_to_db)
        thread3 = threading.Thread(target=self.add_code_hash_dataset_to_db)
        
        thread1.start()
        thread2.start()
        thread3.start()
        
        thread1.join()
        thread2.join()
        thread3.join() # wait for the all threads to finish before ending the program

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Log File Processor")
    parser.add_argument('--site', type=str, default='google.com', help='The site to process')
    parser.add_argument('--log_path', type=str, default=None, help='Full path to the log file')
    args = parser.parse_args()
    
    processor = LogProcessor(site=args.site, log_path=args.log_path)
    processor.run()
