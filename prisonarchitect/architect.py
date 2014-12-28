import json

from prisonarchitect.lexer.parsers import read_quote, section_name, section_contents
from prisonarchitect.lexer.tokenizer import tokenize
from prisonarchitect.lexer.tokens import Token
from prisonarchitect.section import Section


class PrisonParser(object):
    def __init__(self):
        self.section = None

        self._sections = {}
        self._section_indices = {}

    def _tokenize(self, filename):
        with open(filename, 'r') as f:
            return tokenize(f.read())

    def _get_name_from_section(self, parent, tokens):
        name_tokens, consumed = section_name(tokens)
        if name_tokens is None:
            print tokens[:5]
            raise Exception(('Name of a section under {0} unable '
                             'to be parsed!').format(parent.name))

        return ' '.join(t.value for t in name_tokens), consumed

    def _parse_section(self, parent, tokens):
        name, idx = self._get_name_from_section(parent, tokens)
        section = Section(name)

        noaction = True
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
                    nxt = tokens[idx + 1]

                    if nxt.type == 'T_QUOTE':
                        q_tokens, q_consumed = read_quote(tokens[idx+1:])
                        val = ' '.join(t.value for t in q_tokens)
                        idx += q_consumed + 1
                    else:
                        val = nxt.value
                        idx += 2

                    section.add_attribute(token.value, val)

                    noaction = False
                elif token.type == 'T_QUOTE':
                    q_tokens, q_consumed = read_quote(tokens[idx:])

                    attr_name = ' '.join(t.value for t in q_tokens)

                    section[attr_name] = tokens[idx + q_consumed].value

                    idx += q_consumed + 1
                    noaction = False

            if noaction:
                print tokens[idx:idx+5]
                raise Exception('Found a section unable to be parsed under {0} --> {1}'.format(parent.name, section.name))

            noaction = True

        return section

    def _parse(self, tokens):
        idx = 0
        ntokens = len(tokens)

        has_next = lambda: idx + 1 < ntokens
        get_next = lambda: tokens[idx + 1]
        noaction = False

        while idx < ntokens - 1:
            tok = tokens[idx]
            nxt = get_next()

            if tok.type in ['T_NAME', 'T_OBJ_PROP']:
                self.base_section.add_attribute(tok.value, nxt.value)
                idx += 2
            elif tok.type == 'SEC_START':
                matched, consumed = section_contents(tokens[idx:])
                name, _ = self._get_name_from_section(self.base_section, matched)

                self._section_indices[name] = {'start': idx,
                                               'end': idx + consumed + 1}

                idx += consumed

    def _load_section(self, name):
        indices = self._section_indices[name]
        subset = self.tokens[indices['start']:indices['end']]
        breakdown, _ = section_contents(subset)

        section = self._parse_section(self.base_section, breakdown)
        self.base_section.add_section(section)

        self._sections[name] = section

    def get_section(self, name):
        if name not in self._section_indices:
            raise IndexError('{0} is not a valid section'.format(name))

        if name not in self._sections:
            self._load_section(name)

        return self._sections[name]

    def find(self, section=None, filter=lambda sec: True):
        if section is None:
            sections = self._section_indices.keys()
        elif section in self._section_indices:
            sections = [section]
        else:
            raise IndexError('{} section does not exist'.format(section))

        def _dfs(sect, _criteria):
            if _criteria(sect):
                yield sect

            for s in sect.sections.values():
                if _criteria(s):
                    # print s
                    yield s

        for s in sections:
            for match in _dfs(self.get_section(s), filter):
                yield match

    def find_first(self, *args, **kwargs):
        return next(self.find(*args, **kwargs))

    def load(self, filename):
        self.tokens = self._tokenize(filename)

        section = Section('self')

        self.base_section = section
        self._parse(self.tokens)

        return section

    def save(self, filename):
        for k, section in self._section_indices.items():
            if k not in self._sections:
                self._load_section(k)

        with open(filename, 'w') as f:
            for line in self.base_section.generate_save_file_lines(first=True):
                f.write(line + '\n')
