# -*- coding: future_fstrings -*-
#!python3
from __future__ import print_function
import os, re, logging, argparse, codecs, json, glob, difflib
from tqdm import tqdm
from datetime import date
from pprint import pprint
from config import CONFIG
import time

# phase1_dict = {site: {codehash: {key: ["line,col", js_name]}}}
# Function to generate a phase1 dictionary
def gen_phase1_dict():
    """
    Generate a phase1 dictionary from a JSON file specified in the CONFIG.

    Returns:
    - phase1_dict (dict): The phase1 dictionary.
    """
    with open(CONFIG.PHASE1_INFO_JSON) as json_file:
        phase1_dict = json.load(json_file)
    return phase1_dict

# phase3_dict = {site: {codehash: {key: ["line,col", js_name]}}}
# Function to generate a phase3 dictionary
def gen_phase3_dict():
    """
    Generate a phase3 dictionary from a JSON file specified in the CONFIG.

    Returns:
    - phase3_dict (dict): The phase3 dictionary.
    """
    with open(CONFIG.PHASE3_INFO_JSON) as json_file:
        phase3_dict = json.load(json_file)
    return phase3_dict

# Function to find new undefined values in phase3 that are not in phase1
def find_new_undef(phase1_dict, phase3_dict, sites_not_found):
    """
    Find new undefined values in phase3 that are not present in phase1.

    Parameters:
    - phase1_dict (dict): The phase1 dictionary.
    - phase3_dict (dict): The phase3 dictionary.
    - sites_not_found (set): A set to store sites not found in phase1.

    Returns:
    - new_undef_dict (dict): A dictionary containing new undefined values in phase3.
    """
    new_undef_dict = {}
    for site, phase3_site_dict in phase3_dict.items():
        # site in phase3 should be included in phase1
        # if not included, then pass (CHECK PATH)
        if site not in phase1_dict:
            sites_not_found.add(site)
            continue
        phase1_site_dict = phase1_dict[site]
        for codehash, phase3_codehash_dict in phase3_site_dict.items():
            # add new codehash with all contents in it
            if codehash not in phase1_site_dict:
                if site not in new_undef_dict:
                    new_undef_dict[site] = {}
                new_undef_dict[site][codehash] = phase3_codehash_dict
                continue
            phase1_codehash_dict = phase1_site_dict[codehash]
            for key, value in phase3_codehash_dict.items():
                if key in phase1_codehash_dict and value[0] == phase1_codehash_dict[key][0] and value[1] == phase1_codehash_dict[key][1]:
                    continue
                # add key value to new_undef_dict
                if site not in new_undef_dict:
                    new_undef_dict[site] = {}
                if codehash not in new_undef_dict[site]:
                    new_undef_dict[site][codehash] = {}
                new_undef_dict[site][codehash][key] = value
    return new_undef_dict



if __name__ == "__main__":
    phase1_dict = gen_phase1_dict()
    phase3_dict = gen_phase3_dict()
    sites_not_found = set()
    new_undef_dict = find_new_undef(phase1_dict, phase3_dict, sites_not_found)
    print(new_undef_dict)
    print("len of new_undef_dict: ", len(new_undef_dict))
    print(sites_not_found)
    print("len of sites_not_found: ", len(sites_not_found))
