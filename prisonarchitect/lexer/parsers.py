from prisonarchitect.lexer.tokens import Token


def matches_between(tokens, t_start, t_end):
	if not tokens or tokens[0].type != t_start:
		return None, 0

	i = 1
	matched = []
	while i < len(tokens):
		if tokens[i].type == t_end:
			i += 1
			break
		elif tokens[i].type == t_start and t_start != t_end:
			m, ml = matches_between(tokens[i:], t_start, t_end)
			matched.append(m)
			i += ml
			continue

		matched.append(tokens[i])

		i += 1

	return matched, i


def read_quote(tokens):
	return matches_between(tokens, 'T_QUOTE', 'T_QUOTE')


def section_name(tokens):
	if tokens[0].type == 'T_NAME':
		return [tokens[0]], 1

	return read_quote(tokens)


def section_contents(tokens):
	return matches_between(tokens, 'SEC_START', 'SEC_END')

