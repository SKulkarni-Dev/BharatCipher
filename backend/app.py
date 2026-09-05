from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.cases import cases
from backend.routes.investigations import investigations
from backend.routes.face_auth import face_auth

app = Flask(__name__)

CORS(app)

app.register_blueprint(cases)
app.register_blueprint(investigations)  
app.register_blueprint(face_auth)

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "SIH26151 backend is running."
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "service": "SIH26151",
        "status": "healthy"
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )