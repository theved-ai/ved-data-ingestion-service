import base64

def encode_audio_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    return encoded_string

def main():
    # Usage
    file_path = '/Users/a36469/Downloads/sample_audio_7.m4a'  # or .wav, .mp3 etc.
    base64_audio = encode_audio_to_base64(file_path)
    print(base64_audio)  # Print first 200 chars to verify

if __name__ == '__main__':
    main()