import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ScanFace,
  ShieldHalf,
  TerminalSquare,
  AlertCircle,
  Camera,
  X,
} from 'lucide-react';

import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { verifyFaceId, devLogin } from '@/api/auth';
import { useAuth } from '@/hooks/useAuth';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraOpen, setCameraOpen] = useState(false);
  const [faceIdNotice, setFaceIdNotice] = useState(null);
  const [scanning, setScanning] = useState(false);

  const [devUsername, setDevUsername] = useState('');
  const [showDevFallback, setShowDevFallback] = useState(false);

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraOpen(false);
  }

  async function openCamera() {
    setFaceIdNotice(null);

    if (!navigator.mediaDevices?.getUserMedia) {
      setFaceIdNotice('Camera access is not supported by this browser.');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user',
          width: { ideal: 640 },
          height: { ideal: 480 },
        },
        audio: false,
      });

      streamRef.current = stream;
      setCameraOpen(true);

      // Wait for the video element to render.
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play().catch(() => {});
        }
      }, 50);
    } catch (error) {
      console.error('Camera access failed:', error);

      setFaceIdNotice(
        'Camera access was denied or is unavailable. Please allow camera access and try again.'
      );
    }
  }

  async function handleFaceScan() {
    if (!cameraOpen) {
      await openCamera();
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) {
      setFaceIdNotice('Camera is not ready yet. Please try again.');
      return;
    }

    if (video.readyState < 2) {
      setFaceIdNotice('Camera is still starting. Please wait a moment.');
      return;
    }

    setScanning(true);
    setFaceIdNotice(null);

    try {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const context = canvas.getContext('2d');

      context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
      );

      const imageBlob = await new Promise((resolve) => {
        canvas.toBlob(resolve, 'image/jpeg', 0.9);
      });

      if (!imageBlob) {
        setFaceIdNotice('Unable to capture camera image.');
        return;
      }

      const result = await verifyFaceId(imageBlob);

      if (result.verified) {
        stopCamera();

        login(result.investigator);
        navigate('/');
      } else {
        setFaceIdNotice(
          result.reason || 'Face-ID verification failed.'
        );
      }
    } catch (error) {
      console.error('Face scan failed:', error);
      setFaceIdNotice('Face-ID verification failed.');
    } finally {
      setScanning(false);
    }
  }

  async function handleDevLogin(e) {
    e.preventDefault();

    const result = await devLogin(devUsername);

    login(result.investigator);
    navigate('/');
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[var(--color-base)] px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-[color-mix(in_srgb,var(--color-accent)_18%,transparent)] text-[var(--color-accent)]">
            <ShieldHalf size={26} strokeWidth={2.25} />
          </div>

          <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-[var(--color-ink-faint)]">
            SIH26151
          </p>

          <h1 className="mt-2 font-display text-xl font-semibold text-[var(--color-ink)]">
            Dark Web Threat Actor
            <br />
            De-Anonymization Platform
          </h1>
        </div>

        <Card className="p-6">
          <div className="mb-5 text-center">
            <p className="font-mono text-[11px] uppercase tracking-wider text-[var(--color-ink-faint)]">
              Authenticate Investigator
            </p>
          </div>

          <div className="relative mx-auto flex h-40 w-40 items-center justify-center overflow-hidden rounded-full border-2 border-[var(--color-border)]">
            {cameraOpen ? (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="h-full w-full object-cover"
              />
            ) : (
              <ScanFace
                size={44}
                className="text-[var(--color-ink-faint)]"
              />
            )}
          </div>

          <canvas ref={canvasRef} className="hidden" />

          {faceIdNotice && (
            <p className="mt-3 flex items-start gap-1.5 text-center text-[11.5px] text-[var(--color-warning)]">
              <AlertCircle
                size={13}
                className="mt-0.5 shrink-0"
              />

              <span>{faceIdNotice}</span>
            </p>
          )}

          <Button
            className="mt-5 w-full"
            onClick={handleFaceScan}
            icon={cameraOpen ? ScanFace : Camera}
            disabled={scanning}
          >
            {scanning
              ? 'Verifying Face...'
              : cameraOpen
                ? 'Capture & Verify'
                : 'Scan Face'}
          </Button>

          {cameraOpen && !scanning && (
            <button
              type="button"
              onClick={stopCamera}
              className="mt-2 flex w-full items-center justify-center gap-2 py-2 font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)] hover:text-[var(--color-ink)]"
            >
              <X size={13} />
              Cancel Camera
            </button>
          )}

          <div className="mt-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-[var(--color-border)]" />

            <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--color-ink-faint)]">
              or
            </span>

            <div className="h-px flex-1 bg-[var(--color-border)]" />
          </div>

          {!showDevFallback ? (
            <button
              onClick={() => setShowDevFallback(true)}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-md border border-dashed border-[var(--color-border)] py-2 font-mono text-[11px] uppercase tracking-wider text-[var(--color-ink-muted)] hover:text-[var(--color-ink)]"
            >
              <TerminalSquare size={14} />
              Development fallback login
            </button>
          ) : (
            <form
              onSubmit={handleDevLogin}
              className="mt-4 space-y-2"
            >
              <input
                type="text"
                placeholder="dev.investigator"
                value={devUsername}
                onChange={(e) => setDevUsername(e.target.value)}
                className="w-full rounded-md border border-[var(--color-border)] bg-[var(--color-panel-raised)] px-3 py-2 text-[13px] text-[var(--color-ink)] outline-none focus:border-[var(--color-accent)]"
              />

              <Button
                type="submit"
                variant="secondary"
                className="w-full"
              >
                Continue (local testing only)
              </Button>

              <p className="text-center text-[10px] text-[var(--color-ink-faint)]">
                No real authentication is performed. For local
                development only — no backend is called.
              </p>
            </form>
          )}
        </Card>

        <p className="mt-5 text-center text-[11px] text-[var(--color-ink-faint)]">
          Face-ID service integration point:{' '}
          <code className="font-mono">
            /face/verify
          </code>
        </p>
      </div>
    </div>
  );
}