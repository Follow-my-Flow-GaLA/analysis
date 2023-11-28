# Originally by Song Li
# run "ls -la --full-time -U inactive_0to100k_phase2_crawl > /home/zfk/Documents/sanchecker/name_list.list" in the sanchecker folder before running this file
# from target_list import result_site_dict
import os, re
from tqdm import tqdm
EXTRACT_SITES_REG = r"(.*_)\d*?_\d*?_\d"
DB_PATH = "/media/datak/inactive/sanchecker"
PREFIX = "inactive_notemplate_phase3_partial_"

def get_target_name_list():
    """
    get a list of target prefixes
    """
    # 01/12 added: extract from list_to_capnp_*.txt
    sites_to_capnp = set()
    for each_file in ['list_to_capnp_recursive_key1key2_0to600k.txt', 
                      'list_to_capnp_recursive_key1key2_600kto1m.txt']:
        with open(each_file, 'r') as fr:
            contents = fr.readlines()
            for line in contents:
                m = re.search(EXTRACT_SITES_REG, line)
                if m and m.group(0):
                    each_site = m.group(1)
                    sites_to_capnp.add(each_site)
                else:
                    raise ValueError
    # return set([e.replace('.', '_', 1)+'_' for e in result_site_dict['ppExploitFOUND'][1]])
    return sites_to_capnp

def get_info_from_file(file_path):
    """
    """
    ret_list = []
    with open(file_path, 'r') as fp:
        all_name_list = fp.readlines()
        for line in tqdm(all_name_list):
            line = line.strip()
            parts = line.split(' ')
            parts = [e for e in parts if e != '']
            if len(parts) < 6:
                continue
            size, time, file_name = parts[4], parts[6], parts[8]
            if int(size) > 336 and file_name not in ['.', '..']:
                ret_list.append(file_name)
    return ret_list 


def keep_file_with_prefix(prefix_list, name_list):
    """
    keep all the names in name_list with prefix in prefix_list
    """
    # using hash table to make it faster
    res_list = []
    for fn in tqdm(name_list):
        # can be future opted by binary search
        base_fn = os.path.basename(fn)
        if base_fn.startswith(prefix_list):
            res_list.append(fn)
    return res_list

if __name__ == "__main__":
    info_list = get_info_from_file(os.path.join(DB_PATH, "name_list.list"))
    # target_prefix = get_target_name_list()
    # res_list = keep_file_with_prefix(tuple(target_prefix), info_list)
    res_list = info_list
    with open(os.path.join(DB_PATH, "list_to_capnp_" + PREFIX), 'w') as fp: # prev: "res.tmp"
        fp.write('\n'.join(res_list))