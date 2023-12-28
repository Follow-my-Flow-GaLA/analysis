from flask import Flask, Blueprint, request, Response
import hashlib 
from app import db

phase2_api = Blueprint('phase2', __name__)

@phase2_api.route('/', methods=['GET'])
def phase2():
    return "This is route for phase 2."

@phase2_api.route('/log', methods=['POST'])
def add_log():
    required_fields = ['phase', 'site', 'code_hash', 'key', 'value', 'row', 'col', 'sink_type']

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
    if request_body['phase'] != "2":
        return Response('Phase is not 2', status=400)
    
    msg = ""
    
    # add defined value to def_val_dataset
    code_hash_obj = db["phase2"]["def_val_dataset"].find_one({"_id": request_body["code_hash"]})
    if (code_hash_obj):
        if (request_body["key"] in code_hash_obj["key_value_dict"]):
            key_value_dict = code_hash_obj["key_value_dict"]
            # if two values are available, leave the one with shorter length
            if (len(key_value_dict[request_body["key"]]["value"]) > len(request_body["value"])):
                key_value_dict[request_body["key"]] = {
                    "value": request_body["value"],
                    "sink_type": request_body["sink_type"],
                    "site": request_body["site"]
                }
                db["phase2"]["def_val_dataset"].update_one({"_id": request_body["code_hash"]}, {"$set": {"key_value_dict": key_value_dict}})
        else:
            db["phase2"]["def_val_dataset"].update_one({"_id": request_body["code_hash"]}, {"$set": {"key_value_dict": {request_body["key"]: {"value": request_body["value"], "sink_type": request_body["sink_type"], "site": request_body["site"]}}}})
    else:
        db["phase2"]["def_val_dataset"].insert_one({
            "_id": request_body["code_hash"],
            "key_value_dict": {
                request_body["key"]: {
                    "value": request_body["value"],
                    "sink_type": request_body["sink_type"],
                    "site": request_body["site"], 
                }
            }
        })

    # add log to phase_info
    site_obj = db["phase2"]["phase_info"].find_one({"_id": request_body["site"]})
    if (site_obj):
        if (request_body["code_hash"] in site_obj["code_hash_dict"]):
            if (request_body["key"] in site_obj["code_hash_dict"][request_body["code_hash"]]):
                msg += "Key already exists in phase_info (Key is " + request_body["key"] + ", Code hash is " + request_body["code_hash"] + ", Site is " + request_body["site"] + "). \n"
            else:
                site_obj["code_hash_dict"][request_body["code_hash"]][request_body["key"]] = {
                    "value": request_body["value"],
                    "row": request_body["row"],
                    "col": request_body["col"],
                    "sink_type": request_body["sink_type"]
                }
                db["phase2"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}})
        else:
            site_obj["code_hash_dict"][request_body["code_hash"]] = {
                request_body["key"]: {
                    "value": request_body["value"],
                    "row": request_body["row"],
                    "col": request_body["col"],
                    "sink_type": request_body["sink_type"]
                }
            }
            db["phase2"]["phase_info"].update_one({"_id": request_body["site"]}, {"$set": {"code_hash_dict": site_obj["code_hash_dict"]}})
    else:
        db["phase2"]["phase_info"].insert_one({
            "_id": request_body["site"],
            "code_hash_dict": {
                request_body["code_hash"]: {
                    request_body["key"]: {
                        "value": request_body["value"],
                        "row": request_body["row"],
                        "col": request_body["col"],
                        "sink_type": request_body["sink_type"]
                    }
                }
            }
        })
        
    return msg

@phase2_api.route('/phase_info', methods=['GET'])
def get_phase_info():
    site = request.args.get('site')
    if (site):
        site_obj = db["phase2"]["phase_info"].find_one({"_id": site})
        if (site_obj):
            return site_obj
        else:
            return "Site not found"
    else:
        return "Missing site"

@phase2_api.route('/def_val_dataset', methods=['GET'])
def get_def_val_dataset():
    code_hash = request.args.get('code_hash')
    if (code_hash):
        code_hash_obj = db["phase2"]["def_val_dataset"].find_one({"_id": code_hash})
        if (code_hash_obj):
            return code_hash_obj
        else:
            return "Code hash not found"
    else:
        return "Missing code hash"