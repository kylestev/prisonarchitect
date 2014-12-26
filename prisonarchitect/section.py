class Section(object):
    def __init__(self, name):
        self.name = name

        self.attrs = {}
        self.sections = {}

    def add_attribute(self, name, value):
        self.attrs[name] = value

    def add_section(self, section):
        self.sections[section.name] = section

    def __repr__(self):
        return '<Section>(name={0}, attrs={1}, sections={2})'.format(self.name, self.attrs, self.sections)
