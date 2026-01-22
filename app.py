from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

drones = {}

@app.route("/drones/register", methods=["POST"])
def register_drone():
    data = request.json
    drone_id = data.get("drone_id")

    if not drone_id:
        return jsonify({"error": "drone_id is required"}), 400

    drones[drone_id] = {
        "battery": 100,
        "status": "idle",
        "location": "unknown",
        "last_seen": str(datetime.utcnow())
    }

    return jsonify({"message": f"Drone {drone_id} registered successfully"}), 201


@app.route("/drones/heartbeat", methods=["POST"])
def drone_heartbeat():
    data = request.json
    drone_id = data.get("drone_id")

    if drone_id not in drones:
        return jsonify({"error": "Drone not registered"}), 404

    drones[drone_id]["battery"] = data.get("battery", drones[drone_id]["battery"])
    drones[drone_id]["status"] = data.get("status", drones[drone_id]["status"])
    drones[drone_id]["location"] = data.get("location", drones[drone_id]["location"])
    drones[drone_id]["last_seen"] = str(datetime.utcnow())

    return jsonify({"message": f"Heartbeat received from {drone_id}"}), 200


@app.route("/drones", methods=["GET"])
def list_drones():
    return jsonify(drones), 200


if __name__ == "__main__":
    app.run(debug=True)
