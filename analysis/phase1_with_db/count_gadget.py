import requests
import time

API_URL = 'http://127.0.0.1:5000/api/phase1/'

"""
    codehash_dict = {
        "codehash1": {
            "occurance": 1,
            "keys": {
                "key1": 1,
                "key2": 1
            
            }
        }
    }
"""

def add_to_codehash(codehash_dict, website):
    try:
        response = requests.get(API_URL + "phase_info?site=" + website)
        response.raise_for_status()  # Raises an HTTPError for bad HTTP response
        site_info = response.json()
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return
    except ValueError:
        print("Error decoding JSON")
        return

    for code_hash, hash_info in site_info.get("code_hash_dict", {}).items():
        if code_hash not in codehash_dict:
            # If the code hash does not exist, initialize it with the hash info
            codehash_dict[code_hash] = {
                "occurance": 1,
                "keys": {}
            }
            for key in hash_info:
                codehash_dict[code_hash]["keys"][key] = 1
        else:
            # If the code hash exists, update its occurrence and keys
            codehash_dict[code_hash]["occurance"] += 1
            for key in hash_info:
                if key in codehash_dict[code_hash]["keys"]:
                    codehash_dict[code_hash]["keys"][key] += 1
                else:
                    codehash_dict[code_hash]["keys"][key] = 1


def summarize(websites, codehash_dict):
    print("Total Websites: ", len(websites))
    print("Total Code Hashes: ", len(codehash_dict))
    # find the most common code hash
    max_occurance = 0
    max_codehash = ""
    for codehash in codehash_dict:
        if codehash_dict[codehash]["occurance"] > max_occurance:
            max_occurance = codehash_dict[codehash]["occurance"]
            max_codehash = codehash
    print("Most Common Code Hash: ", max_codehash)
    print("Occurance: ", max_occurance)
    # find the totoal number of keys
    total_keys = 0
    for codehash in codehash_dict:
        total_keys += len(codehash_dict[codehash]["keys"])
    print("Total Keys: ", total_keys)


if __name__ == '__main__':
    print("Phase 1 Gadget")
    
    response = requests.get(API_URL)

    codehash_dict = {}

    # Get all websites
    response = requests.get(API_URL + "websites")
    websites = response.json()
    for website in websites:
        add_to_codehash(codehash_dict, website)
    
    summarize(websites, codehash_dict)