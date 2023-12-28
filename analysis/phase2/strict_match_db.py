import os, re, logging, argparse, codecs, json, glob, difflib
from tqdm import tqdm
from datetime import date
from pprint import pprint
from config import CONFIG
import time
import requests

base_url = "http://localhost:5000/api/"

db_post_error_count = 0

# load website list from db
def load_website_list():
    website_list = []
    url = base_url + "phase1/websites"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print("Error: Failed to load website list from db")
            return []
        website_list = r.json()["website_ids"]
    except Exception as e:
        print("Error: " + str(e))
    return website_list

# get phase1 info for a website
def get_phase1_info(website):
    phase1_info = {}
    url = base_url + "phase1/phase_info?site=" + website
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print("Error: Failed to load phase 1 info for website " + website)
            return {}
        phase1_info = r.json()
    except Exception as e:
        print("Error: " + str(e))
    return phase1_info

# get def_val_dataset for a code_hash
def get_def_value_dataset(code_hash):
    def_value_dict = {}
    url = base_url + "phase2/def_val_dataset?code_hash=" + code_hash
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print("Error: Failed to load def_val_dataset for code_hash " + code_hash)
            return {}
        if r.text == "Code hash not found":
            print("Error: def_val_dataset for code_hash " + code_hash + " not found")
            return {}
        def_value_dict = r.json()
    except Exception as e:
        print("Error: " + str(e))
    return def_value_dict

# post data to change to db
def post_data_to_change_to_db(payload):
    try:
        url = base_url + "phase3/data_to_change"
        payload_json = json.dumps(payload)
        
        headers = {'Content-Type': 'application/json'}  # Adding headers if required
        
        r = requests.post(url, data=payload_json, headers=headers)
        
        if r.status_code != 200:
            print("Error: Failed to post payload to db")
            return False
    except Exception as e:
        print("Error: " + str(e))
        return False
    return True

# this is strict match with dummy value (i.e. if the value is not matched, then it has dummy value "~")
def strict_match_with_dummy_value(website_list):
    for website in website_list:
        # get phase 1 info
        phase1_info = get_phase1_info(website)
        # get all code_hash in phase1_info
        for code_hash, undef_prop_dict in phase1_info["code_hash_dict"].items():
            # get def_val_dataset for this code_hash
            def_value_dict = get_def_value_dataset(code_hash)["key_value_dict"]
            # match undef_prop_dict and def_value_dict
            for undef_prop_key in undef_prop_dict.keys():
                payload = {
                    "phase": "3",
                    "site": website,
                    "var_name": undef_prop_key,
                    "row": undef_prop_dict[undef_prop_key][0].split(",")[0],
                    "col": undef_prop_dict[undef_prop_key][0].split(",")[1],
                    "file_name": undef_prop_dict[undef_prop_key][1],
                }
                if undef_prop_key in def_value_dict: # matched
                    payload["payload"] = def_value_dict[undef_prop_key]["value"]
                else: # not matched, use dummy value "~"
                    payload["payload"] = "~"
                # post to db
                post_data_to_change_to_db(payload) 

if __name__ == "__main__":
    website_list = load_website_list()
    strict_match_with_dummy_value(website_list)
    