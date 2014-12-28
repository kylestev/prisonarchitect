from prisonarchitect import PrisonParser

parser = PrisonParser()
parser.load('autosave.prison')

for prisoner in parser.find(section='Objects', filter=lambda sec: sec.attrs.get('Type', None) == 'Prisoner'):
    bio = prisoner.sections['Bio']
    bio['Served'] = bio['Sentence']

parser.save('autosave.prison')
