import ply.yacc as yacc
import os
import time
import os.path
import sys
import re
from datetime import date
from datetime import timedelta

from savant_lexer import tokens



if len(sys.argv) >= 2:
	if os.path.exists(sys.argv[1]):
		currentDir = sys.argv[1]
		print currentDir + "\n"

	else:
		currentDir = os.getcwd()
		print "invalid path: defaulting to: " + currentDir

	selection = ""
	if len(sys.argv) >= 3:
		selection = sys.argv[2:]
		print selection

else:
	currentDir = os.getcwd()
	print "no path provided: defaulting to: " + currentDir


os.chdir(currentDir) # changes directory to the current directory


# Start Symbol

def p_start_new(p):
	'start : newItem' 
	p[0] = p[1]

def p_start_show(p):
	'start : showItem' 
	p[0] = p[1]

def p_start_copy(p):
	'start : copyItem' 
	p[0] = p[1]

def p_start_move(p):
	'start : moveItem' 
	p[0] = p[1]

def p_start_zip(p):
	'start : zipItem'
	p[0] = p[1]


def p_start_sort(p):
	'start : sortItem' 
	p[0] = p[1]

def p_start_delete(p):
	'start : deleteItem' 
	p[0] = p[1]

# New File/Folder Rules

def p_newItem_file(p):
	'newItem : NEW FILE NAME'
	os.system('echo \"\" >' + p[3])
	p[0] = ""


def p_newItem_folder(p):
	'newItem : NEW FOLDER NAME'
	os.system('mkdir ' + p[3])
	p[0] = p[3] + "/"


# Delete Rules

def p_deleteItem_query(p):
	'deleteItem : DELETE query'
	os.system('rm -rf ' + p[2])
	p[0] = ""


# Show Rules

def p_showItem_query(p):
	'showItem : SHOW query'
	p[0] = p[2]


# Copy Rules


def p_copyItem_folder(p):
	'copyItem : COPY query TO newItem'
	os.system('cp -r ' + p[2] + ' ' + p[4])
	p[0] = ""

def p_copyItem_query(p):
	'copyItem : COPY query TO NAME'
	os.system('cp -r ' + p[2] + ' ' + p[4])	
	p[0] = ""

def p_moveItem_folder(p):
	'moveItem : MOVE query TO newItem'
	os.system('mv ' + p[2] + ' ' + p[4])	
	p[0] = ""


def p_moveItem_query(p):
	'moveItem : MOVE query TO NAME'
	os.system('mv ' + p[2] + ' ' + p[4])
	p[0] = ""


def p_zipItem_query(p):
	'zipItem : ZIP query TO NAME'
	os.system('zip -r ' + p[4] + ' ' + p[2])
	p[0] = ""


# Sort Rules

def p_sortItem_name(p):
	'sortItem : SORT BY STR_NAME'
	p[0] = "\n".join(sorted(os.listdir(currentDir)))

def p_sortItem_time(p):
	'sortItem : SORT BY STR_TIME'
	p[0] = "\n".join(sorted((os.listdir(currentDir)), (lambda a, b : get_mtime_sec(b) - get_mtime_sec(a)) ) )

def p_sortItem_type(p):
	'sortItem : SORT BY STR_TYPE'
	p[0] = "\n".join(sorted((os.listdir(currentDir)), (lambda a, b : cmp(os.path.splitext(a)[1] , os.path.splitext(b)[1])) ) )



def p_query_this(p):
	'query : THIS'
	p[0] = " ".join(selection)


# Query Combination Rules


def p_query_query(p):
	'query : query query'
	set1 = set(p[1].split(' '))
	set2 = set(p[2].split(' '))
	result = set1 & set2
	p[0] = " ".join(result)


def p_query_and_query(p):
	'query : query AND query'
	set1 = set(p[1].split(' '))
	set2 = set(p[3].split(' '))
	result = set1 & set2
	p[0] = " ".join(result)


def p_query_or_query(p):
	'query : query OR query'
	set1 = set(p[1].split(' '))
	set2 = set(p[3].split(' '))
	result = set1 | set2	
	p[0] = " ".join(result)
	




def p_query_filetype(p):
	'query : NAME FILES'
	
	ext2 = '.' + p[1]

	result = filter(lambda f: (os.path.splitext(f)[1] == ext2), os.listdir(currentDir))
	p[0] = " ".join(result)



def p_query_filename(p):
	'query : NAME'
	

	result = filter(lambda f: (f==p[1]),os.listdir(currentDir))
	p[0] = " ".join(result)

	if os.path.exists(p[1]): # try as a path
		if os.path.isfile(p[1]):		
			p[0] = p[1]


# doesnt work 100 %, behaves like starts with

def p_query_regex(p):
	'query : MATCHING NAME'
	
	result = filter(lambda f: (re.match(p[2], f) != None)  ,os.listdir(currentDir))
	p[0] = " ".join(result)
	
	


def p_query_modified(p):
	'query : MODIFIED time'

	result = filter(lambda f: eval(p[2]), os.listdir(currentDir))
	p[0] = " ".join(result)


# Time Rules

months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def p_time_range(p):
	'time : range'
	p[0] = p[1]

def p_time_unit(p):
	'time : unit'
	p[0] = "(get_mtime(f)==get_date(\"" + p[1] + "\"))"


# Unit Time Rules

def get_mtime(filename):
	t = os.stat(filename)[8]
	return get_date(time.ctime(t))

def get_mtime_sec(filename):
	return os.stat(filename)[8]


# given a string representation of datetime, returns the tuple (year, month, day)
def get_date(t):
	return time.strptime( t, "%a %b %d %H:%M:%S %Y")[0:3]

def p_unit_today(p):
	'unit : TODAY'
	p[0] = date.today().ctime()

def p_unit_yesterday(p):
	'unit : YESTERDAY'
	p[0] = (date.today() - timedelta(days=1)).ctime()

def p_unit_number_month(p):
	'unit : NUMBER NAME'
	m = filter(lambda s: s.startswith(p[2]), months)[0]
	p[0] = date(date.today().year, months.index(m)+1 ,p[1]).ctime() # check if p[2] is a month

def p_unit_month_number(p):
	'unit : NAME NUMBER'
	m = filter(lambda s: s.startswith(p[1]), months)[0]
	p[0] = date(date.today().year, months.index(m)+1 ,p[2]).ctime()	# check if p[1] is month

def p_unit_day(p):
	'unit : NAME'
	t1 = date.today().weekday()
	day = filter(lambda s: s.startswith(p[1]), days)[0]
	t2 = days.index(day)
	diff = t1-t2
	if(diff < 0):
		diff += 7

	p[0] = (date.today() - timedelta(days=diff)).ctime()



# Range Time Rules


def p_range_last_span(p):
	'range : LAST span'
	p[0] = p[2]

def p_range_before_unit(p):
	'range : BEFORE unit'
	p[0] = "(get_mtime(f) < get_date(\"" + p[2] + "\"))"

def p_range_after_unit(p):
	'range : AFTER unit'
	p[0] = "(get_mtime(f) > get_date(\"" + p[2] + "\"))"

def p_range_between_unit(p):
	'range : BETWEEN unit AND unit'
	p[0] = "((get_mtime(f) > get_date(\"" + p[2] + "\")) and (get_mtime(f) < get_date(\"" + p[4] + "\")))"


# Time Span Rules

def get_date_diff(delta):
	return (date.today() - delta).ctime()

def p_span_week(p):
	'span : WEEK'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(weeks=1)) + "\"))"

def p_span_month(p):
	'span : MONTH'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(days=30)) + "\"))"

def p_span_year(p):
	'span : YEAR'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(days=365)) + "\"))"

def p_span_number_days(p):
	'span : NUMBER DAYS'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(days=p[2])) + "\"))"

def p_span_number_weeks(p):
	'span : NUMBER WEEKS'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(weeks=p[2])) + "\"))"

def p_span_number_months(p):
	'span : NUMBER MONTHS'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(days=30*p[2])) + "\"))"

def p_span_number_years(p):
	'span : NUMBER YEARS'
	p[0] = "(get_mtime(f) > get_date(\"" + get_date_diff(timedelta(days=365*p[2])) + "\"))"



# Build the parser
parser = yacc.yacc()


# Show prompt
while True:
   try:
       s = raw_input('savant > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print result

