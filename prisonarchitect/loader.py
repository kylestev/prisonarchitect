from prisonarchitect import PrisonParser

class PrisonLoader(object):
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self._parser = PrisonParser()
        self._parser.load(self.filename)
        return self._parser

    def __exit__(self, type, value, traceback):
        self._parser.save(self.filename)
