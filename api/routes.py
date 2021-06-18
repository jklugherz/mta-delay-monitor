from flask import jsonify

from api.app import app
from shared.db import get_is_delayed, get_total_time_line_exists, get_total_time_delayed


@app.route('/status/<line_id>', methods=["GET"])
def status(line_id: str):
    is_delayed = get_is_delayed(line_id)
    return jsonify(is_delayed)


@app.route('/uptime/<line_id>', methods=["GET"])
def uptime(line_id: str):
    total_time_exists = get_total_time_line_exists(line_id)
    total_time_delayed = get_total_time_delayed(line_id)
    up_time = 1 - (total_time_delayed / total_time_exists)
    return jsonify(up_time)
