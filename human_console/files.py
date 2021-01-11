import ply.lex as lex
from ply.yacc import yacc
from .functionality import (
    create_txt_file,
    delete_txt_file,
)

import re

tokens = (
    'OPERATE',
    'FILE',
    'FILE_TYPE',
    'FILE_NAME',
)


def FilesLexer():
    def t_OPERATE(t):
        r'[Ww](łącz|yłącz) | [Oo](dpal|dtwórz|dpaułzuj) | [Zz](atrzymaj|apałzuj) | [SsUu]twórz | [Ss](zukaj|kasuj) | [Uu]suń'
        return t

    def t_FILE( t):
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

    return lex.lex()


def p_command(p):
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
                    file_name = "file.txt"

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


def p_error(p):
    print(f"Niepoprawna komenda.")


file_parser = yacc()
