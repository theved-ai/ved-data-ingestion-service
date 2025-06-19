import tempfile
import whisper
import base64

def generata_text(audio_blob: str, audio_format: str) -> str:
    decoded_audio_blob = base64.b64decode(audio_blob)
    suffix = '.' + audio_format.lstrip('.')
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(decoded_audio_blob)
        tmp.flush()
        result = whisper.load_model('base').transcribe(tmp.name)
        return result['text']