import os
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import playsound
from numpy import power, round
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import environ


env = environ.Env()
environ.Env.read_env()


def recording_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language="pl-PL")
        except Exception as e:
            print(str(e))
        return said


def synthesize_text(msg, filename="voice.mp3"):
    tts = gTTS(text=msg, lang="pl", )
    filename = filename
    file_audio = open(f"human_console/sounds/{filename}", 'wb')
    tts.write_to_fp(file_audio)
    file_audio.close()


def play_sound(msg, file_name):
    if not os.path.isfile(f"human_console/sounds/{file_name}"):
        synthesize_text(msg, file_name)
    playsound.playsound(f"human_console/sounds/{file_name}")


def testing(msg="Test został przeprowadzony poprawnie.", file_name='test.mp3'):
    play_sound(msg, file_name)
    # translator = Translator(to_lang='en', from_lang='pl')
    # translation = translator.translate("jeden milion dziewięćset dziewięćdziesiąt dziewięć")
    # print(translation)
    # print(w2n.word_to_num(translation))


def create_txt_file(file_name):
    if not os.path.isdir("files"):
        os.mkdir("files")

    if not os.path.isfile(f"files/{file_name}"):
        f = open(f"files/{file_name}", 'w')
        msg = f"Utworzono plik tekstowy {file_name.replace('_', ' ')}"
        audio_file_name = f"create_file_{file_name.split('.')[0]}.mp3"
        f.close()
    else:
        msg = f"Plik już istnieje."
        audio_file_name = f"file_txt_exist.mp3"

    print(msg)
    play_sound(msg, audio_file_name)


def delete_txt_file(file_name):
    if os.path.isfile(f"../files/{file_name}"):
        os.remove(f"../files/{file_name}")
        msg = f"Usunięto plik tekstowy."
        audio_file_name = f"file_txt_deleted.mp3"

    else:
        msg = f"Plik, który chcesz usunąć, nie istnieje."
        audio_file_name = f"file_not_exist.mp3"

    play_sound(msg, audio_file_name)


def run_program(program_name):
    subprocess.call(["tutaj_ścieżka"])


def get_webbrowser(browser=None):
    return webbrowser.get(browser)


def open_webpage_window(browser, page="google.pl"):
    browser.open_new(page)


def open_webpage_tab(browser, page="google.pl"):
    browser.open_new_tab(page)


def operate_sum(num1, num2):
    result = num1 + num2

    msg = f"Wynik działania {num1} + {num2} = {result}."
    file_name = f"sum_{num1}_{num2}.mp3"
    print(msg)
    play_sound(msg, file_name)


def operate_minus(num1, num2):
    result = num1 - num2

    msg = f"Wynik działania {num1} odjąć {num2} = {result}."
    file_name = f"minus_{num1}_{num2}.mp3"
    print(msg.replace("odjąć", "-"))
    play_sound(msg, file_name)


def operate_times(num1, num2):
    result = num1 * num2

    msg = f"Wynik działania {num1} razy {num2} = {result}."
    file_name = f"times_{num1}_{num2}.mp3"
    print(msg.replace("razy", "*"))
    play_sound(msg, file_name)


def operate_divide(num1, num2):
    if num2 == 0:
        msg = "Kto dzielić przez zero próbuje\n" +\
              "dostaje jedynki, nie dwóje,\n" +\
              "bo wiedzą wszyscy i wszędzie,\n" +\
              "że z tego nic nie będzie!"

        file_name = f"dont_divide_by_0.mp3"
        print(msg.replace("podzielone przez", "/"))
        play_sound(msg, file_name)
        return

    result = round(num1 / num2, 4)
    if result % int(result) == 0:
        result = int(result)

    msg = f"Wynik działania {num1} podzielone przez {num2} = {result}."
    file_name = f"divide_{num1}_{num2}.mp3"
    print(msg.replace("podzielone przez", "/"))
    play_sound(msg, file_name)


def operate_power(num1, num2):
    result = power(num1, num2)

    msg = f"Wynik działania {num1} do potęgi {num2} = {result}."
    file_name = f"power_{num1}_{num2}.mp3"
    print(msg.replace(" do potęgi ", "^"))
    play_sound(msg, file_name)


def operate_nth_root(root, num):
    if root == 0:
        msg = "Kto dzielić przez zero próbuje\n" +\
              "dostaje jedynki, nie dwóje,\n" +\
              "bo wiedzą wszyscy i wszędzie,\n" +\
              "że z tego nic nie będzie!"

        file_name = f"dont_divide_by_0.mp3"
        print(msg.replace("podzielone przez", "/"))
        play_sound(msg, file_name)
        return

    result = round(power(num, (1./root)), 4)
    if result % int(result) == 0:
        result = int(result)

    msg = f"Wynik działania pierwiastek {root} stopnia z {num} = {result}."
    file_name = f"root_{root}_{num}.mp3"
    print(msg)
    play_sound(msg, file_name)


class SpotifyControler(object):
    def __init__(self):
        self.sp = None
        self.device_id = None

    def authorize(self):
        scope = "user-modify-playback-state playlist-modify-public playlist-modify-private user-follow-modify user-read-currently-playing user-read-playback-state"

        auth_manager = SpotifyOAuth(client_id=env("SPOTIFY_API_CLIENT_ID"), client_secret=env("SPOTIFY_API_CLIENT_SECRET"),
                                    redirect_uri=env("SPOTIFY_API_REDIRECT_URI"), scope=scope)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_device_id(self):
        print(self.sp.devices())

    def get_me(self):
        print(self.sp.me())

    def spotify_unpause(self):
        pass

    def spotify_pause(self):
        pass

    def spotify_play_song(self, artist, song):
        pass

