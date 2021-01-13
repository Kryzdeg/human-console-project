from gtts import gTTS
from numpy import power, round
from spotipy.oauth2 import SpotifyOAuth

import os
import platform
import webbrowser
import playsound
import speech_recognition as sr
import spotipy
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


class SpotifyController:
    def __init__(self):
        self.sp = None
        self.current_device_id = None

    def setup(self):
        scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        auth_manager = SpotifyOAuth(client_id=env("SPOTIFY_API_CLIENT_ID"),
                                    client_secret=env("SPOTIFY_API_CLIENT_SECRET"),
                                    redirect_uri=env("SPOTIFY_API_REDIRECT_URI"),
                                    scope=scope)

        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self._get_computer_device_id()

    def _get_current_device(self):
        for device in self.sp.devices()['devices']:
            if device['id'] == self.current_device_id:
                return device

    def _get_computer_device_id(self):
        for device in self.sp.devices()['devices']:
            if device['name'] == platform.node():
                self.current_device_id = device['id']
                return

        if not self.current_device_id:
            self.current_device_id = None

    def _get_smartphone_device_id(self):
        for device in self.sp.devices()['devices']:
            if device['type'] == "Smartphone":
                self.current_device_id = device['id']
                return

        if not self.current_device_id:
            self.current_device_id = None

    def _get_me(self):
        return self.sp.me()

    def _get_artist_id(self, artist):
        q_artist = self.sp.search(q=artist, type='artist')
        try:
            return q_artist['artists']['items'][0]['id']
        except Exception as e:
            return None

    def _get_track_uri(self, artist_id, track_name):
        q_track = self.sp.search(q=track_name, type="track")
        for track in q_track['tracks']['items']:
            if artist_id in [artist['id'] for artist in track['artists']]:
                return track['uri']

        return None

    def _get_playlist_uri(self, playlist, is_mine=False):
        q_playlist = self.sp.search(q=playlist, type="playlist")
        if not is_mine:
            return q_playlist['playlists']['items'][0]['uri']
        else:
            for pl in q_playlist['playlists']['items']:
                if pl['owner']['id'] == self._get_me()['id']:
                    return pl['uri']
            return None

    def spotify_unpause(self):
        try:
            if self.current_device_id:
                self.sp.start_playback()
        except Exception as e:
            msg = "Twój utwór już jest odtwarzany, lub nie wybrałeś utworu do odtworzenia."
            print(msg)
            play_sound(msg, "track_cant_be_played.mp3")

    def spotify_pause(self):
        try:
            if self.current_device_id:
                self.sp.pause_playback()
        except Exception as e:
            msg = "Twój utwór już jest zatrzymany, lub nie ma co zatrzymywać."
            print(msg)
            play_sound(msg, "track_cant_be_paused_.mp3")

    def spotify_reset_track(self):
        self.sp.seek_track(position_ms=0)

    def spotify_next_track(self):
        self.sp.next_track()

    def spotify_change_to_smartphone(self):
        self._get_smartphone_device_id()
        self.sp.transfer_playback(device_id=self.current_device_id)

    def spotify_change_to_computer(self):
        self._get_computer_device_id()
        self.sp.transfer_playback(device_id=self.current_device_id)

    def spotify_play_playlist(self, playlist, is_mine=False):
        playlist_uri = self._get_playlist_uri(playlist, is_mine)

        if playlist_uri:
            self.sp.start_playback(context_uri=playlist_uri)
        else:
            msg = f"Nie znaleziono playlisty."
            print(msg)
            play_sound(msg, "playlist_dont_exist.mp3")

    def spotify_play_track(self, artist, track):
        artist_id = self._get_artist_id(artist)

        if artist_id:
            track_uri = self._get_track_uri(artist_id, track)
        else:
            msg = f"Nie znaleziono artysty {artist}."
            print(msg)
            play_sound(msg, "artist_dont_exists.mp3")
            return

        if track_uri:
            self.sp.start_playback(uris=[track_uri])
        else:
            msg = "Nie znaleziono poszukiwanego utworu."
            print(msg)
            play_sound(msg, "track_dont_exists.mp3")
            return