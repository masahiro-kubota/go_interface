#!/usr/bin/env python3
# coding: utf-8

# Copyright 2021 eve autonomy inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from flask import abort, Flask, jsonify, request

# create api
api = Flask(__name__)

vehicle_id = "XXXXX"
lock_flg = 0
voice_flg = 0
active_schedule_exists = 0

# receive GET method
@api.route('/api/vehicle_status', methods=['GET'])
def get_vehicle_status():
    global vehicle_id
    q_id = request.args.get('vehicle_id', default=None, type=str)

    if q_id is None:
        abort(400, {'code': '400', 'message': 'Getting vehicle id failed.'})

    vehicle_id = q_id
    return jsonify({"result": {"vehicle_id": vehicle_id,
                               "lock_flg": lock_flg,
                               "voice_flg": voice_flg,
                               "active_schedule_exists": active_schedule_exists}})

# receive PATCH method
@api.route('/api/vehicle_status', methods=['PATCH'])
def patch_vehicle_status():
    global vehicle_id
    global lock_flg
    payload = json.loads(request.data)
    vehicle_id = payload.get("vehicle_id")
    lock_flg = payload.get("lock_flg")

    return jsonify(
        {"result": {"vehicle_id": vehicle_id, "lock_flg": lock_flg}})

# for debug:
# Here, overwrite `lock_flg`, `voice_flg`, and `active_schedule_exists` here.
@api.route('/api/vehicle_status_debug', methods=['PATCH'])
def patch_vehicle_status_debug():
    global voice_flg
    global lock_flg
    global active_schedule_exists
    payload = json.loads(request.data)
    voice_flg = payload.get("voice_flg")
    lock_flg = payload.get("lock_flg")
    active_schedule_exists = payload.get("active_schedule_exists")

    return jsonify({"result": {"lock_flg": lock_flg,
                               "voice_flg": voice_flg,
                               "active_schedule_exists": active_schedule_exists}})

# error check:
# Here, check the error of 401.
@api.errorhandler(401)
def error_handler(error):
    # error.code: HTTP status code
    return jsonify({'detail': error.description}), error.code


if __name__ == "__main__":
    api.run(debug=True, port=5000, threaded=True)
