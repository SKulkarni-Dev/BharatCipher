import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

detector_path = str(
    MODEL_DIR / "face_detection_yunet_2026may.onnx"
)

detector = cv2.FaceDetectorYN.create(
    detector_path,
    "",
    (320, 320)
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open camera.")
    exit()

print("Camera started.")
print("Press Q to quit.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("❌ Could not read camera frame.")
        break

    height, width = frame.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(frame)

    if faces is not None:
        for face in faces:
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "FACE DETECTED",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow("SIH26151 - Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()