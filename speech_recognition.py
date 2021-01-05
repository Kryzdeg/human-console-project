from google.cloud.speech_v1 import types
from google.cloud.speech_v1.services.speech import SpeechClient
import io
import os

LANGUAGE_RECOGNITION = 'pl-PL'


def speech_recognition(hertz_rate):

    client = SpeechClient()

    with io.open('file.wav', 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=hertz_rate,
        language_code=LANGUAGE_RECOGNITION,
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)

    if os.path.isfile('file.wav'):
        os.remove('file.wav')

    for result in response.results:
        return result.alternatives[0].transcript
