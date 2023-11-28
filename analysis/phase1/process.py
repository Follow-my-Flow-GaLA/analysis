#!python2

# Import necessary libraries and modules
from __future__ import print_function
import os, re, logging, codecs, hashlib
import multiprocessing
from config import CONFIG


# /home/zfk/Documents/sanchecker/src/song/handle_log.py
# Function to set up and configure a logger
def setup_logger(logger_name, log_file, level=logging.INFO):
    """
    This function sets up a logger for logging purposes.

    Parameters:
    - logger_name: Name of the logger.
    - log_file: Path to the log file where log messages will be written.
    - level: Log level (default is logging.INFO).
    """
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    
# Initialize loggers for various purposes
setup_logger("started", "./logs/started.log")
setup_logger("hash", "./logs/hash.log")
setup_logger("error", "./logs/error.log")
setup_logger("js_info", "./logs/js_info.log")
hash_logger = logging.getLogger('hash')
error_logger = logging.getLogger('error')
started_logger = logging.getLogger('started')
js_info_logger = logging.getLogger("js_info")

# Global set to store unique hashes
global_hash_set = set()

# Function to scan subdirectories and process log files
def scan_subdir(dir):
    """
    Scans the content of files within a given directory, extracts information related to JavaScript functions,
    and computes a hash for each function using SHA-256. It also logs relevant information into separate log files.

    Parameters:
    - dir: List of file names to be processed.
    """
    log_str = ""
    
    sub_hash_table = set()
    for each_file in dir:
        started_logger.info("{} started".format(each_file))
        try:
            with codecs.open(os.path.join(CONFIG.SCAN_ROOT_PATH, each_file), 'r', encoding='utf-8', errors='replace') as f0:
                line_count = 0
                hash_logger_info = ""
                js_info_logger_info = ""
                while True:
                    line_count += 1
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
                        
                hash_logger.info(hash_logger_info)
                js_info_logger.info(js_info_logger_info)
        except KeyboardInterrupt:
            break
        except Exception as e:
            error_logger.info("{} error!==> {} ".format(each_file, e))
            continue
        
    return sub_hash_table

# Function to generate a list of subdirectories to process
def gen_sub_dirs():
    """
    Generates a list of subdirectories to be processed by reading the "logs/started.log" file
    to skip sites that have already been processed.

    Returns:
    - sub_dirs: List of subdirectories to process.
    """
    started_dir = {}
    with codecs.open("logs/started.log", 'r', encoding='utf-8', errors='replace') as ff:
        lines = ff.readlines()
        end_num = len(lines) - 20 * 64 # get rid of the last (n_threads * slice_size) sites
        for num, line in enumerate(lines, 0):
            if num >= end_num:
                break
            fname = line.split()[-2]
            started_dir[fname] = True
    sub_dirs = []
    for f in os.listdir(CONFIG.SCAN_ROOT_PATH):
        if 'log_file' in f:
            if f not in started_dir: 
                sub_dirs.append(f)
    return sub_dirs
         
# Entry point for the script
if __name__ == "__main__":
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
    

