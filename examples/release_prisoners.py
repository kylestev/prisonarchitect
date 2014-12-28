from prisonarchitect import PrisonLoader

with PrisonLoader('autosave.prison') as parser:
    def prisoner_filter(section):
        return section.attrs.get('Type', None) == 'Prisoner'

    for prisoner in parser.find(section='Objects', filter=prisoner_filter):
        bio = prisoner.sections['Bio']
        bio['Served'] = bio['Sentence']

    # implicit save on exiting the context.
