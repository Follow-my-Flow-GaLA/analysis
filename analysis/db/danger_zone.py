from flask import Flask, Blueprint, request, Response, jsonify
import hashlib 
from app import db

danger_zone_api = Blueprint('danger_zone', __name__)

# This deletes all data from all collections in phase1
# Write parameter confirm_delete == "Confirm Delete Phase1" to confirm the deletion
@danger_zone_api.route('/phase1', methods=['delete'])
def delete_phase1():
    confirm_msg = request.args.get('confirm_delete')
    if confirm_msg == "Confirm Delete Phase1":
        db["phase1"]["undef_prop_dataset"].delete_many({})
        db["phase1"]["phase_info"].delete_many({})
        return Response('All data from phase1 has been deleted', status=200)
    else:
        return Response('Confirm Delete header not found', status=400)

# This deletes all data from all collections in phase2
# Write parameter confirm_delete == "Confirm Delete Phase2" to confirm the deletion
@danger_zone_api.route('/phase2', methods=['delete'])
def delete_phase2():
    confirm_msg = request.args.get('confirm_delete')
    if confirm_msg == "Confirm Delete Phase2":
        db["phase2"]["phase_info"].delete_many({})
        db["phase2"]["def_val_dataset"].delete_many({})
        return Response('All data from phase2 has been deleted', status=200)
    else:
        return Response('Confirm Delete header not found', status=400)

# This deletes all data from all collections in phase3
# Write parameter confirm_delete == "Confirm Delete Phase3" to confirm the deletion
@danger_zone_api.route('/phase3', methods=['delete'])
def delete_phase3():
    confirm_msg = request.args.get('confirm_delete')
    if confirm_msg == "Confirm Delete Phase3":
        db["phase3"]["phase_info"].delete_many({})
        db["phase3"]["payload"].delete_many({})
        db["phase3"]["undef_prop_dataset"].delete_many({})
        db["phase3"]["data_to_change"].delete_many({})
        return Response('All data from phase3 has been deleted', status=200)
    else:
        return Response('Confirm Delete header not found', status=400)
    