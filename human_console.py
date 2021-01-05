from ply.lex import lex
from ply.yacc import yacc
from speech_synthesize import synthesize_speech
from functionality import create_file
from playsound import playsound
import re
import os

tokens = (
    'OPERATE',
    'FILE',
    'FILE_TYPE',
    'FILE_NAME'
)


def t_OPERATE(t):
    r'[Ww](łącz|yłącz) | [Oo](dpal|dtwórz|dpaułzuj) | [Zz](atrzymaj|apałzuj) | [SsUu]twórz | [Ss]zukaj | [Tt]est'
    return t


def t_FILE(t):
    r'[Pp]lik'
    return t


def t_FILE_TYPE(t):
    r'[Tt]ekstowy | [Dd]źwiękowy'
    return t


def t_FILE_NAME(t):
    r'\w+'
    return t


t_ignore = ' \t'


def p_command(p):
    '''command : OPERATE
               | OPERATE FILE FILE_TYPE FILE_NAME
               | OPERATE FILE FILE_TYPE'''

    if re.match(r'[Ww]łącz|[Oo](dpal|dtwórz)', p[1]):
        print("Elo jestem se tutaj. Testuje se.")

    elif re.match(r'[SsUu]twórz', p[1]):
        if re.match(r'[Pp]lik', p[2]):
            if re.match(r'[Tt]ekstowy', p[3]):
                try:
                    file_name = f"{p[4]}.txt"
                except IndexError:
                    file_name = "file.txt"

                create_file(file_name)
        else:
            print("Zła komenda :(")

    elif re.match(r'[Tt]est', p[1]):
        file_name = 'test.mp3'

        if not os.path.isfile(file_name):
            synthesize_speech("Test został przeprowadzony poprawnie.", file_name)
        playsound(file_name)


lexer = lex()
parser = yacc()
