from collections import namedtuple

Token = namedtuple('Token', ['value', 'type'])


float_re = (r'^\d+\.\d+$', 'V_FLOAT') # before int
int_re = (r'^\d+$', 'V_INT')
bool_re = (r'^(true|false)$', 'V_BOOL')

section_begin_re = (r'^BEGIN$', 'SEC_START')
section_end_re = (r'^END$', 'SEC_END')

name_mixin = r'([A-Za-z0-9]+(?:[A-Za-z0-9_]*)*)'

name_re = (r'^{0}$'.format(name_mixin), 'T_NAME')
obj_prop_re = (r'^{0}((?:\.[a-zA-Z\d_]*)+)$'.format(name_mixin), 'T_OBJ_PROP')
quote_re = (r'^"$', 'T_QUOTE')

atom_re = (r'^.+$', 'V_ATOM') # last, catch-all


parse_order = [float_re, int_re, bool_re,
               section_begin_re, section_end_re,
               name_re, obj_prop_re, quote_re,
               atom_re]
