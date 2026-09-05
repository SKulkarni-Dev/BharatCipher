import cv2
import numpy as np
from pathlib import Path

from capture import open_camera, detect_face
from encoding import create_embedding


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data" / "face_data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DETECTOR = str(
    MODEL_DIR / "face_detection_yunet_2026may.onnx"
)

MODEL_RECOGNIZER = str(
    MODEL_DIR / "face_recognition_sface_2021dec.onnx"
)

OUTPUT_FILE = DATA_DIR / "investigator_face.npy"


# --------------------------------------------------
# Load models
# --------------------------------------------------

print("Loading face detector...")

detector = cv2.FaceDetectorYN.create(
    MODEL_DETECTOR,
    "",
    (320, 320)
)

print("Loading face recognizer...")

recognizer = cv2.FaceRecognizerSF.create(
    MODEL_RECOGNIZER,
    ""
)

print("Models loaded.")


# --------------------------------------------------
# Camera
# --------------------------------------------------

camera = open_camera()

print()
print("======================================")
print("   SIH26151 FACE REGISTRATION")
print("======================================")
print()
print("Look at the camera.")
print("Keep only ONE face visible.")
print()
print("We will capture 5 good samples.")
print("Press Q to cancel.")
print()


# --------------------------------------------------
# Capture embeddings
# --------------------------------------------------

embeddings = []

TARGET_SAMPLES = 5

while len(embeddings) < TARGET_SAMPLES:

    ret, frame = camera.read()

    if not ret:
        print("Could not read camera frame.")
        break

    face = detect_face(frame, detector)

    if face is not None:

        x, y, w, h = face[:4].astype(int)

        # Draw face box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Create embedding
        embedding = create_embedding(
            frame,
            face,
            recognizer
        )

        embeddings.append(
            embedding.flatten()
        )

        sample_number = len(embeddings)

        text = f"Captured: {sample_number}/{TARGET_SAMPLES}"

        cv2.putText(
            frame,
            text,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        print(
            f"Sample {sample_number}/{TARGET_SAMPLES} captured."
        )

        # Small delay so consecutive frames aren't identical
        cv2.waitKey(300)

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
        "SIH26151 - Face Registration",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        print("Registration cancelled.")
        camera.release()
        cv2.destroyAllWindows()
        exit()


# --------------------------------------------------
# Create stable template
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()

if len(embeddings) < TARGET_SAMPLES:

    print("❌ Not enough samples.")
    exit()


print()
print("Creating face template...")

embeddings = np.array(
    embeddings,
    dtype=np.float32
)

# Average all samples
template = np.mean(
    embeddings,
    axis=0
)

# Normalize
template = template / np.linalg.norm(template)

# Save
np.save(
    OUTPUT_FILE,
    template
)

print()
print("======================================")
print("✅ FACE REGISTRATION SUCCESSFUL")
print("======================================")
print()
print(f"Saved to:")
print(OUTPUT_FILE)
print()
print(f"Embedding shape: {template.shape}")