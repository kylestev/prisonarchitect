from itertools import dropwhile
import re

from prisonarchitect.lexer.tokens import parse_order, Token


def input_stream(src):
    token = ""
    for char in dropwhile(lambda x: x in '\t\n', src):
        if char is '"':
            if token:
                yield token
                token = ''
            yield char
        elif char in ' \n' and token:
            yield token
            token = ''
        elif char in ' \n':
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

