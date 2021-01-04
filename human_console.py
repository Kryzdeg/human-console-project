from ply.lex import lex
from ply.yacc import yacc
import re

tokens = (
    'OPERATE',
)


def t_OPERATE(t):
    r'[Ww](łącz|yłącz) | [Oo](dpal|dtwórz|dpaułzuj) | [Zz](atrzymaj|apałzuj)'
    return t


t_ignore = ' \t'


def p_command(p):
    '''command : OPERATE'''
    print(re.match(r'[Ww]łącz|[Oo](dpal|dtwórz)', p[1]), p[1])
    if re.match(r'[Ww]łącz|[Oo](dpal|dtwórz)', p[1]):
        print("Elo jestem se tutaj. Testuje se.")


lexer = lex()
parser = yacc()
