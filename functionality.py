import os
from speech_synthesize import synthesize_speech
from playsound import playsound


def create_file(file_name):

    if not os.path.isfile(file_name):
        f = open(file_name, 'w')
        msg = f"Utworzono plik tekstowy {file_name}"
        audio_file_name = f"create_file_{file_name.split('.')[0]}.mp3"
        f.close()
    else:
        msg = f"Plik już istnieje."
        audio_file_name = f"file_txt_exist.mp3"

    if not os.path.isfile(audio_file_name):
        synthesize_speech(msg, audio_file_name)

    print(msg)
    playsound(audio_file_name)


