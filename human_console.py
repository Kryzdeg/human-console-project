from ply.lex import lex
from ply.yacc import yacc
import re
import os

tokens = (
    'OPERATE',
    'OBJECT',
    'FILE_TYPE',
    'FILE_NAME'
)


def t_OPERATE(t):
    r'[Ww](łącz|yłącz) | [Oo](dpal|dtwórz|dpaułzuj) | [Zz](atrzymaj|apałzuj) | [SsUu]twórz | [Ss]zukaj'
    return t


def t_OBJECT(t):
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
               | OPERATE OBJECT FILE_TYPE FILE_NAME
               | OPERATE OBJECT FILE_TYPE'''

    if re.match(r'[Ww]łącz|[Oo](dpal|dtwórz)', p[1]):
        print("Elo jestem se tutaj. Testuje se.")

    elif re.match(r'[SsUu]twórz', p[1]):
        if re.match(r'[Pp]lik', p[2]):
            if re.match(r'[Tt]ekstowy', p[3]):
                try:
                    f = open(p[4] + ".txt", 'w')
                except IndexError:
                    f = open("file.txt", 'w')
                f.close()
                print("Stworzono plik :D !")
        else:
            print("Zła komenda :(")



lexer = lex()
parser = yacc()
