from collections import OrderedDict


class Section(object):
    def __init__(self, name):
        self.name = name

        self.attrs = OrderedDict()
        self.sections = OrderedDict()

    def __contains__(self, key):
        return key in self.attrs

    def __delitem__(self, key):
        if key not in self:
            raise IndexError('{} is not an attribute'.format(key))

        del self.attrs[key]

    def __getitem__(self, key):
        if key not in self:
            raise IndexError('{} is not an attribute'.format(key))

        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def add_attribute(self, name, value):
        if name not in self.attrs:
            self.attrs[name] = []

        self.attrs[name].append(value)

    def add_section(self, section):
        self.sections[section.name] = section

    def generate_save_file_lines(self, first=False):
        section_name = self.name if ' ' not in self.name else '"{}"'.format(self.name)
        if not first:
            yield 'BEGIN {}'.format(section_name)

        spacing = (' ' * 4) if not first else ''

        def _format_attr_pair(key, value):
            if ' ' in key:
                key = '"{}"'.format(key)

            if ' ' in value:
                value = '"{}"'.format(value)

            return spacing + '{}   {}'.format(key, value)

        for k, v in self.attrs.items():
            for val in v:
                yield _format_attr_pair(k, val)



        for section in self.sections.values():
            for line in section.generate_save_file_lines():
                yield spacing + line

        if not first:
            yield 'END'

    def __repr__(self):
        return '<Section>(name={0}, attrs={1}, sections={2})'.format(self.name, self.attrs, self.sections)
