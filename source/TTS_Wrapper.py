from google.cloud import texttospeech
from dotenv import load_dotenv

class TTS_Wrapper:
    def __init__(self):
        load_dotenv()
        self.client = texttospeech.TextToSpeechClient()
        
    #default to mp3 output
    def set_audio_encoding(encoding=texttospeech.AudioEncoding.MP3):
        texttospeech.AudioConfig(audio_encoding=encoding)

  
