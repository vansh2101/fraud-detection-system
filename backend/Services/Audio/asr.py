import mimetypes
import whisper
import torch

# Load models here 
whisper_model = whisper.load_model("turbo")

def extract_text_from_audio_video(file_path : str):
    try : 
        whisper_model.transcribe(file_path)
    except Exception as e :
        print(e)

    return 
