# -*- coding: future_fstrings -*-
#!python3
from __future__ import print_function
import os, re, logging, argparse, codecs, json, glob, difflib
from tqdm import tqdm
from datetime import date
from pprint import pprint
from config import CONFIG

# Function to get a list of finished log files
def get_finished_list(target_path):
    """
    This function extracts the list of finished log files from a specified target path.

    Parameters:
    - target_path (str): The path to the target log files.

    Returns:
    - finished_set: A set containing the names of finished log files.
    """
    FINISHED_REG = r"INFO: .*?(?:AM|PM) (.*?_log_file) started"
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, target_path), 'r', encoding='utf-8', errors='replace') as f0:
        contents = f0.read()
        
        maybe_result = re.finditer(FINISHED_REG, contents, re.M | re.S)
        if maybe_result:
            finished_set = set()
            for matched_group in maybe_result:
                finished_set.add(matched_group.group(1))
                
    return finished_set

# Function to output an iterable to a file
def output_target_iter(target_iter, write_path):
    """
    This function writes an iterable to a specified file.

    Parameters:
    - target_iter: The iterable to be written.
    - write_path (str): The path to the output file.
    """
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, write_path), 'w', encoding='utf-8') as fw:
        for each in target_iter:
            fw.write(each + '\n')

# Function to read an iterable from a file
def read_iter(read_path):
    """
    This function reads an iterable from a specified file.

    Parameters:
    - read_path (str): The path to the input file.

    Returns:
    - iter_set: A set containing the items read from the file.
    """
    with codecs.open(os.path.join(CONFIG.THIS_ROOT_PATH, read_path), 'r', encoding='utf-8', errors='replace') as f0:
        contents = f0.read()
        iter_set = set(contents.split('\n'))
    return iter_set

# Function to count unique definition values from a JSON file
def count_def_values(json_path):
    """
    This function counts unique definition values from a JSON file.

    Parameters:
    - json_path (str): The path to the JSON file containing definition values.
    """
    with open(json_path, 'r') as file:
        # Guaranteed data structure: 
        # {
        #     "codeHash1": {"var1": "lineNumber1"}, 
        #     "codeHash2": {"var2": "lineNumber2"},
        #     "codeHash3": {"var3": "lineNumber3"},
        # }
        data = json.load(file)

    def_val_set = set()
    for value in data.values():
        vars = value.keys()
        def_val_set.update(vars)

    with open('/home/zfk/Documents/sanchecker/src/Inactive/' + date.today().strftime("%m_%d_") + 'def_values.py', 'w') as f1: 
        f1.write(f'''def_value_json={{
        '# of unique def values: ': {len(def_val_set)}, 
        '# of gadgets found: ': {len(data.keys())}, 
        'List of def values: ': {def_val_set}
        }}''')
    
    print('# of unique def values: ', len(def_val_set), '\n', def_val_set)
    print('# of gadgets found: ', len(data.keys()))

# Function to check definition flows in log records
def check_def_flows(target_str='', mode='count_flow'):
    """
    This function checks definition flows in log records and generates statistics.

    Parameters:
    - target_str (str): A target string used for log file selection.
    - mode (str): The mode of operation (optional, default is 'count_flow').
    """
    # If the injected payload is only "testk" and "testv", strict_check_mode is True; otherwise False
    # from all_vul_websites import vul_sites
    # from verified_vul_list import verified_list
    sinktype_pattern = re.compile('sinkType = (.*?),')
    content_pattern = re.compile('content = "(.*)",')
    consq = {'All':[0,0,set()]}
    consq_sub = {'All':0}
    prev_pos = 0
    TARGET_CRAWL = target_str + "crawl"
    # from check_ppExploit_results_additional import result_site_dict
    # check_site_list = result_site_dict['ppExploitFOUND'][1]
    # check_site_list = all_vul_websites.URL_vul_sites if mode=='URL' else all_vul_websites.vul_sites[mode]
    # os.chdir('/home/zfk/temp/cookie') #Documents/sanchecker/record_new_check_pp_pattern1_0to600kplus_crawl')
    os.chdir(CONFIG.THIS_ROOT_PATH + 'record_' + TARGET_CRAWL)
    vul_website = set()
    for fpath in tqdm(glob.iglob("record_*")):
        if True: #"record_" in fpath:
            inactive_flag = False
            with codecs.open(fpath, mode='r') as ff:
                cont = ff.readlines()
                z = fpath.split('_')
                site = '.'.join(z[1:len(z)-3])
                # if have_site_check_list and site not in check_site_list:
                #     continue
                # list_cont_to_search = []
                for num, line in enumerate(cont, 1):
                    if 'type = inactive' in line:
                        inactive_flag = True
                        continue
                    if 'targetString = (' in line:
                        prev_pos = num
                    # if 'content = "' in line:
                    #     list_cont_to_search.append(line)
                    elif 'sinkType = ' in line and inactive_flag:
                        inactive_flag = False
                        if any([each in line for each in CONFIG.SHOULD_EXCLUDE_SINKTYPE]):
                            # Those are sinks add by client-pp
                            continue
                        
                        if 'content = "' in cont[num - 3]:
                            contents_to_search = ''.join(cont[prev_pos + 1 : num - 2])
                        else:
                            contents_to_search = ''.join(cont[prev_pos + 1 : num - 3])
                        # contents_to_search = ''.join(list_cont_to_search)
                        # list_cont_to_search = []
                        if contents_to_search:
                            content_result = content_pattern.finditer(contents_to_search)
                        # if content_result:
                            content = ''.join([m.groups()[0] for m in content_result])
                            
                            sinktype_result = sinktype_pattern.search(line)
                            if sinktype_result:
                                sinkType = sinktype_result.group(1) #sinktype_result[1]
                            else:
                                raise ValueError('{} Cannot find sinkType! Line {} {}'.format(site, num, line))
                                
                            # judge, consequence, sinkType = judge_if_valid(content, sinkType, mode=mode, strict_check_mode=strict_check_mode)
                            consequence = sinkType
                            if True: # judge:
                                # found
                                # assert len(consequence) and len(sinkType)
                                # if have_verified_vul_list and consequence in ['xss', 'setTaintAttribute']:
                                    
                                #     if site not in verified_list:
                                #         continue
                                
                                if sinkType not in consq.keys():
                                    consq[sinkType] = [[], 0, set()]
                                consq[sinkType][1] += 1
                                consq[sinkType][2].add(site)
                                consq[sinkType][0].append('{} {} {}'.format(site, num, content))
                                consq['All'][1] += 1
                                consq['All'][2].add(site)

                                if consequence not in consq_sub.keys():
                                    consq_sub[consequence] = [0, set(), []]
                                consq_sub[consequence][0] += 1
                                consq_sub[consequence][1].add(site)
                                consq_sub[consequence][2].append('{} {} {}'.format(site, num, content))
                                consq_sub['All'] += 1

                                vul_website.add(site)
                                
                                inactive_flag = False
                        else:
                            raise ValueError('{} Cannot find content! Line {} {}'.format(site, num-3, cont[ num - 3]))
                            
    # should_verify = {}
    # consq['All'][0] = vul_weighted_sum(consq['All'][2])
    # for kk,vv in consq.items():
    #     if kk != 'All':
    #         consq[kk][0] = vul_weighted_sum(vv[2])
    #         if kk == 'html':
    #             exploit = [
    #                 "__proto__[98765]=<script>console.log(67890)</script>", 
    #                 "__proto__[98765]=<img/src/onerror%3dconsole.log(67890)>", 
    #                 "__proto__[98765]=<img src=1 onerror=console.log(67890)>", 
    #                 "__proto__[98765]=javascript:console.log(67890)//",
    #                 "constructor[prototype][98765]=<script>console.log(67890)</script>", 
    #                 "constructor[prototype][98765]=<img/src/onerror%3dconsole.log(67890)>", 
    #                 "constructor[prototype][98765]=<img src=1 onerror=console.log(67890)>", 
    #                 "constructor[prototype][98765]=javascript:console.log(67890)//"
    #             ]
    #         elif kk == 'javascript':
    #             exploit = [
    #                 "__proto__[98765]=console.log(67890)//", 
    #                 "constructor[prototype][98765]=console.log(67890)//",  
    #             ]
    #         elif kk == 'setTaintAttribute':
    #             exploit = [
    #                 "__proto__[98765]=data:,console.log(67890)//", 
    #                 "__proto__[src]=data:,console.log(67890)//", 
    #                 "__proto__[url]=data:,console.log(67890)//&__proto__[dataType]=script&__proto__[crossDomain]=", 
    #                 "__proto__[srcdoc][]=<script>console.log(67890)</script>", 
    #                 "__proto__[onload]=console.log(67890)//&__proto__[src]=1&__proto__[onerror]=console.log(67890)//", 
    #                 "constructor[prototype][98765]=data:,console.log(67890)//",  
    #                 "constructor[prototype][src]=data:,console.log(67890)//", 
    #                 "constructor[prototype][url]=data:,console.log(67890)//&constructor[prototype][dataType]=script&constructor[prototype][crossDomain]=", 
    #                 "constructor[prototype][srcdoc][]=<script>console.log(67890)</script>", 
    #                 "constructor[prototype][onload]=console.log(67890)//&constructor[prototype][src]=1&constructor[prototype][onerror]=console.log(67890)//"
    #             ]
    #         else:
    #             continue
    #         should_verify[kk] = [vv[2], exploit]
    # for kk,vv in consq_sub.items():
    #     if kk != 'All':
    #         consq_sub[kk][1] = vul_weighted_sum(vv[1])

    # # pprint(consq)
    # with open('/home/zfk/Documents/sanchecker/src/' + 'should_verify_new_vul.py', 'w') as fw:
    #     fw.write('should_verify=' + str(should_verify))
    with open('/home/zfk/Documents/sanchecker/src/Inactive/' + date.today().strftime("%m_%d_") + TARGET_CRAWL + '_consequence.log', 'w') as f1: #0614_consequence_cookie.log, 0609_consequence_0to600kplus.log
        f1.write(f"{vul_website}\n{str(len(vul_website))}\n")
        pprint(consq, f1)
        pprint(consq_sub, f1)
    print(vul_website, len(vul_website))


if __name__ == "__main__":
    check_def_flows(target_str='inactive_notemplate_phase2_partial_', mode='count_flow')
    # count_def_values("/home/zfk/Documents/sanchecker/src/undef_prop_dataset.json")
    # output_target_iter(get_finished_list("./logs/started.log"), "./logs/finished_list.log")