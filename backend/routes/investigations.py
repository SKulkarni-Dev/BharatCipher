from pathlib import Path

from flask import Blueprint, request, jsonify

from backend.database.sqlite_db import (
    save_investigation,
    get_investigations,
    get_investigation
)

from intelligence.investigation_engine import investigate_dataset


investigations = Blueprint("investigations", __name__)

# Datasets must live inside the project directory. This prevents a
# caller from pointing dataset_path at arbitrary files on disk
# (e.g. "/etc/passwd.json" or "../../secrets.json").
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@investigations.route("/investigations", methods=["POST"])
def create_investigation():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400

    dataset_path = data.get("dataset_path")

    if not dataset_path or not isinstance(dataset_path, str):
        return jsonify({
            "success": False,
            "message": "dataset_path is required."
        }), 400

    resolved_path = (PROJECT_ROOT / dataset_path).resolve()

    if PROJECT_ROOT not in resolved_path.parents and resolved_path != PROJECT_ROOT:
        return jsonify({
            "success": False,
            "message": "dataset_path must be inside the project directory."
        }), 400

    try:
        result = investigate_dataset(str(resolved_path))

        investigation_id = save_investigation(result)

        if not investigation_id:
            return jsonify({
                "success": False,
                "message": "Investigation could not be saved."
            }), 500

        return jsonify({
            "success": True,
            "message": "Investigation completed and saved successfully.",
            "investigation_id": investigation_id
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Investigation failed.",
            "error": str(e)
        }), 500


@investigations.route("/investigations", methods=["GET"])
def list_investigations():
    try:
        investigations_data = get_investigations()

        return jsonify({
            "success": True,
            "count": len(investigations_data),
            "investigations": investigations_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Could not retrieve investigations.",
            "error": str(e)
        }), 500


@investigations.route("/investigations/<investigation_id>", methods=["GET"])
def get_investigation_by_id(investigation_id):
    try:
        investigation = get_investigation(investigation_id)

        if investigation is None:
            return jsonify({
                "success": False,
                "message": "Investigation not found."
            }), 404

        return jsonify({
            "success": True,
            "investigation": investigation
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Could not retrieve investigation.",
            "error": str(e)
        }), 500