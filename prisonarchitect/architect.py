import json

from prisonarchitect.lexer.parsers import read_quote, section_name, section_contents
from prisonarchitect.lexer.tokenizer import tokenize
from prisonarchitect.lexer.tokens import Token
from prisonarchitect.section import Section


class PrisonParser(object):
    def __init__(self):
        pass

    def _tokenize(self, filename):
        with open(filename, 'r') as f:
            return tokenize(f.read())

    def _parse_section(self, parent, tokens):
        name_tokens, consumed = section_name(tokens[0:])

        if name_tokens is None:
            pprint(tokens[:10])
            raise Exception('Name of a section under {0} unable to be parsed!'.format(parent.name))

        section = Section(' '.join(t.value for t in name_tokens))

        noaction = True
        idx = consumed
        while idx < len(tokens):
            piece = tokens[idx]
            if type(piece) is list:
                child = self._parse_section(section, piece)
                section.add_section(child)
                idx += 1
                noaction = False
            elif type(piece) is Token:
                token = piece
                if token.type in ['T_NAME', 'T_OBJ_PROP']:
                    section.add_attribute(token.value, tokens[idx + 1].value)
                    idx += 2
                    noaction = False
                elif token.type == 'T_QUOTE':
                    q_tokens, q_consumed = read_quote(tokens[idx:])

                    attr_name = ' '.join(t.value for t in q_tokens)

                    section.add_attribute(attr_name, tokens[idx + q_consumed].value)

                    idx += q_consumed + 1
                    noaction = False

            if noaction:
                raise Exception('Found a section unable to be parsed under {0} --> {1}'.format(parent.name, section.name))

            noaction = True

        return section

    def _parse(self, base_section, tokens):
        idx = 0
        ntokens = len(tokens)

        has_next = lambda: idx + 1 < ntokens
        get_next = lambda: tokens[idx + 1]
        noaction = False

        while idx < ntokens - 1:
            tok = tokens[idx]
            nxt = get_next()

            if tok.type in ['T_NAME', 'T_OBJ_PROP']:
                base_section.add_attribute(tok.value, nxt.value)
                idx += 2
            elif tok.type == 'SEC_START':
                matched, consumed = section_contents(tokens[idx:])

                section = self._parse_section(base_section, matched)
                base_section.add_section(section)

                idx += consumed

    def load(self, filename, caching=False):
        if caching:
            self.tokens = []
            with open('cache.json', 'r') as f:
                token_pairs = json.loads(f.read())
            for pair in token_pairs:
                self.tokens.append(Token(*pair))
        else:
            self.tokens = self._tokenize(filename)
            with open('cache.json', 'w') as f:
                f.write(json.dumps(self.tokens))

        section = Section('self')
        self._parse(section, self.tokens)

        return section
