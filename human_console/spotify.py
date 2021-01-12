from ply.lex import lex
from ply.yacc import yacc
import re
from .functionality import SpotifyControler

tokens = (
    "OPERATE",
    "ARTIST",
    "SONG"
)


def SpotifyLexer():
    def t_OPERATE(t):
        r'([Oo]d|[Zz]a)pauzuj | [Pp]auza | [Ww](łącz|znów) | [Oo]d(twórz|pal)'
        return t

    t_ignore = ' \t'

    def t_error(t):
        print(f"Błąd: {t.value}")
        t.lexer.skip(1)

    return lex()


def p_command(p):
    """command : OPERATE
               | OPERATE ARTIST SONG"""

    if re.match(r"[Oo]dpauzuj|[Ww]znów", p[1]):
        spotify_unpause()
    elif re.match(r"[Zz]apauzuj|[Pp]auza]", p[1]):
        spotify_pause()


def p_error(p):
    print(f"Niepoprawna komenda.")


spotify_parser = yacc()
