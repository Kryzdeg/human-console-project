from my_speech_recognition import speech_recognition
from human_console.functionality import play_sound, recording_command, synthesize_text
from human_console.files import file_parser, FilesLexer
from human_console.browser import browser_parser, BrowserLexer
from human_console.calc import calc_parser, CalcLexer
import sys


def run_command(msg):
    lexer_type = msg.split()[0].upper()
    msg = msg.split(" ", 1)[1]
    if lexer_type == "PLIKI":
        file_lexer = FilesLexer()
        file_parser.parse(msg, lexer=file_lexer)
    elif lexer_type == "PRZEGLĄDARKA":
        browser_lexer = BrowserLexer()
        browser_parser.parse(msg, lexer=browser_lexer)
    elif lexer_type == "KALKULATOR":
        calc_lexer = CalcLexer()
        calc_parser.parse(msg, lexer=calc_lexer)
    else:
        print("Podaj proszę typ poleceń.")


while True:
    print("Wybierz:\n1 - aby włączyć nasłuchiwanie,"
          "\n2 - żeby wpisać ręcznie komendę,"
          "\n3 - żeby zakończyć działanie programu.")

    switch = input()

    if switch == "1":
        msg = recording_command()
        print("Podana komenda: " + msg)
        # run_command(msg)

    elif switch == "2":
        msg = input("Wpisz komendę: ").lower()
        print("Podana komenda: " + msg)
        run_command(msg)

    elif switch == "3":
        sys.exit()

    else:
        print("Wciśnij jeden z podanych przycisków.")
