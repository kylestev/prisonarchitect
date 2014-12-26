prisonarchitect
===============

Python module for accessing Prison Architect save files

## Example Usage

```python
from pprint import pprint

from prisonarchitect import PrisonParser

parser = PrisonParser()
base = parser.load('autosave.prison')
print base['Intake.numPrisoners'], 'new prisoners'
base['CeoLetterRead'] = 'false'
parser.save('autosave.prison')

```
