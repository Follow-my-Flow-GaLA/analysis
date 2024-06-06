from concurrent.futures import ProcessPoolExecutor
import os, json, codecs, logging, csv
from tqdm import tqdm
from pymongo import MongoClient

# Function to set up and configure a logger
def setup_logger(logger_name, log_file, level=logging.INFO, include_time=True):
    """
    This function sets up a logger for logging purposes.

    Parameters:
    - logger_name: Name of the logger.
    - log_file: Path to the log file where log messages will be written.
    - level: Log level (default is logging.INFO).
    - include_time: Boolean indicating whether to include time in log messages (default is True).
    """
    log_setup = logging.getLogger(logger_name)
    
    # Choose the formatter based on whether time should be included
    if include_time:
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        formatter = logging.Formatter('%(message)s')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)

# Initialize loggers for various purposes
setup_logger("started", "/media/datak/inactive/analysis/phase2/strict_match/logs/started.log")
setup_logger("end", "/media/datak/inactive/analysis/phase2/strict_match/logs/end.log", include_time=False)
setup_logger("error", "/media/datak/inactive/analysis/phase2/strict_match/logs/error.log")
error_logger = logging.getLogger('error')
started_logger = logging.getLogger('started')
end_logger = logging.getLogger("end")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]
phase2_db = client["phase2"]
phase3_db = client["phase3"]

db_post_error_count = 0

# get phase1 info for a website
def get_phase1_info(website):
    try:
        return phase1_db["phase_info"].find_one({"_id": website})
    except Exception as e:
        print("Error when loading phase1 info for website " + website + ": " + str(e))
    return []

# get def_val_dataset for a code_hash
def get_def_value_dataset(code_hash):
    try:
        def_value_dict = phase2_db["def_val_dataset"].find_one({"_id": code_hash})
        if not def_value_dict:
            pass
            # print("Error: def_val_dataset for code_hash " + code_hash + " not found")
        else:
            return def_value_dict
    except Exception as e:
        pass
        # print("Error: Failed to load def_val_dataset for code_hash " + code_hash)
    return {}

# get failed_value_dataset for a code_hash
def get_failed_value_dataset(code_hash):
    try:
        failed_value_dict = phase2_db["failed_val_dataset"].find_one({"_id": code_hash})
        if not failed_value_dict:
            pass
            # print("Error: failed_value_dataset for code_hash " + code_hash + " not found")
        else:
            return failed_value_dict
    except Exception as e:
        pass
        # print("Error: Failed to load failed_value_dataset for code_hash " + code_hash)
    return {}

# post data to change to db
def post_data_to_change_to_db(payload):
    # add site to data_to_change only if it does not exist
    phase3_db["data_to_change"].update_one(
        {"_id": payload["site"]}, 
        {"$setOnInsert": {
            "data_to_change": []
        }},
        upsert=True
    )
    # append data to change
    phase3_db["data_to_change"].update_one(
        {"_id": payload["site"]},
        {"$push": {
            "data_to_change": {
                "var_name": payload["var_name"],
                "payload": payload["payload"],
                "row_col": payload["row_col"],
                "file_name": payload["file_name"]
            }
        }}
    )

# post data to change (with failed flow) to db
def post_data_to_change_failed_flow_to_db(payload):
    phase3_db["data_to_change_failed_flow"].update_one(
        {"_id": payload["site"]},
        {"$setOnInsert": {
            "data_to_change": []
        }},
        upsert=True
    )
    phase3_db["data_to_change_failed_flow"].update_one(
        {"_id": payload["site"]},
        {"$push": {
            "data_to_change": {
                "var_name": payload["var_name"],
                "payload": payload["payload"],
                "row_col": payload["row_col"],
                "file_name": payload["file_name"]
            }
        }}
    )

# post data to change (with dummy value) to db
def post_data_to_change_dummy_value_to_db(payload):
    phase3_db["data_to_change_dummy_value"].update_one(
        {"_id": payload["site"]},
        {"$setOnInsert": {
            "data_to_change": []
        }},
        upsert=True
    )
    phase3_db["data_to_change_dummy_value"].update_one(
        {"_id": payload["site"]},
        {"$push": {
            "data_to_change": {
                "var_name": payload["var_name"],
                "payload": payload["payload"],
                "row_col": payload["row_col"],
                "file_name": payload["file_name"]
            }
        }}
    )

# this is strict match with dummy value (i.e. if the value is not matched, then it has dummy value "~")
def strict_match_with_dummy_value(website):
    website = website.replace(".","_")
    # get phase 1 info
    phase1_info = get_phase1_info(website)
    if not phase1_info:
        return
    # get all code_hash in phase1_info
    for code_hash, undef_prop_dict in phase1_info["code_hash_dict"].items():
        # get value_dataset for this code_hash
        def_value_dataset = get_def_value_dataset(code_hash)
        failed_value_dataset = get_failed_value_dataset(code_hash)
        def_value_dict = def_value_dataset["key_value_dict"] if def_value_dataset else {}
        failed_value_dict = failed_value_dataset["key_value_dict"] if failed_value_dataset else {}
        # match undef_prop_dict and def_value_dict
        for undef_prop_key in undef_prop_dict.keys():
            payload = {
                "phase": "3",
                "site": website,
                "var_name": undef_prop_key,
                "row_col": undef_prop_dict[undef_prop_key][0],
                "file_name": undef_prop_dict[undef_prop_key][1],
            }
            # not matched, use dummy value "~"
            payload["payload"] = "~"
            if undef_prop_key in def_value_dict: # matched key
                payload["payload"] = def_value_dict[undef_prop_key]["value"]
                post_data_to_change_to_db(payload) 
            elif undef_prop_key in failed_value_dict: # matched key
                payload["payload"] = failed_value_dict[undef_prop_key]["value"]
                post_data_to_change_failed_flow_to_db(payload)
            else:
                post_data_to_change_dummy_value_to_db(payload)

# csv file path
csv_file_path = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"

class ParallelLogProcessor:
    def __init__(self, progress_file, max_workers=20, slice_size=64):
        self.progress_file = progress_file
        self.max_workers = max_workers
        self.slice_size = slice_size
        self.target_sites = self.extract_domains_from_csv() # if <condition> else <other_func>
        self.processed_sites = self.load_progress()
    
    def extract_domains_from_csv(self):
        domains = []
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Assuming the domain is the second column in each row
                if row:  # Check if the row is not empty
                    domains.append(row[1])
        return domains
    
    def load_progress(self):
        processed_sites = []
        with open(self.progress_file, 'r') as f:
            # Assuming each line in progress_file represents a site
            for each_line in f:
                processed_sites.append(each_line.strip())
        return processed_sites
    
    def process_log_file(self, site_list):
        for site in site_list:
            started_logger.info("{} started".format(site))
            try:
                strict_match_with_dummy_value(site)
                end_logger.info("{}".format(site))
            except KeyboardInterrupt:
                # User wants to quit. Abort. 
                break
            except Exception as e:
                error_logger.info("{} error!==> {} ".format(site, e))
                continue
    
    def generate_tasks(self, mode="sites"):
        tasks = []
        if mode == "sites":
            target_sites_set = set(self.target_sites)
            processed_sites_set = set(self.processed_sites)
            sites_to_process = target_sites_set - processed_sites_set
            for each_site in sites_to_process:
                tasks.append(each_site)
        return tasks

    def process_all_sites(self):
        print("Starting to generate tasks")
        tasks = self.generate_tasks()
        task_slices = [tasks[i:i + self.slice_size] for i in range(0, len(tasks), self.slice_size)]
        print("Finishing generating tasks")
        
        total_tasks = len(task_slices)
        with tqdm(total=total_tasks, desc="Processing") as pbar:
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                # Wrap executor.map with tqdm
                for _ in executor.map(self.process_log_file, task_slices):
                    pbar.update(1)

if __name__ == "__main__":
    progress_file = "/media/datak/inactive/analysis/phase2/strict_match/logs/end.log"
    print("Starting initializing ParallelLogProcessor")
    parallel_processor = ParallelLogProcessor(progress_file=progress_file)
    print("Finished initializing ParallelLogProcessor")
    parallel_processor.process_all_sites()