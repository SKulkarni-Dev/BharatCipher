import cv2
import numpy as np


def compare_faces(reference_feature, current_feature):
    """
    Compare two SFace embeddings using cosine similarity.

    Returns:
        float: cosine similarity score
    """

    reference_feature = np.asarray(
        reference_feature,
        dtype=np.float32
    )

    current_feature = np.asarray(
        current_feature,
        dtype=np.float32
    )

    # Normalize both embeddings
    reference_feature = reference_feature / np.linalg.norm(
        reference_feature
    )

    current_feature = current_feature / np.linalg.norm(
        current_feature
    )

    similarity = cv2.norm(
        reference_feature,
        current_feature,
        cv2.NORM_L2
    )

    # Use OpenCV's actual SFace comparison method instead.
    # This function is replaced below by direct cosine calculation.
    cosine_similarity = float(
        np.dot(
            reference_feature.flatten(),
            current_feature.flatten()
        )
    )

    return cosine_similarity


def is_match(similarity, threshold=0.363):
    """
    Determine whether the similarity passes the
    initial SFace threshold.

    NOTE:
    0.363 is only our starting threshold.
    We will calibrate it later using our own test data.
    """

    return similarity >= threshold