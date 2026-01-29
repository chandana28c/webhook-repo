from flask import Blueprint, json, request
from flask import request, jsonify
from datetime import datetime
from app.extensions import mongo
from datetime import timedelta



webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    event_data = None

    # PUSH EVENT
    if event_type == "push":
        event_data = {
            "author": payload["pusher"]["name"],
            "event": "push",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.fromisoformat(
                payload["head_commit"]["timestamp"].replace("Z", "+00:00")
            )
        }

    # PULL REQUEST & MERGE EVENT
    elif event_type == "pull_request":
        pr = payload["pull_request"]
        event_name = "merge" if pr["merged"] else "pull_request"

        event_data = {
            "author": pr["user"]["login"],
            "event": event_name,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.fromisoformat(
                pr["created_at"].replace("Z", "+00:00")
            )
        }

    # STORE IN DB
    if event_data:
        mongo.db.events.insert_one(event_data)

    return jsonify({"status": "ok"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():
    time_limit = datetime.utcnow() - timedelta(seconds=15)

    events = list(
        mongo.db.events.find(
            {"timestamp": {"$gte": time_limit}},
            {"_id": 0}
        ).sort("timestamp", -1)
    )

    return jsonify(events), 200


