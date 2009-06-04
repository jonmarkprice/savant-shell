import ply.lex as lex
import sys

# mapping of reserved words to tokens

reserved = {
'this' : 'THIS',
'new' : 'NEW',
'folder' : 'FOLDER',
'file' : 'FILE',
'delete' : 'DELETE',
'show' : 'SHOW',
'copy' : 'COPY',
'zip' : 'ZIP',
'to' : 'TO',
'move' : 'MOVE',
'sort' : 'SORT',
'by' : 'BY',
'name' : 'STR_NAME',
'type' : 'STR_TYPE',
'time' : 'STR_TIME',
'files' : 'FILES',
'matching' : 'MATCHING',
'accessed' : 'ACCESSED',
'and' : 'AND',
'or' : 'OR',
'modified' : 'MODIFIED',
'today' : 'TODAY',
'yesterday' : 'YESTERDAY',
'last' : 'LAST',
'before' : 'BEFORE',
'after' : 'AFTER',
'between' : 'BETWEEN',
'and' : 'AND',
'year' : 'YEAR',
'days' : 'DAYS',
'weeks' : 'WEEKS',
'months' : 'MONTHS',
'years' : 'YEARS',
'week' : 'WEEK',
'month' : 'MONTH'
	   
}

# List of token names.   This is always required
tokens = [

	'NAME',
	'NUMBER',

] + list(reserved.values())



# A regular expression rule with some action code


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
	return t


def t_NAME(t):
	r'[\w.]+'
	t.type = reserved.get(t.value,'NAME')    # if its a reserved word, assign it, otherwise its NAME
	return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()





















