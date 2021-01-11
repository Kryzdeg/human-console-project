import os
from word2number import w2n
from translate import Translator
import webbrowser
import speech_recognition as sr
from gtts import gTTS
import playsound


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


def get_webbrowser(browser=None):
    return webbrowser.get(browser)


def open_webpage_window(browser, page="google.pl"):
    browser.open_new(page)


def open_webpage_tab(browser, page="google.pl"):
    browser.open_new_tab(page)
