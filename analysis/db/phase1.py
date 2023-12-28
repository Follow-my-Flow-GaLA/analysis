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
    # check if the phase is 1
    if request_body['phase'] != "1":
        return Response('Phase is not 1', status=400)
    # check if the start_key is valid
    if request_body['start_key'] not in starting_keys:
        return Response('Invalid start key', status=400)

    # hash the func using sha256
    # the hash algorithm should match the one in the V8's runtime-object.cc
    sha256_hash = hashlib.sha256()
    sha256_hash.update(request_body["func"].encode('ascii'))
    hash_func = sha256_hash.hexdigest()

    msg = ""

    # add log to undef_prop_dataset
    code_hash_obj = db["phase1"]["undef_prop_dataset"].find_one({"_id": hash_func})
    if (code_hash_obj):
        if (request_body["key"] in code_hash_obj["key_value_dict"]):
            msg += "Key already exists in undef_prop_dataset (Key is " + request_body["key"] + ", Code hash is " + hash_func + "). \n"
        else:
            code_hash_obj["key_value_dict"][request_body["key"]] = request_body["row"] + ", " + request_body["col"]
            db["phase1"]["undef_prop_dataset"].update_one({"_id": hash_func}, {"$set": {"key_value_dict": code_hash_obj["key_value_dict"]}})
    else:
        db["phase1"]["undef_prop_dataset"].insert_one({
            "_id": hash_func,
            "key_value_dict": {
                request_body["key"]: request_body["row"] + ", " + request_body["col"]
            }
        })
    
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
                db["phase1"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}})
        else:
            site_obj["code_hash_dict"][hash_func] = {
                request_body["key"]: [
                    request_body["row"] + ", " + request_body["col"],
                    request_body["js"],
                    request_body["func_name"],
                    request_body["func"]
                ]
            }
            db["phase1"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}})
    else: 
        db["phase1"]["phase_info"].insert_one({
            "_id": request_body["site"],
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
        })

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
    if (code_hash):
        code_hash_obj = db["phase1"]["undef_prop_dataset"].find_one({"_id": code_hash})
        if (code_hash_obj):
            return code_hash_obj
        else:
            return "Code hash not found"
    else:
        return "Missing code hash"

@phase1_api.route('/websites', methods=['GET'])
def get_websites():
    websites = db["phase1"]["phase_info"].find()
    website_ids = [website["_id"] for website in websites]
    return jsonify({"website_ids": website_ids})

