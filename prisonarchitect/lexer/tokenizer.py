from itertools import dropwhile
import re

from prisonarchitect.lexer.tokens import parse_order, Token


def input_stream(src):
    token = ""
    inside = False
    for char in dropwhile(lambda x: x in '\t\n', src):
        if char is '"':
            inside = not inside
            if token:
                yield token
                token = ''
            yield char
        elif char in ' \n' and token and not inside:
            yield token
            token = ''
        elif char in ' \n' and not inside:
            continue
        else:
            token += char


def tokenize(src):
    tokens = []
    size = 0
    for token in input_stream(src):
        for parser, token_type in parse_order:
            if re.search(parser, token):
                tokens.append(Token(token, token_type))
                break
    return tokens

