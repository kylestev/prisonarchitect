from collections import OrderedDict


class Section(object):
    def __init__(self, name):
        self.name = name

        self.attrs = OrderedDict()
        self.sections = OrderedDict()

    def add_attribute(self, name, value):
        self.attrs[name] = value

    def add_section(self, section):
        self.sections[section.name] = section

    def generate_save_file_lines(self, first=False):
        section_name = self.name if ' ' not in self.name else '"{}"'.format(self.name)
        if not first:
            yield 'BEGIN {}'.format(section_name)

        spacing = (' ' * 4) if not first else ''

        for k, v in self.attrs.items():
            if ' ' in k:
                k = '"{}"'.format(k)

            yield spacing + '{}   {}'.format(k, v)

        for section in self.sections.values():
            for line in section.generate_save_file_lines():
                yield spacing + line

        if not first:
            yield 'END'

    def __repr__(self):
        return '<Section>(name={0}, attrs={1}, sections={2})'.format(self.name, self.attrs, self.sections)
