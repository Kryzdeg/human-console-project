from speech_recognition import speech_recognition
from sound_recorder import sound_recorder
from google.cloud.speech_v1.services.speech import SpeechClient
from human_console import parser

import sys

HERTZ_RATE = 16000
CLIENT = SpeechClient()


while True:
    print("Wybierz:\n1 - aby włączyć nasłuchiwanie,\n2 - żeby zakończyć działanie programu.")
    switch = input()

    if switch == "1":
        sound_recorder(hertz_rate=HERTZ_RATE)
        msg = speech_recognition(gcloud_client=CLIENT, hertz_rate=HERTZ_RATE)
        print("Twoja komenda: " + msg)
        parser.parse(msg)

    elif switch == "2":
        sys.exit()

    else:
        print("Wciśnij jeden z podanych przycisków.")
