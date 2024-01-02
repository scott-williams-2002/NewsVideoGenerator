from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()



def synthesize_speech(text, output_filename):
# Create a Text-to-Speech client
    client = texttospeech.TextToSpeechClient()

    
    # Set the text input
    input_text = texttospeech.SynthesisInput(text=text)

    # Configure the voice settings
    voice = texttospeech.VoiceSelectionParams(language_code="en-AU", name="en-AU-Polyglot-1")

    # Set the audio configuration
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, pitch = -4.0, speaking_rate=1, effects_profile_id = ["handset-class-device"])
    #texttospeech.package_version

    # Perform the text-to-speech request
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # Save the audio to a file
    
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to '{output_filename}'")
    
    

# Test the text-to-speech function
synthesize_speech("Hey Chris. This is a test message from your brother, Sanka. Hope you are doing well. Don't poop too much or else the poop fairy will come.", "output.mp3")