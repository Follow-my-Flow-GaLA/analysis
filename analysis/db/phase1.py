from flask import Flask, Blueprint, request, Response, jsonify
import hashlib 
from app import db

phase1_api = Blueprint('phase1', __name__)

@phase1_api.route('/', methods=['GET'])
def phase1():
    return "This is route for phase 1."

@phase1_api.route('/undefined_value', methods=['POST'])
def add_undefined_value():
    required_fields = ['phase', 'start_key', 'site', 'key', 'func_name', 'js', 'row', 'col', 'func']
    starting_keys = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC"]

    # check if the request is in json format
    if not request.json:
        return Response('Data not in json format', status=400)
    # get the request body
    request_body = request.get_json()
    # check if the request body contains all the required fields
    for field in required_fields:
        if field not in request_body:
            return Response('Missing field: ' + field, status=400)
    
    # create and open a log file
    # log_file = open("log/" + request_body['site'].replace(".", "_") + "_log.txt", "a")

    # check if the phase is 1
    if request_body['phase'] != "1":
        # log_file.write(request_body['site'], ": Phase is not 1\n")
        return Response('Phase is not 1', status=400)
    # check if the start_key is valid
    if request_body['start_key'] not in starting_keys:
        # log_file.write(request_body['site'], ": Invalid start key\n")
        return Response('Invalid start key', status=400)

    # if code_hash is provided, use it, otherwise hash the func
    if "code_hash" in request_body:
        hash_func = request_body["code_hash"]
    else:
        # hash the func using sha256
        # the hash algorithm and the encoding should match the one in the V8's runtime-object.cc and objects.cc
        try:
            sha256_hash = hashlib.sha256()
            sha256_hash.update(request_body["func"].encode('utf-8'))
            hash_func = sha256_hash.hexdigest()
        except:
            # log_file.write(request_body['site'], ": Hashing failed\n")
            return Response('Hashing failed', status=500)
        
        # change . to %2E; change $ to %24 

    request_body["site"] = request_body["site"].replace(".", "_")
    request_body["key"] = request_body["key"].replace(".", "\\2E").replace("$", "\\24")
    request_body["func_name"] = request_body["func_name"].replace(".", "\\2E").replace("$", "\\24")
    request_body["js"] = request_body["js"].replace(".", "\\2E").replace("$", "\\24")
    request_body["func"] = request_body["func"].replace(".", "\\2E").replace("$", "\\24")

    msg = ""

    # add log to undef_prop_dataset
    code_hash_obj = db["phase1"]["undef_prop_dataset"].find_one({"_id": hash_func})
    row_col_str = request_body["row"] + ", " + request_body["col"]
    if (code_hash_obj):
        if (request_body["key"] in code_hash_obj["key_value_dict"]):
            # check if row and col are in the array
            row_col_list = code_hash_obj["key_value_dict"][request_body["key"]]
            if row_col_str in row_col_list:
                msg += "Row and col already exists in undef_prop_dataset (Key is " + request_body["key"] + ", Code hash is " + hash_func + "). \n"
            else:
                row_col_list.append(row_col_str)
                code_hash_obj["key_value_dict"][request_body["key"]] = row_col_list
                db["phase1"]["undef_prop_dataset"].update_one({"_id": hash_func}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}}, upsert=True)
        else:
            code_hash_obj["key_value_dict"][request_body["key"]] = [row_col_str]
            db["phase1"]["undef_prop_dataset"].update_one({"_id": hash_func}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}}, upsert=True)
    else:
        db["phase1"]["undef_prop_dataset"].update_one(
            {"_id": hash_func},
            {"$set": {
                "key_value_dict": {
                    request_body["key"]: [row_col_str]
                }
            }}
        , upsert=True)
    
    # add log to phase_info
    site_obj = db["phase1"]["phase_info"].find_one({"_id": request_body["site"]})
    if (site_obj):
        if (hash_func in site_obj["code_hash_dict"]):
            if (request_body["key"] in site_obj["code_hash_dict"][hash_func]):
                msg += "Key already exists in phase_info (Key is " + request_body["key"] + ", Code hash is " + hash_func + "Site is " + request_body["site"] + "). \n"
            else:
                site_obj["code_hash_dict"][hash_func][request_body["key"]] = [
                    request_body["row"] + ", " + request_body["col"],
                    request_body["js"],
                    request_body["func_name"],
                    request_body["func"]
                ]
                db["phase1"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}}, upsert=True)
        else:
            site_obj["code_hash_dict"][hash_func] = {
                request_body["key"]: [
                    request_body["row"] + ", " + request_body["col"],
                    request_body["js"],
                    request_body["func_name"],
                    request_body["func"]
                ]
            }
            db["phase1"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}}, upsert=True)
    else: 
        db["phase1"]["phase_info"].update_one(
            {"_id": request_body["site"]},
            {"$set": {
                "code_hash_dict": {
                    hash_func: {
                        request_body["key"]: [
                            request_body["row"] + ", " + request_body["col"],
                            request_body["js"],
                            request_body["func_name"],
                            request_body["func"]
                        ]
                    }
                }
            }}
        , upsert=True)

    # write msg to log file and close the log file
    # log_file.write(msg)
    # log_file.close()
    return msg

@phase1_api.route('/phase_info', methods=['GET'])
def get_phase_info():
    site = request.args.get('site')
    if (site):
        site_obj = db["phase1"]["phase_info"].find_one({"_id": site})
        if (site_obj):
            return site_obj
        else:
            return "Site not found"
    else:
        return "Missing site"

@phase1_api.route('/undef_prop_dataset', methods=['GET'])
def get_undef_prop_dataset():
    code_hash = request.args.get('code_hash')
    key = request.args.get('key').replace(".", "\\2E").replace("$", "\\24")
    row_col = request.args.get('row_col')
    
    # check if the required args are provided
    if not code_hash or not key or not row_col:
        return Response('Missing args', status=400)

    code_hash_obj = db["phase1"]["undef_prop_dataset"].find_one({"_id": code_hash})
    
    # check if the undefined property exists
    if not code_hash_obj:
        return Response('Code hash not found', status=404)
    if not key in code_hash_obj["key_dict"]:
        return Response('Key not found', status=404)
    
    # check if the row and col exists with the column number blurred (+- 5)
    row_col_list = code_hash_obj["key_dict"][key]
    row_col = row_col.split(",") # received from V8, format is ","
    for row_col_item in list(map(lambda x: x.split(", "), row_col_list)): # retrieved from db, format is ", "
        if row_col[0] == row_col_item[0] and (abs(int(row_col[1]) - int(row_col_item[1])) <= 5):
            return Response('Undefined property found', status=200)
    
    return Response('Row_Col not found', status=404)

@phase1_api.route('/websites', methods=['GET'])
def get_websites():
    websites = db["phase1"]["phase_info"].distinct("_id")
    return jsonify(websites)
