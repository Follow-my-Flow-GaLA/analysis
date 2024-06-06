from pymongo import MongoClient
import csv
from time import time

client = MongoClient("mongodb://localhost:27017/")
phase1_db = client["phase1"]

start_time = time()

WEB_LIST_PATH = "/media/datak/inactive/sanchecker/src/tranco_LJ494.csv"
if __name__ == "__main__":
    num_of_sites = 0
    # extract domains from csv
    with open(WEB_LIST_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                site = row[1].replace('.', '_')
                if phase1_db["phase_info"].find_one({"_id": site}):
                    num_of_sites += 1
            if num_of_sites % 40000 == 0:
                print(f"Number of websites involved in phase 1: ", num_of_sites, "Time elapsed: ", time() - start_time)
    print(f"Total number of websites involved in phase 1: ", num_of_sites)