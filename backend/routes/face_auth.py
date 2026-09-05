import cv2
import numpy as np

from flask import Blueprint, request, jsonify
from pathlib import Path

from backend.face.encoding import create_embedding
from backend.face.verify import compare_faces, is_match 


face_auth = Blueprint("face_auth", __name__)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data" / "face_data"

DETECTOR_PATH = str(
    MODEL_DIR / "face_detection_yunet_2026may.onnx"
)

RECOGNIZER_PATH = str(
    MODEL_DIR / "face_recognition_sface_2021dec.onnx"
)

FACE_TEMPLATE_PATH = (
    DATA_DIR / "investigator_face.npy"
)


# Load models once when the backend starts
detector = cv2.FaceDetectorYN.create(
    DETECTOR_PATH,
    "",
    (320, 320)
)

recognizer = cv2.FaceRecognizerSF.create(
    RECOGNIZER_PATH,
    ""
)


@face_auth.route("/face/verify", methods=["POST"])
def verify_face():

    try:

        # ------------------------------------------
        # Check image
        # ------------------------------------------

        if "image" not in request.files:

            return jsonify({
                "success": False,
                "authenticated": False,
                "message": "No image received."
            }), 400

        image_file = request.files["image"]

        image_bytes = image_file.read()

        image_array = np.frombuffer(
            image_bytes,
            np.uint8
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:

            return jsonify({
                "success": False,
                "authenticated": False,
                "message": "Invalid image."
            }), 400

        # ------------------------------------------
        # Detect face
        # ------------------------------------------

        height, width = frame.shape[:2]

        detector.setInputSize(
            (width, height)
        )

        _, faces = detector.detect(frame)

        if faces is None or len(faces) == 0:

            return jsonify({
                "success": True,
                "authenticated": False,
                "message": "No face detected."
            })

        # ------------------------------------------
        # Use largest face
        # ------------------------------------------

        faces = sorted(
            faces,
            key=lambda f: f[2] * f[3],
            reverse=True
        )

        face = faces[0]

        # ------------------------------------------
        # Create embedding
        # ------------------------------------------

        current_feature = create_embedding(
            frame,
            face,
            recognizer
        )

        # ------------------------------------------
        # Load registered template
        # ------------------------------------------

        if not FACE_TEMPLATE_PATH.exists():

            return jsonify({
                "success": False,
                "authenticated": False,
                "message": "No registered investigator."
            }), 500

        reference_feature = np.load(
            FACE_TEMPLATE_PATH
        )

        reference_feature = reference_feature.reshape(
            1, -1
        )

        # ------------------------------------------
        # Compare
        # ------------------------------------------

        similarity = compare_faces(
            reference_feature,
            current_feature
        )

        authenticated = is_match(
            similarity
        )

        # ------------------------------------------
        # Response
        # ------------------------------------------

        if authenticated:

            message = "Face verified successfully."

        else:

            message = "Face verification failed."

        return jsonify({

            "success": True,

            "authenticated": authenticated,

            "similarity": round(
                float(similarity),
                4
            ),

            "message": message

        })

    except Exception as e:

        print("Face verification error:", e)

        return jsonify({

            "success": False,

            "authenticated": False,

            "message": "Face verification failed."

        }), 500