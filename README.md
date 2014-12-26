prisonarchitect
===============

Python module for accessing Prison Architect save files

## Example Usage

```python
from pprint import pprint

from prisonarchitect import PrisonParser

parser = PrisonParser()
section = parser.load('autosave.prison')
pprint(section.attrs)
pprint(section.sections.keys())

```
