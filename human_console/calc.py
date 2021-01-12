from ply.lex import lex
from ply.yacc import yacc
import re
from .functionality import operate_sum, operate_minus, operate_times, operate_divide, operate_power, operate_nth_root

tokens = (
    "OPERATE_PLUS",
    "OPERATE_MINUS",
    "OPERATE_TIMES",
    "OPERATE_DIVIDE",
    "OPERATE_POWER",
    "OPERATE_ROOT",
    "NUMBER",
)


def CalcLexer():

    def t_OPERATE_PLUS(t):
        r'[dD]oda(ć|j\sdo) | [Ss]uma | \+'

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

    def t_OPERATE_DIVIDE(t):
        r'([Pp]odziel(one)?\s)?przez | /'

        if re.match(r'([Pp]odziel(one)?\s)?przez', t.value):
            t.value = re.sub(r'([Pp]odziel(one)?\s)?przez', "/", t.value)
        return t

    def t_OPERATE_POWER(t):
        r'[Dd]o(\s[Pp]otęgi)? | \^'

        if re.match(r'[Dd]o(\s[Pp]otęgi)?', t.value):
            t.value = re.sub(r'[Dd]o(\s[Pp]otęgi)?', "^", t.value)
        return t

    def t_OPERATE_ROOT(t):
        r'[Pp]ierwiastek\s(\d+)\sstopnia\sz | [Kk]wadrat\sz | [Ss]ześcian\sz'

        if re.match(r"[Pp]ierwiastek\s(\d+)\sstopnia\sz", t.value):
            root = "root" + re.match(r"[Pp]ierwiastek\s(\d+)\sstopnia\sz", t.value).group(1)
            t.value = re.sub(r"[Pp]ierwiastek\s(\d+)\sstopnia\sz", root, t.value)
        elif re.match(r"[Kk]wadrat\sz", t.value):
            root = "root2"
            t.value = re.sub(r"[Kk]wadrat\sz", root, t.value)
        elif re.match(r"[Ss]ześcian\sz", t.value):
            root = "root3"
            t.value = re.sub(r"[Ss]ześcian\sz", root, t.value)
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
               | NUMBER OPERATE_TIMES NUMBER
               | NUMBER OPERATE_DIVIDE NUMBER
               | NUMBER OPERATE_POWER NUMBER
               | OPERATE_ROOT NUMBER'''

    if re.match(r'\+', p[2]):
        operate_sum(int(p[1]), int(p[3]))
    elif re.match(r'-', p[2]):
        operate_minus(int(p[1]), int(p[3]))
    elif re.match(r'\*', p[2]):
        operate_times(int(p[1]), int(p[3]))
    elif re.match(r'/', p[2]):
        operate_divide(int(p[1]), int(p[3]))
    elif re.match(r'\^', p[2]):
        operate_power(int(p[1]), int(p[3]))
    elif re.match(r'root(\d+)', p[1]):
        num = re.match(r'root(\d+)', p[1]).group(1)
        operate_nth_root(int(num), int(p[2]))


calc_parser = yacc()
