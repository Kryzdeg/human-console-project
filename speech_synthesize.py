from google.cloud import texttospeech
from playsound import playsound
import os


def synthesize_speech(text_to_synthesize, file_name):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)

    voice = texttospeech.VoiceSelectionParams(
        language_code="pl-PL", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(f"sounds/{file_name}", "wb") as out:
        out.write(response.audio_content)


def play_sound(msg, file_name):
    if not os.path.isfile(f"sounds/{file_name}"):
        synthesize_speech(msg, file_name)
    print(msg)
    playsound(f"sounds/{file_name}")
