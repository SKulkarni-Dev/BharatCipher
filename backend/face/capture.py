import cv2


def open_camera(camera_index=0):
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        raise RuntimeError("Could not open camera.")

    return camera


def detect_face(frame, detector):
    height, width = frame.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(frame)

    if faces is None:
        return None

    # Largest face
    faces = sorted(
        faces,
        key=lambda f: f[2] * f[3],
        reverse=True
    )

    return faces[0]