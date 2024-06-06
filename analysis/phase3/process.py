#!python2
from __future__ import print_function
import os, re, logging, argparse, codecs, hashlib
import multiprocessing
# from tqdm import tqdm
from analysis.phase3.phase3_config import CONFIG
import time
# from helper_sha256 import sha256

# /home/zfk/Documents/sanchecker/src/song/handle_log.py
# Function to set up a logger
def setup_logger(logger_name, log_file, level=logging.INFO):
    """
    Set up a logger with the specified configuration.

    Parameters:
    - logger_name (str): The name of the logger.
    - log_file (str): The path to the log file.
    - level (int, optional): The log level (default is logging.INFO).
    """
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)

# Set up loggers
setup_logger("started", "./logs/started.log")
error_logger = logging.getLogger('error')
setup_logger("js_info", "./logs/js_info.log")
started_logger = logging.getLogger('started')
error_logger = logging.getLogger('error')
js_info_logger = logging.getLogger("js_info")

# Global set to store hash values
global_hash_set = set()

# Function to scan subdirectories for log files
def scan_subdir(dir):
    """
    Scan subdirectories for log files and process them.

    Parameters:
    - dir (list): A list of log file directories.
    - mode (str, optional): The mode of operation (default is "dev").
    """
    log_str = ""
    
    sub_hash_table = set()
    for each_file in dir:
        started_logger.info("{} started".format(each_file))
        try:
            with codecs.open(os.path.join(CONFIG.PHASE3_LOG_PATH, each_file), 'r', encoding='utf-8', errors='replace') as f0:
                line_count = 0
                hash_logger_info = ""
                js_info_logger_info = ""
                while True:
                    line_count += 1
                    # Get next line from file
                    line = f0.readline()
                    
                    # if line is empty, end of file is reached
                    if not line:
                        break
                    
                    if " KeyIs " in line: 
                        starting_key = line.split()[0]
                        log_str = line
                        while (line and starting_key+"End" not in line):
                            line = f0.readline()
                            log_str = log_str + line
                        matched_group = re.search(CONFIG.PARSE_LOG_REG, log_str)
                        if matched_group == None:
                            continue
                        key_name, func_name, js_name, row, col, func = \
                            matched_group.group(1), matched_group.group(2), matched_group.group(3), \
                                matched_group.group(4), matched_group.group(5), matched_group.group(6)
                        if CONFIG.SHOULD_EXCLUDE in key_name:
                            # Exclude "extensions::" (Chrome Builtins)
                            continue
                        if CONFIG.SHOULD_EXCLUDE in js_name:
                            continue
                        
                        # hash the func using sha256
                        # the hash algorithm should match the one in the V8's runtime-object.cc
                        sha256_hash = hashlib.sha256()
                        sha256_hash.update(func.encode('ascii'))
                        hash_func = sha256_hash.hexdigest()

                        if (hash_func, key_name, row) in sub_hash_table:
                            continue
                        sub_hash_table.add((hash_func, key_name, row))
                        
                        js_info_logger_info += "{}==>({}, {}, {}, {}, {}, {})"\
                            .format(each_file, hash_func, key_name, func_name, js_name, row, col)
                        js_info_logger_info += "\n"
                        
                js_info_logger.info(js_info_logger_info)
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_logger.info("{} error!==> {} ".format(each_file, e))
            continue
        
    return sub_hash_table

# Function to generate a list of subdirectories
def gen_sub_dirs():
    """
    Generate a list of subdirectories that contain log files.

    Returns:
    - sub_dirs (list): A list of subdirectories.
    """
    sub_dirs = []
    for f in os.listdir(CONFIG.PHASE3_LOG_PATH):
        if 'log_file' in f:
            sub_dirs.append(f)
    return sub_dirs

if __name__ == "__main__":
    #scan_subdir(["mcafee_com_log_file"])
    res = []
    n_threads = 20
    slice_size = 64 #int(len(sub_dirs) / n_threads) + 1
    sub_dirs = gen_sub_dirs()
    task_list = [sub_dirs[i:i + slice_size] for i in range(0, len(sub_dirs), slice_size)]
    print("Split into {} parts".format(len(task_list)))
    pool = multiprocessing.Pool(n_threads)
    zip(*pool.map(scan_subdir, task_list))
    pool.close()
    pool.join()


