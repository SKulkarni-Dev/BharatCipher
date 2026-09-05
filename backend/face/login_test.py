import cv2
import numpy as np
from pathlib import Path

from capture import open_camera, detect_face
from encoding import create_embedding
from verify import compare_faces, is_match


# --------------------------------------------------
# Paths
# --------------------------------------------------

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


# --------------------------------------------------
# Check template
# --------------------------------------------------

if not FACE_TEMPLATE_PATH.exists():

    print("❌ No registered face found.")

    print(
        "Run register_face.py first."
    )

    exit()


# --------------------------------------------------
# Load models
# --------------------------------------------------

print("Loading YuNet...")

detector = cv2.FaceDetectorYN.create(
    DETECTOR_PATH,
    "",
    (320, 320)
)

print("Loading SFace...")

recognizer = cv2.FaceRecognizerSF.create(
    RECOGNIZER_PATH,
    ""
)

# --------------------------------------------------
# Load registered face
# --------------------------------------------------

reference_feature = np.load(
    FACE_TEMPLATE_PATH
)

reference_feature = reference_feature.reshape(
    1, -1
)

print("Registered face loaded.")

# --------------------------------------------------
# Camera
# --------------------------------------------------

camera = open_camera()

print()
print("======================================")
print("       SIH26151 FACE LOGIN")
print("======================================")
print()
print("Look at the camera.")
print("Press Q to quit.")
print()


# --------------------------------------------------
# Verification loop
# --------------------------------------------------

while True:

    ret, frame = camera.read()

    if not ret:

        print(
            "❌ Could not read camera frame."
        )

        break

    face = detect_face(
        frame,
        detector
    )

    if face is not None:

        x, y, w, h = face[:4].astype(int)

        # Create embedding
        current_feature = create_embedding(
            frame,
            face,
            recognizer
        )

        # Compare
        similarity = compare_faces(
            reference_feature,
            current_feature
        )

        matched = is_match(
            similarity
        )

        # --------------------------------------------------
        # Display result
        # --------------------------------------------------

        if matched:

            status = "ACCESS GRANTED"

        else:

            status = "ACCESS DENIED"

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            status,
            (x, max(y - 35, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Similarity: {similarity:.3f}",
            (x, max(y - 10, 55)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "NO FACE DETECTED",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "SIH26151 - Face Login",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()

print("Login test closed.")