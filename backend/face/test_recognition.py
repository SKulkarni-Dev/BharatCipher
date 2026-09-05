import cv2
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

detector_path = str(
    MODEL_DIR / "face_detection_yunet_2026may.onnx"
)

recognizer_path = str(
    MODEL_DIR / "face_recognition_sface_2021dec.onnx"
)

# --------------------------------------------------
# Load models
# --------------------------------------------------

print("Loading YuNet...")

detector = cv2.FaceDetectorYN.create(
    detector_path,
    "",
    (320, 320)
)

print("Loading SFace...")

recognizer = cv2.FaceRecognizerSF.create(
    recognizer_path,
    ""
)

print("Models loaded successfully.")

# --------------------------------------------------
# Camera
# --------------------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open camera.")
    exit()

print("Camera started.")
print("Look at the camera.")
print("Press Q to quit.")
print("Press R to reset the reference face.")

# --------------------------------------------------
# Reference embedding
# --------------------------------------------------

reference_feature = None

# --------------------------------------------------
# Main loop
# --------------------------------------------------

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read camera frame.")
        break

    height, width = frame.shape[:2]

    detector.setInputSize((width, height))

    # Detect faces
    _, faces = detector.detect(frame)

    if faces is not None:

        # Use the largest detected face
        faces = sorted(
            faces,
            key=lambda f: f[2] * f[3],
            reverse=True
        )

        face = faces[0]

        x, y, w, h = face[:4].astype(int)

        # --------------------------------------------------
        # Align face for SFace
        # --------------------------------------------------

        aligned_face = recognizer.alignCrop(
            frame,
            face
        )

        # --------------------------------------------------
        # Generate embedding
        # --------------------------------------------------

        feature = recognizer.feature(
            aligned_face
        )

        # --------------------------------------------------
        # First face becomes reference
        # --------------------------------------------------

        if reference_feature is None:

            reference_feature = feature.copy()

            print("✅ Reference face captured.")

        # --------------------------------------------------
        # Compare current face with reference
        # --------------------------------------------------

        similarity = recognizer.match(
            reference_feature,
            feature,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        # --------------------------------------------------
        # Display
        # --------------------------------------------------

        if similarity >= 0.363:

            status = "MATCH"
            text = f"MATCH | Similarity: {similarity:.3f}"

        else:

            status = "NO MATCH"
            text = f"NO MATCH | Similarity: {similarity:.3f}"

        # Face box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Status
        cv2.putText(
            frame,
            text,
            (x, max(y - 15, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
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
        "SIH26151 - SFace Recognition Test",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord("q"):
        break

    # Reset reference
    if key == ord("r"):
        reference_feature = None
        print("🔄 Reference face reset.")

# --------------------------------------------------
# Cleanup
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()

print("Camera closed.")