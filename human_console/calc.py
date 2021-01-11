from ply.lex import lex
from ply.yacc import yacc
import re
from .functionality import operate_sum, operate_minus, operate_times

tokens = (
    "OPERATE_PLUS",
    "OPERATE_MINUS",
    "OPERATE_TIMES",
    "NUMBER",
)


def CalcLexer():

    def t_OPERATE_PLUS(t):
        r'[dD]odać | [Ss]uma | \+'

        if re.match(r'[dD]odać|[Ss]uma', t.value):
            t.value = re.sub(r'[dD]odać|[Ss]uma', "+", t.value)

        return t

    def t_OPERATE_MINUS(t):
        r'[Oo]djąć | [Mm]inus | -'

        if re.match(r'[Oo]djąć|[Mm]inus', t.value):
            t.value = re.sub(r'[Oo]djąć|[Mm]inus', "-", t.value)
        return t

    def t_OPERATE_TIMES(t):
        r'[Rr]azy | [Pp]omnóż\sprzez | \*'

        if re.match(r'[Rr]azy|[Pp]omnóż\sprzez', t.value):
            t.value = re.sub(r'[Rr]azy|[Pp]omnóż\sprzez', "*", t.value)
        return t

    def t_NUMBER(t):
        r'\d+'
        return t

    t_ignore = ' \t'

    def t_error(t):
        print(f"Błąd: {t.value}")
        t.lexer.skip(1)

    return lex()


def p_command(p):
    '''command : NUMBER OPERATE_PLUS NUMBER
               | NUMBER OPERATE_MINUS NUMBER
               | NUMBER OPERATE_TIMES NUMBER'''

    if re.match(r'\+', p[2]):
        operate_sum(int(p[1]), int(p[3]))
    elif re.match(r'-', p[2]):
        operate_minus(int(p[1]), int(p[3]))
    elif re.match(r'\*', p[2]):
        operate_times(int(p[1]), int(p[3]))


calc_parser = yacc()
