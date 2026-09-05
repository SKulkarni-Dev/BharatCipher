import cv2
import numpy as np


def create_embedding(frame, face, recognizer):
    """
    Detects/aligned face information is supplied through `face`.
    Returns an SFace embedding.
    """

    aligned_face = recognizer.alignCrop(frame, face)

    feature = recognizer.feature(aligned_face)

    # Normalize the embedding
    feature = feature / np.linalg.norm(feature)

    return feature