from flask import Blueprint, request, jsonify

from backend.database.sqlite_db import (
    create_case,
    get_cases
)


cases = Blueprint("cases", __name__)


@cases.route("/cases", methods=["POST"])
def create_case_route():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required."
        }), 400

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({
            "success": False,
            "message": "Case title is required."
        }), 400

    try:
        case = create_case(
            title=title,
            description=description
        )

        return jsonify({
            "success": True,
            "message": "Case created successfully.",
            "case": case
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Case could not be created.",
            "error": str(e)
        }), 500


@cases.route("/cases", methods=["GET"])
def get_cases_route():

    try:
        result = get_cases()

        return jsonify({
            "success": True,
            "count": len(result),
            "cases": result
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Could not retrieve cases.",
            "error": str(e)
        }), 500