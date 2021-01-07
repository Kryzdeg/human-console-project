from speech_recognition import speech_recognition
from sound_recorder import sound_recorder
from human_console import parser

import sys

HERTZ_RATE = 16000

while True:
    print("Wybierz:\n1 - aby włączyć nasłuchiwanie,"
          "\n2 - żeby wpisać ręcznie komendę,"
          "\n3 - żeby zakończyć działanie programu.")

    switch = input()

    if switch == "1":
        sound_recorder(hertz_rate=HERTZ_RATE)
        msg = speech_recognition(hertz_rate=HERTZ_RATE)
        print("Twoja komenda: " + msg)
        # parser.parse(msg)

    elif switch == "2":
        msg = input("Wpisz komendę:")
        print(msg)
        parser.parse(msg)

    elif switch == "3":
        sys.exit()

    else:
        print("Wciśnij jeden z podanych przycisków.")
