from ply.lex import lex
from ply.yacc import yacc
from functionality import (
    create_txt_file,
    delete_txt_file,
    testing,
    open_webpage_window,
    open_webpage_tab,
    get_webbrowser,
    print_command
)

import re

tokens = (
    'TEST',
    'TEST_ARG',
    'OPERATE',
    'WEBBROWSER',
    'BROWSER_ARG',
    'PAGE',
    'FILE',
    'FILE_TYPE',
    'FILE_NAME'
)


def t_TEST(t):
    r'[Tt]est'
    return t


def t_TEST_ARG(t):
    r'(.)+'

    t.value = re.sub(r' kropka ', '.', t.value)
    return t


def t_OPERATE(t):
    r'[Ww](łącz|yłącz) | [Oo](dpal|dtwórz|dpaułzuj) | [Zz](atrzymaj|apałzuj) | [SsUu]twórz | [Ss](zukaj|kasuj) | [Uu]suń'
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
    r'[Tt]aby? | [Zz]akładk[ai] | [Oo]kn[oa]'
    return t


def t_PAGE(t):
    r'\w+'
    return t


def t_FILE(t):
    r'[Pp]lik'
    return t


def t_FILE_TYPE(t):
    r'[Tt]ekstowy | [Dd]źwiękowy'
    return t


def t_FILE_NAME(t):
    r'(\w+(\s)?)+'
    return t


t_ignore = ' \t'


def t_error(t):
    print(f"Błąd: {t.value}")
    t.lexer.skip(1)


def p_command_file(p):
    '''command : OPERATE FILE FILE_TYPE FILE_NAME
               | OPERATE FILE FILE_TYPE'''

    if re.match(r'[Ww]łącz|[Oo](dpal|twórz)', p[1]):
        print(p[1], p[2])

    elif re.match(r'[SsUu]twórz', p[1]):
        if re.match(r'[Pp]lik', p[2]):
            if re.match(r'[Tt]ekstowy', p[3]):
                try:
                    file_name = f"{p[4].replace(' ', '_')}.txt"
                except IndexError:
                    file_name = "files/file.txt"

                create_txt_file(file_name)
        else:
            print("Zła komenda :(")

    elif re.match(r'[Uu]suń|[Ss]kasuj', p[1]):
        if re.match(r'[Pp]lik', p[2]):
            if re.match(r'[Tt]ekstowy', p[3]):
                try:
                    file_name = f"{p[4]}.txt"
                    delete_txt_file(file_name)
                except IndexError:
                    print("Musisz podać jaki plik chcesz usunąć.")

    print_command(p.value)


def p_command_web(p):
    '''command : OPERATE WEBBROWSER
               | OPERATE WEBBROWSER BROWSER_ARG
               | OPERATE WEBBROWSER BROWSER_ARG PAGE'''

    if re.match(r'[Ww]łącz|[Oo](dpal|twórz)', p[1]):
        try:
            if re.match(r'[Tt]aby?|[Zz]akładk[ai]', p[3]):
                open_webpage_tab(get_webbrowser(p[2]))
            elif re.match(r'[Oo]kn[oa]', p[3]):
                open_webpage_window(get_webbrowser(p[2]))
        except IndexError:
            open_webpage_window(get_webbrowser(p[2]))
    else:
        print("Błędna komenda ...")


def p_command_test(p):
    '''command : TEST
               | TEST TEST_ARG'''

    if re.match(r'[Tt]est', p[1]):
        try:
            testing(p[2])
        except IndexError:
            testing()

    print_command(p.value)


def p_error(p):
    print(f"Niepoprawna komenda.")


lexer = lex()
parser = yacc()
