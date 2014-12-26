prisonarchitect
===============

Python module for accessing Prison Architect save files

## Example Usage

```python
from pprint import pprint

from prisonarchitect import PrisonParser

parser = PrisonParser()
base = parser.load('autosave.prison')
print base.attrs['Intake.numPrisoners'], 'new prisoners for next intake!'
base.attrs['CeoLetterRead'] = 'false'
parser.save('autosave.prison')

```
