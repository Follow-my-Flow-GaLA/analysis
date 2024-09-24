from pprint import pprint
from urllib.parse import urlparse, unquote_plus
from datetime import date
import json, ast, os, glob, codecs, re, logging, multiprocessing, pyperclip
from tqdm import tqdm

allow_no_load_time_set = set()

def get_show_time(fpath, time_write_file, recrawl_write_file, mode='add'):
    load_time_dict = {}
    site_to_recrawl = set()
    for each_file in tqdm(os.listdir(os.path.join("/media/datak/inactive/sanchecker/src", fpath))):
        if 'log_file' in each_file:
            with open(os.path.join("/media/datak/inactive/sanchecker/src", fpath, each_file), 'r') as fr:
                site = each_file.replace('_log_file', '').replace('_', '.', 1)
                for line in fr.readlines():
                    # if 'Codes for showing loading time in' in line:
                    try:
                        matchs = re.search(r'Loading time for (.*) is: (.*)", source:', line)
                        if matchs:
                            load_time = int(matchs.group(2))
                            load_time_dict[site] = load_time
                            break
                    except Exception as e:
                        continue
                else:
                    if mode == 'add':
                        allow_no_load_time_set.add(site)
                    elif mode == 'check' and site not in allow_no_load_time_set:
                        site_to_recrawl.add(site)
    if mode == 'add':
        print(fpath, len(allow_no_load_time_set))
    else:
        print(fpath, len(site_to_recrawl))
    with open(os.path.join("/media/datak/inactive/sanchecker/src", time_write_file), 'a') as fw:
        fw.write(str(load_time_dict)+',\n')
    if mode == 'check':
        with open(os.path.join("/media/datak/inactive/sanchecker/src", recrawl_write_file), 'w') as fwr:
            for idx, each_line in zip(range(1, len(site_to_recrawl)+1), site_to_recrawl):
                fwr.write(str(idx)+','+each_line+'\n')

if __name__ == "__main__": 
#    get_show_time('show_load_time_gala_1k_phase1_logs', 'load-time-gala-1k-phase1.py', '', mode='add')
    get_show_time('show_load_time_gala_1k_logs', 'load-time-gala-1k-phase2.py', '', mode='add')
#    get_show_time('show_load_time_Fastchrome_key1key2_1k_logs', 'load-time-Fastchrome-1k.py', 'recrawl-ppchrome-1k.txt', mode='check')
#    get_show_time('show_load_time_Fastndss18_1k_logs', 'load-time-ndss18-1k.py', 'recrawl-ndss18-1k.txt', mode='check')
#    get_show_time('show_load_time_gala_1k_logs', 'load-time-gala-1k.py', 'recrawl-gala-1k.txt', mode='check')

