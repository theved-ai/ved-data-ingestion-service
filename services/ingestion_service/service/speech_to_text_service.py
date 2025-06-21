# speech_to_text_service.py  (drop-in)
from __future__ import annotations
import base64
import binascii
import subprocess
import tempfile
from pathlib import Path

import whisper

_MODEL = whisper.load_model("base")

class SpeechToTextError(RuntimeError):
    """Wrap *any* ffmpeg / Whisper failure so callers can handle it."""

# --------------------------------------------------------------------------
def _run_ffmpeg(
        in_path: Path | str,
        *,
        fmt: str = "f32le",
        rate: int = 48_000,
        ch: int   = 1,
) -> bytes:
    cmd = [
        "ffmpeg", "-nostdin", "-v", "error", "-threads", "0",
        "-f", fmt, "-ac", str(ch), "-ar", str(rate), "-i", str(in_path),
        "-f", "wav", "-ac", "1", "-ar", "16000", "-y", "-"      # wav to stdout
    ]
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, bufsize=0)
        return res.stdout
    except FileNotFoundError as exc:             # ffmpeg missing
        raise SpeechToTextError("ffmpeg not found on PATH") from exc
    except subprocess.CalledProcessError as exc: # ffmpeg ran but failed
        raise SpeechToTextError(
            f"ffmpeg failed (rc={exc.returncode}): "
            f"{exc.stderr.decode(errors='ignore')}"
        ) from exc

# --------------------------------------------------------------------------
def pcm_b64_to_text(
        *,
        audio_blob_b64: str,
        audio_chunk_index: int,
        pcm_format : str = "f32le",
        sample_rate: int = 48_000,
        channels   : int = 1,
) -> str:
    try:
        raw_pcm = base64.b64decode(audio_blob_b64)
    except binascii.Error as exc:
        raise SpeechToTextError("Invalid base-64 in payload") from exc

    if channels != 1:                           # early guard – helps debugging
        raise SpeechToTextError(
            f"Expected mono (1 ch) but got {channels} channels"
        )

    # ---------- temp #1 : raw pcm -----------------------------------------
    with tempfile.NamedTemporaryFile(suffix=".pcm", delete=False) as tmp_raw:
        tmp_raw.write(raw_pcm)
        tmp_raw_path = Path(tmp_raw.name)

    try:
        # ---------- ffmpeg → wav bytes ------------------------------------
        wav_bytes = _run_ffmpeg(
            tmp_raw_path, fmt=pcm_format, rate=sample_rate, ch=channels
        )
    finally:
        tmp_raw_path.unlink(missing_ok=True)    # tidy up

    # ---------- temp #2 : tiny wav Whisper loves --------------------------
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir='/Users/a36469/Downloads/test_audio_wav/', prefix=audio_chunk_index.__str__().join('_')) as tmp_wav:
        tmp_wav.write(wav_bytes)
        tmp_wav.flush()
        try:
            result = _MODEL.transcribe(tmp_wav.name)
            return result["text"].strip()
        except Exception as exc:
            raise SpeechToTextError(f"Whisper failed: {exc}") from exc
