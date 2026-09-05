const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

export async function verifyFaceId(imageBlob) {
  if (!imageBlob) {
    return {
      verified: false,
      reason: 'No camera image was captured.',
    };
  }

  try {
    const formData = new FormData();
    formData.append('image', imageBlob, 'face.jpg');

    const response = await fetch(`${API_BASE_URL}/face/verify`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        verified: false,
        reason: data.message || 'Face-ID verification failed.',
      };
    }

    if (data.authenticated) {
      return {
        verified: true,
        investigator: {
          id: 'INVESTIGATOR-01',
          name: 'Investigator',
          role: 'Analyst',
        },
        similarity: data.similarity,
      };
    }

    return {
      verified: false,
      reason: data.message || 'Face verification failed.',
    };
  } catch (error) {
    console.error('Face-ID request failed:', error);

    return {
      verified: false,
      reason:
        'Unable to connect to the Face-ID service. Make sure the backend is running.',
    };
  }
}

/** Local-only development fallback. */
export async function devLogin(username) {
  return {
    verified: true,
    investigator: {
      id: 'DEV-LOCAL',
      name: username || 'dev.investigator',
      role: 'Analyst (Local Dev Fallback)',
    },
  };
}