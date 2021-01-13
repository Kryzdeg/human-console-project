from ply.lex import lex
from ply.yacc import yacc
import re
from .functionality import SpotifyController

tokens = (
    "OPERATE",
    "TRACK_PLAYLIST",
)


def SpotifyLexer():
    def t_OPERATE(t):
        r'''([Oo]d\s|([Zz]a)?)pauzuj
            | [Zz]atrzymaj
            | [Pp]auza
            | [Ww]znów
            | [Ww]łącz(\s(moją\s)?([Uu]twór|[Pp]iosenk[eę]|pl(ay|ej)list[ęe]))?
            | (([Ww]łącz|[Oo]twórz)|([Ww]yłącz|[Zz]amknij))\sspotif(y|aja)
            | [Oo]d(twórz(aj)?|pal)(\s(moją\s)?([Uu]twór|[Pp]iosenk[eę]|pl(ay|ej)list[ęe]))?
            | [Zz]?reset(uj)?
            | [Pp]uść\sod\s(nowa|początku)
            | ([Pp]rzełącz|[Zz]a?mień)\sna\s(telefon|smart(ph|f)ona?|komputer)
            | [Nn]e(ks|x)t | [Nn]astępny\s(utwór)?
            | ([Cc]ofnij\sdo\s)?([Pp]oprzedni(ego)?)(\sutwóru?)?'''
        return t

    def t_TRACK_PLAYLIST(t):
        r'(\w+\W*)+,\s(\w+\W*)+ | (\w+\s?)+'

        track = re.match(r'(.+),\s(.+)', t.value)
        if track:
            artist = track.group(1)
            title = track.group(2)

            if re.match(r'(\w\s)+', artist):
                title = re.sub(r'\s', "", artist)

            if re.match(r'(\w\s)+', title):
                title = re.sub(r'\s', "", title)

            t.value = (artist, title)

        return t

    t_ignore = ' \t'

    def t_error(t):
        print(f"Błędna komenda! -> {t.value}")

    return lex()


def p_command(p):
    """command : OPERATE
               | OPERATE TRACK_PLAYLIST"""

    spotify_controller = SpotifyController()
    spotify_controller.setup()

    if re.match(r"([Zz]a)?pauzuj|[Pp]auza|[Zz]atrzymaj]", p[1]):
        spotify_controller.spotify_pause()

    elif re.match(r"([Ww]łącz|[Oo]twórz)\sspotif(y|aja)", p[1]):
        spotify_controller.run_spotify()

    elif re.match(r"([Ww]yłącz|[Zz]amknij)\sspotif(y|aja)", p[1]):
        spotify_controller.kill_spotify()

    elif re.match(r"([Ww]łącz|[Oo](dtwórz|dpal))\s([Uu]twór|[Pp]iosenk[eę])", p[1]):
        try:
            spotify_controller.spotify_play_track(p[2][0], p[2][1])
        except Exception as e:
            spotify_controller.spotify_unpause()
    elif re.match(r"[Zz]?reset(uj)?|[Pp]uść\sod\s(nowa|początku)", p[1]):
        spotify_controller.spotify_reset_track()

    elif re.match(r"([Pp]rzełącz|[Zz]a?mień)\sna\s(telefon|smart(ph|f)ona?)", p[1]):
        spotify_controller.spotify_change_to_smartphone()

    elif re.match(r"([Pp]rzełącz|[Zz]a?mień)\sna\skomputer", p[1]):
        spotify_controller.spotify_change_to_computer()

    elif re.match(r"[Nn]e(ks|x)t|[Nn]astępny\s(utwór)?", p[1]):
        spotify_controller.spotify_next_track()

    elif re.match(r"([Cc]ofnij\sdo\s)?([Pp]oprzedni(ego)?)(\sutw(oru|ór))?", p[1]):
        spotify_controller.spotify_previous_track()

    elif re.match(r"([Ww]łącz|[Oo]d(twórz|pal))\s(pl(ay|ej)list[ęe])", p[1]):
        try:
            if re.match(r"(\w+\s?)+", p[2]):
                spotify_controller.spotify_play_playlist(p[2])
            else:
                print("Niepoprawna komenda.")
        except Exception as e:
            print("Niepoprawna komenda.")

    elif re.match(r"([Ww]łącz|[Oo]d(twórz|pal))\smoją\s(pl(ay|ej)list[ęe])", p[1]):
        try:
            if re.match(r"(\w+\s?)+", p[2]):
                spotify_controller.spotify_play_playlist(p[2], is_mine=True)
            else:
                print("Niepoprawna komenda.")
        except Exception as e:
            print("Niepoprawna komenda.")

    elif re.match(r"[Oo]d\spauzuj|[Ww]znów|[Ww]łącz|[Oo]d(twórz(aj)?|pal)", p[1]):
        spotify_controller.spotify_unpause()


def p_error(p):
    print(f"Niepoprawna komenda.")


spotify_parser = yacc()
