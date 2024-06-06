from concurrent.futures import ProcessPoolExecutor
import os, json, codecs, logging, csv
from tqdm import tqdm
from run_phase3_with_db import LogProcessor
import sys

# import phase3_config
config_path = '/media/datak/inactive/analysis/phase3'
sys.path.append(config_path)
from phase3_config import CONFIG

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
setup_logger("started", "./logs/started.log")
setup_logger("end", "./logs/end.log", include_time=False)
setup_logger("error", "./logs/error.log")
setup_logger("long_data", "./logs/long_data.log")
error_logger = logging.getLogger('error')
started_logger = logging.getLogger('started')
end_logger = logging.getLogger("end")
long_data_logger = logging.getLogger("long_data")

class ParallelLogProcessor:
    def __init__(self, base_dirs, progress_file, max_workers=20, slice_size=64, root="/media/datak/inactive/sanchecker/src"):
        self.base_dirs = base_dirs
        self.root = root
        self.progress_file = progress_file
        self.max_workers = max_workers
        self.slice_size = slice_size
        self.target_sites = self.extract_domains_from_csv() # if <condition> else <other_func>
        self.processed_sites = self.load_progress()
        
    def extract_domains_from_csv(self, file_path="tranco_LJ494.csv"):
        domains = []
        with open(os.path.join(self.root, file_path), newline='') as csvfile:
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

    def process_log_file(self, site_log_paths):
        for site, log_path in site_log_paths:
            started_logger.info("{} started ==> {}".format(site, log_path))
            try:
                processor = LogProcessor(site=site, log_path=log_path, error_logger=error_logger, long_data_logger=long_data_logger)
                processor.run()
                end_logger.info("{}".format(site))
            except KeyboardInterrupt:
                # User wants to quit. Abort. 
                break
            except Exception as e:
                error_logger.info("{} error!==> {} ".format(log_path, e))
                continue

    def generate_tasks(self, mode="sites"):
        tasks = []
        if mode == "sites":
            target_sites_set = set(self.target_sites)
            processed_sites_set = set(self.processed_sites)
            sites_to_process = target_sites_set - processed_sites_set
            for each_site in sites_to_process:
                for each_dir in self.base_dirs:
                    log_path = os.path.join(each_dir, each_site.replace(".", "_", 1) + "_log_file")
                    if os.path.isfile(log_path):
                        tasks.append((each_site, log_path))
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
    # Run `find logs -type f -name "*.log" -exec sh -c '> {}' \;` prior to this file if logs need to be cleaned
    # Run `sudo systemctl start mongod; source env/bin/activate` prior to this file 
    base_dirs = [CONFIG.PHASE3_LOG_PATH] 
    progress_file = "./logs/end.log"
    print("Starting initializing ParallelLogProcessor")
    parallel_processor = ParallelLogProcessor(base_dirs=base_dirs, progress_file=progress_file)
    print("Finished initializing ParallelLogProcessor")
    parallel_processor.process_all_sites()
