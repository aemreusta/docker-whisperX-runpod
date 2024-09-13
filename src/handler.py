import os

import runpod
from model import AudioBase64, AudioUrl
from utils import base64_to_tempfile, download_file

import whisperx

# CHECK THE ENV VARIABLES FOR DEVICE AND COMPUTE TYPE
device = os.environ.get('DEVICE', 'cpu') # cpu if on Mac
compute_type = os.environ.get('COMPUTE_TYPE', 'int8') #int8 if on Mac
batch_size = 2 # reduce if low on GPU mem

# Retrieve language code and whisper model from environment variables
language_code = os.environ.get('LANGUAGE_CODE', 'tr')  # Default to 'tr' (Turkish)
whisper_model = os.environ.get('WHISPER_MODEL', 'base')  # Default to 'base'

# Load the model outside the handler
model = whisperx.load_model(whisper_model, device, compute_type=compute_type, language=language_code)
model_align, metadata = whisperx.load_align_model(language_code=language_code, device=device)



def handler(event: dict) -> dict:

    audio_input = event.get("input")

    if audio_input is None:
        raise ValueError("No audio input provided")
    
    if audio_input.get("audio_base_64") is not None:
        audio_input = AudioBase64(base64_bytes=audio_input.get("audio_base_64"))
        audio_input_file = base64_to_tempfile(audio_input)

    elif audio_input.get("url") is not None:
        audio_input = AudioUrl(url=audio_input.get("url"))
        audio_input_file = download_file(audio_input)

    else:
        return {"error": "No valid audio input provided"}

    try:
        
        # Load the audio
        audio = whisperx.load_audio(audio_input_file, device)
        # Transcribe the audio
        result = model.transcribe(audio, batch_size=batch_size, language=language_code, print_progress=True)

        # 2. Align whisper output
        
        result = whisperx.align(result["segments"], model_align, metadata, audio, device)
        print(result["segments"])

        # after alignment
        return result
    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({
    "handler": handler
})