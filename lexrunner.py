from savant_lexer import lexer

while True:
	try:
		s = raw_input('lex > ')
	except EOFError:
		break
	if not s: continue
	lexer.input(s)
	for tok in lexer:
		print tok
		print " "


