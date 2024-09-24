import os, re, codecs, glob, difflib
from tqdm import tqdm
from phase3_config import CONFIG
from pymongo import MongoClient
from exploit_gen.exploit_generator import ExploitGenerator
from exploit_gen.payload_comp import best_match, exploit_tuning
from record_reader import get_sink_val_list

### Note: row_col is in the format of "row,col"
###       all dummy values are currently filtered out

GENERATE_SUMMARY = False
GENERATE_LOG = False
LIMIT = 100000

client = MongoClient("mongodb://localhost:27017/")
db = client["phase3"]
data_to_change_collection = db["data_to_change"]
def_val_dataset_collection = db["def_val_dataset"]

# global variable for summary
num_of_sites = 0
total_source_count = 0  
total_sink_count = 0
total_flow_found_count = 0
total_flow_not_found_count = 0
sink_dict = {}
unique_combinations = set()
unique_combo_dict = {}

def get_website_set():
    fpath = "/media/datak/inactive/sanchecker/04_18_detector_1M_phase3_db_crawl_consequence.log"
    first_line = "{}"
    with open(fpath, "r") as f:
        first_line = f.readline()
    website_set = eval(first_line)
    # replace all . to _
    website_set = [x.replace(".","_") for x in website_set]
    global num_of_sites
    num_of_sites = len(website_set)
    return website_set

# output: data_to_change_list = [{var_name, row_col(array), payload, file_name, sink_type}]
def get_data_to_change_list(site):    
    data_to_change_obj = data_to_change_collection.find_one({"_id": site})
    if not data_to_change_obj:
        if GENERATE_LOG: print(f"Error: {site} not found in data_to_change_collection")
        return []
    data_to_change_list = data_to_change_obj["data_to_change"]
    # change dummy value from ~ to "dummy"
    # for data in data_to_change_list:
    #     if data["payload"] == "~":
    #         data["payload"] = "dummy"
    global total_source_count
    total_source_count += len(data_to_change_list)
    return data_to_change_list
 
# output: sink_dict = {site: [{var_name, row_col(array), src_payload, file_name, sink_payload, sink_type, start_pos, end_pos, sink_string, message_id}]
def update_sink_dict(site, sink_val_list, data_to_change_list):
    global total_sink_count
    total_sink_count += len(sink_val_list)
    global total_flow_found_count, total_flow_not_found_count, sink_dict
    sink_dict[site] = []
    # create a dict to store if flow is found for each payload_val
    flow_found_dict = {}
    for sink_val in sink_val_list:
        flow_found_dict[sink_val["sink_payload"]] = False
    # compare sink_val_list with data_to_change_list
    check_duplicate_set = set()
    for data_to_change in data_to_change_list:
        payload = data_to_change["payload"]
        for sink_val in sink_val_list:
            ratio, best_substring = best_match(payload, sink_val["sink_payload"])
            if ratio > CONFIG.STR_MATCH_THRESHOLD:
                flow_found_dict[sink_val["sink_payload"]] = True
                sink_dict_elem = {
                    "var_name": data_to_change["var_name"],
                    "row_col": data_to_change["row_col"],
                    "src_payload": data_to_change["payload"],
                    "file_name": data_to_change["file_name"],
                    "sink_type": sink_val["sink_type"],
                    "sink_payload": sink_val["sink_payload"],
                    "start_pos": sink_val["start_pos"],
                    "end_pos": sink_val["end_pos"],
                    "sink_string": sink_val["sink_string"],
                    "message_id": sink_val["message_id"],
                }
                if str(sink_dict_elem) in check_duplicate_set:
                    pass
                else:
                    sink_dict[site].append(sink_dict_elem)
                    check_duplicate_set.add(str(sink_dict_elem))
                break
    # count flow found and not found 
    flow_found_count = 0
    flow_not_found_count = 0
    for sink_val in sink_val_list:
        if flow_found_dict[sink_val["sink_payload"]]:
            flow_found_count = flow_found_count + 1
        else:
            flow_not_found_count = flow_not_found_count + 1
    total_flow_found_count = total_flow_found_count + flow_found_count
    total_flow_not_found_count = total_flow_not_found_count + flow_not_found_count
    # if GENERATE_LOG: print("", site, " flow_found_count is: ", flow_found_count, " flow_not_found_count is: ", flow_not_found_count) 

def update_uniqueness(site):
    global sink_dict, unique_combinations, unique_combo_dict
    sink_data_list = sink_dict[site]
    # get phase_info from phase1
    phase_info = client["phase1"]["phase_info"].find_one({"_id": site})
    if not phase_info:
        if GENERATE_LOG: print(f"Error: {site} not found in phase_info")
        return
    for data in sink_data_list:
        data_var_name = data["var_name"]
        data_row_col = data["row_col"]
        data_file_name = data["file_name"]
        for code_hash, key_dict in phase_info["code_hash_dict"].items():
            if data_var_name in key_dict:
                # check if the row_col and file_name are the same
                if str(data_row_col) == str(key_dict[data_var_name][0]) and data_file_name == key_dict[data_var_name][1]:
                    data_code_hash = code_hash
                    # add key to uniqueness
                    combination = (data_var_name, data_code_hash)
                    unique_combinations.add(combination)
                    combo_str = ', '.join(combination)
                    if combo_str not in unique_combo_dict:
                        unique_combo_dict[combo_str] = [set(),set()]
                    unique_combo_dict[combo_str][0].add(data["src_payload"])
                    unique_combo_dict[combo_str][1].add(data_var_name)
                    break
        if GENERATE_LOG: print("Error: not able to find data in phase_info: ", data)

def replace_no_quote(begin, whole):
    # Decide if str whole startswith str begin, ignoring ', " and `
    begin_idx = 0
    whole_idx = 0
    while begin_idx != len(begin):
        if whole[whole_idx] == begin[begin_idx]:
            begin_idx += 1
            whole_idx += 1
            continue
        elif begin[begin_idx] in ['"', "'", "`"]:
            begin_idx += 1
            continue
        elif whole[whole_idx] in ['"', "'", "`"]:
            whole_idx += 1
            continue
        else:
            # Not matched
            return None
    return whole[whole_idx:]

# Note: this function will change payload in sink_dict
def generate_and_save_exploit(using_db_buffer=False, using_result_buffer=False):
    global sink_dict

    if using_result_buffer:
        assert os.path.exists("/media/datak/inactive/analysis/phase3/result_buffer.py")
        from result_buffer import js_ans, non_js_sink
        return_dict = {}
        for site in {**js_ans, **non_js_sink}.keys():
            return_dict[site] = []
            if site in js_ans.keys():
                for each_js_ans_dict in js_ans[site]:
                    if "exploit" in each_js_ans_dict.keys() and "MyString" not in each_js_ans_dict["exploit"]:
                        if "code" in each_js_ans_dict.keys() and \
                            each_js_ans_dict["exploit"].startswith(each_js_ans_dict["code"].replace('MyString','')):
                                each_js_ans_dict["exploit"] = each_js_ans_dict["exploit"].replace(each_js_ans_dict["code"].replace('MyString',''), '')
                        elif "code" in each_js_ans_dict.keys() and \
                            replace_no_quote(each_js_ans_dict["code"].replace('MyString',''), each_js_ans_dict["exploit"]): 
                                each_js_ans_dict["exploit"] = replace_no_quote(each_js_ans_dict["code"].replace('MyString',''), each_js_ans_dict["exploit"])
                        else:
                            # the exploit could possibly come from llm_config
                            from exploit_gen.llm_config import CONFIG as llm_config
                            for idx, each_ans in enumerate(llm_config['HIS_ANS']):
                                if each_js_ans_dict["exploit"] == each_ans:
                                    each_js_ans_dict["exploit"] = llm_config['CORRESPONDING_EXPLOIT'][idx]
                                    break
                            else:
                                # the exploit needs no more operations! 
                                pass
                        return_dict[site].append(each_js_ans_dict)
            if site in non_js_sink.keys():
                for each_non_js_sink_dict in non_js_sink[site]:
                    if "exploit" in each_non_js_sink_dict.keys() and "MyString" not in each_non_js_sink_dict["exploit"]:
                        # if containing "MyString", consider as unsuccessful exploit gen
                        return_dict[site].append(each_non_js_sink_dict)
        result = {key:value for key,value in return_dict.items() if value}
        
    else:
        eg = ExploitGenerator()
        result = eg.process(sink_dict, using_buffer=using_db_buffer)
    # print(result)
    
    # store to db
    """
    DB structure for phase3.exploit:
    {
        _id: site,
        exploit_list: [
            {
                var_name: var_name,
                row_col: row_col(array),
                src_payload: src_payload,
                file_name: file_name (sanitized),
                sink_type: sink_type,
                sink_payload: sink_payload,
                start_pos: start_pos,
                end_pos: end_pos,
                sink_string: sink_string,
                message_id: message_id,
                code: exploit_code
            }
        ]
    }
    """
    for site, exploit_list in result.items():
        if exploit_list:
            db["exploit"].update_one(
                {"_id": site}, 
                {"$set": {"exploit_list": exploit_list}}
            , upsert=True)
        
def print_summary(output_file):
    global num_of_sites, total_source_count, total_sink_count, total_flow_found_count, total_flow_not_found_count, sink_dict, unique_combinations, unique_combo_dict
    with open(output_file, "w") as f:
        f.write("Number of sites: " + str(num_of_sites) + "\n")
        f.write("Number of elements in data_to_change(source, not unique): " + str(total_source_count) + "\n")
        f.write("Number of elements in sink_val_set(sink/flow, not unique): " + str(total_sink_count) + "\n")
        f.write("For all flows, we tried to match them with source. " + "\n")
        f.write("\tNumber of flows found(matched, not unique): " + str(total_flow_found_count) + "\n")
        f.write("\tNumber of flows not found(matched, not unique): " + str(total_flow_not_found_count) + "\n")
        f.write("\n")
        f.write("Number of unique combinations: " + str(len(unique_combinations)) + "\n")
        for combo in unique_combinations:
            f.write(str(combo) + "\n")
            f.write(str(unique_combo_dict[', '.join(combo)]) + "\n")
        f.write("\n")
        f.write("sink_dict: " + str(sink_dict))

if __name__ == "__main__":
    website_set = get_website_set()
    
    counter = 0
    
    using_db_buffer = True
    using_result_buffer = True
    
    if not using_db_buffer:
        os.chdir(CONFIG.PHASE3_RECORD_PATH)
        for fpath in tqdm(glob.iglob( "record_*" )):
            z = fpath.split('_')
            site = '_'.join(z[1:len(z)-3])
            site = site.replace(".","_")
            
            # check if site is in website_set
            if site not in website_set:
                continue
            else:
                counter = counter + 1
                if counter > LIMIT:
                    break
                # print(site)
            
            # read record file
            sink_val_list = get_sink_val_list(site, fpath)
            
            # read data to change from db
            data_to_change_list = get_data_to_change_list(site)
            # get only non-dummy payload values
            data_to_change_list = [x for x in data_to_change_list if x["payload"] != "~"]
            
            # update sink_dict
            update_sink_dict(site, sink_val_list, data_to_change_list)
            
            # update uniqueness
            if GENERATE_SUMMARY: update_uniqueness(site)
     
    # generate exploit: using openai for JS sink, and persistent-xss tool for html/scriptsrc sink
    generate_and_save_exploit(using_db_buffer=using_db_buffer, using_result_buffer=using_result_buffer)
        
    # summary
    if GENERATE_SUMMARY: 
        output_file = "/media/datak/inactive/analysis/phase3/count_gadgets_log/5_6_count_gadgets_summary"
        print_summary(output_file)