import ply.lex as lex
from ply.yacc import yacc
from .functionality import (
    create_txt_file,
    delete_txt_file,
    create_directory,
    delete_directory,
    update_txt_file
)

import re

tokens = (
    'OPERATE',
    'FILE_TYPE',
    'FILE_NAME',
    "TEXT"
)


def FilesLexer():
    def t_OPERATE(t):
        r'[SsUu]twórz | [Ss]kasuj | [Uu]suń | [Ee]dytuj | [Dd]opisz\sdo'
        return t

    def t_FILE_TYPE(t):
        r'[Pp]liku?\s([Tt]ekstow(y|ego)|[Dd]źwiękowy)| [Ff]older'
        return t

    def t_FILE_NAME(t):
        r'(\w+(\s)?)+,?'

        if re.match(r"(\w+(\s)?)+,", t.value):
            t.value = re.sub(r",", "", t.value)

        return t

    def t_TEXT(t):
        r'(\w+\s?)+'
        return t

    t_ignore = ' \t'

    def t_error(t):
        print(f"Błąd: {t.value}")
        t.lexer.skip(1)

    return lex.lex()


def p_command(p):
    '''command : OPERATE FILE_TYPE FILE_NAME
               | OPERATE FILE_TYPE'''

    if re.match(r'[SsUu]twórz', p[1]):
        if re.match(r'[Pp]lik\s([Tt]ekstowy)', p[2]):
            try:
                file_name = f"{p[3].replace(' ', '_')}.txt"
            except IndexError:
                file_name = "file.txt"

            create_txt_file(file_name)
        elif re.match(r'[Ff]older', p[2]):
            try:
                directory_name = f"{p[3].replace(' ', '_')}"
            except IndexError:
                directory_name = "default_directory"

            create_directory(directory_name)
        else:
            print("Zła komenda :(")

    elif re.match(r'[Uu]suń|[Ss]kasuj', p[1]):
        if re.match(r'[Pp]lik\s([Tt]ekstowy)', p[2]):
            try:
                file_name = f"{p[3]}.txt"
                delete_txt_file(file_name)
            except IndexError:
                print("Musisz podać jaki plik chcesz usunąć.")

        elif re.match(r'[Ff]older', p[2]):
            try:
                directory_name = f"{p[3].replace(' ', '_')}"
            except IndexError:
                directory_name = "default_directory"

            delete_directory(directory_name)
        else:
            print("Zła komenda :(")

    elif re.match(r'[Ee]dytuj|[Dd]opisz\sdo', p[1]):
        if re.match(r"[Pp]liku?\s[Tt]ekstow(y|ego)", p[2]):
            try:
                update_txt_file(p[3], p[4])
            except IndexError:
                print("Niepoprawna komenda.")


# def p_error(p):
#     print(f"Niepoprawna komenda.")


file_parser = yacc()
