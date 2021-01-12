from ply.lex import lex
from ply.yacc import yacc
from .functionality import (
    open_webpage_window,
    open_webpage_tab,
    get_webbrowser
)

import re

tokens = (
    'OPERATE',
    'WEBBROWSER',
    'BROWSER_ARG',
    'PAGE',
)

def BrowserLexer():

    def t_OPERATE(t):
        r'[Ww](łącz|yłącz) | [Oo](dpal|twórz) | [Zz](atrzymaj|apałzuj)'
        return t

    def t_WEBBROWSER(t):
        r"""([Gg](o{1,2}|u)gl(e)?\s)?[Cc]hrom(e|a)?
            | [Pp]rzeglądark[eę]
            | ([Mm]ozill(a|e|ę)\s)?[Ff](ire|ajer)fo(x|ks)a?"""

        if re.match(r'([Gg](o{1,2}|u)gl(e)?\s)?[Cc]hrom(e|a)?', t.value):
            t.value = "google-chrome"
        elif re.match(r'([Mm]ozill(a|e|ę)\s)?[Ff](ire|ajer)fo(x|ks)a?', t.value):
            t.value = "firefox"
        elif re.match(r'[Pp]rzeglądark[eę]', t.value):
            t.value = None

        return t

    def t_BROWSER_ARG(t):
        r'[wW]\s[Nn]ow(ym\s[Tt]abie|ej\s[Zz]akładce) | [Tt]ab | [Zz]akładka | [Oo]kn[o]'
        return t

    def t_PAGE(t):
        r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

        t.value = re.sub(r"\s.|.\s|\skropka\s", ".", t.value)
        return t

    t_ignore = ' \t'

    def t_error(t):
        print(f"Błąd: {t.value}")
        t.lexer.skip(1)

    return lex()


def p_command(p):
    '''command : OPERATE WEBBROWSER
               | OPERATE WEBBROWSER BROWSER_ARG
               | OPERATE WEBBROWSER BROWSER_ARG PAGE'''

    if re.match(r'[Ww]łącz|[Oo](dpal|twórz)', p[1]):
        try:
            if re.match(r'[wW]\s[Nn]ow(ym\s[Tt]abie|ej\s[Zz]akładce)|[Tt]ab|[Zz]akładka', p[3]):
                try:
                    print(p[4])
                    open_webpage_tab(get_webbrowser(p[2]), p[4])
                except IndexError:
                    open_webpage_tab(get_webbrowser(p[2]))

            elif re.match(r'[Oo]kn[oa]', p[3]):
                open_webpage_window(get_webbrowser(p[2]))
        except IndexError:
            open_webpage_window(get_webbrowser(p[2]))


def p_error(p):
    print(f"Niepoprawna komenda.")


browser_parser = yacc()
