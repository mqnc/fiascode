import sys
import os
import hashlib
from time import time
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley


def concat(elems):
	return ''.join(elems)

def exception(txt):
	raise SyntaxError(txt)
	return txt

class LoopCounter(): # for uniquely labeling escape goto targets
	c = 0;
	def inc_get(self):
		self.c += 1;
		return self.c;
loopcount = LoopCounter()
	
def hash(charlist): # for generating delimiters in raw strings
	return hashlib.md5(concat(charlist).encode("utf-8")).hexdigest()[0:10]	

	
def makeFor(iters, body, counter):

	res = '{\n'

	for ig in iters: # iterate through groups
	
		# initialization of iterators/indices before loop begins
		
		for it in ig: # iterate through iterators in group

			box = ""
			if it['asgn']['type'] == 'iterator':
				box = it['id'] + '__iterator'
				res += 'auto ' + box + ' = all(' + it['asgn']['iterator'] + ');\n'
				it['box'] = box
				
			if it['asgn']['type'] == 'index':
				box = it['id'] + '__index'				
				res += 'auto ' + box + ' = ' + it['asgn']['from'] + ';\n'
				it['box'] = box
		
		# begin of loop header
		
		res += 'for(; '
		
		# conditions for continue
		
		for it in ig: # iterate through iterators in group
			if it['asgn']['type'] == 'index':
				if it['asgn']['oper'] == '...':
					res += 'true /*' + it['id'] + ' loops forever*/ && '
				elif it['asgn']['oper'] == '=>':
					res += '!((' + it['box'] + ') == (' + it['asgn']['to'] + ')) && ';
			else:
				res += '!' + it['box'] + '.empty() && '
		res = res[:-4] # delete last " && "
		res += "; "
		
		# incrementing iterators/indices
		
		for it in ig: # iterate through iterators in group
			if it['asgn']['type'] == 'index':
				res += it['box'] + '++, '
			else:
				res += it['box'] + '.popFront(), '
		res = res[:-2] # delete last ", "
		res += '){\n'
		for it in ig: # iterate through iterators in group
			if it['asgn']['type'] == 'iterator':
				res += '\t auto &' + it['id'] + ' = ' + it['box'] + '.front();\n'
			else:
				res += '\t const auto &' + it['id'] + ' = ' + it['box'] + ';\n'
			
	# definition of exit jump		
			
	res += '#define Break goto loopend__' + str(counter) + '; // deal with it óo´\n\n'
	
	# loop body
	
	res += body
	
	# undef exit jump
	
	res += '\n\n#undef Break\n'
	
	for ig in iters: # iterate through groups
		res += '\n}\n'
	
	res += '\n}\n'
	res += 'loopend__' + str(counter) + ':\n'
	return res

	
	
	
def makeFn(name, qualis, input, output, body):

	res = ''
	if qualis==None: qualis=''
	
	# construct parameter struct for call with keyword parameters

	if len(input) != 0: 
		res += '#hdr\nstruct ' + name + '__params{\n'
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += '; '
		res += '};\n#end\n'
	
	if isinstance(output, str): 
	
		# output is a string, not a list -> no multi-value struct for return
	
		res += qualis + ' ' + output + ' ' + name + '('
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n\n'
		res += body + '\n\n}\n'
	
	else:	
		
		# construct return struct
	
		res += 'struct ' + name + '__result{'
		for par in output:
			res += 'const ' + par['decl'] + '; '
		res += '};\n'
		
		# head: qualifiers, return type and function name
		
		res += qualis + ' ' + name + '__result ' + name + '('
		
		# input parameters
		
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n'
		
		# initialize return values and assign default values if defined
		
		for par in output:
			res += '\t' + par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ';\n'
		
		# function body
		
		if body != '':
		
			# return statement
		
			res += '#define Return return {' # ugly hack until I todo this properly
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
			res += body + '\n'
			res += '\tReturn\n#undef Return\n'
		
		else:
		
			# no actual body (assigning default values was enough)
		
			res += '\treturn {'
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
		res += '}\n'
	
	
	# construct overloaded definition for call with keyword parameters
	
	if len(input) != 0 and name!='main': 
		res += qualis + ' '
		if isinstance(output, str):
			res += output + ' '
		else:
			res += name + '__result '
		res += name + '(' + name + '__params const& args) {\n'
		res += '\treturn ' + name + '('
		for par in input:
			res += 'args.' + par['id'] + ', '
		res = res[:-2]; # delete last comma
		res += ');}'
	
	return res


	
#def makeCall:

	
t0 = time()

grammar = parsley.makeGrammar(r"""

##########
# Basics #
##########

code = symbol*:s -> '#hdr\n#include "cpype.h"\n#end\n' + concat(s)

symbol       = known_symbol | identifier | anything # anything is defined as any character by parsley
known_symbol = (comment | string | substitution | group | stray)
stray        = (group_stray | if_stray | fn_stray | loop_stray | switch_stray):estray -> exception('Stray ' + estray + ' detected')
ws = (' ' | '\t' | '\r' | '\n' | comment)*:space -> concat(space)
group       = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' symbol)*:body ')' -> '(' + concat(body) + ')'
bracketed   = '[' (~']' symbol)*:body ']' -> '[' + concat(body) + ']'
braced      = '{' (~'}' symbol)*:body '}' -> '{' + concat(body) + '}'
group_stray = (')' | ']' | '}')
identifier  = <(letter | '_') (letter | '_' | digit)*>

substitution = declaration | branch_statement | loop_statement | function_statement | keyword_call # actual language grammar 

# Comments
# --------

comment        = (comment1 | comment2 | comment3)
comment1       = <'/*' (~'*/' anything)* '*/'>
comment2       = '//' (~'\n' anything)*:cmt '\n' -> '/*' + concat(cmt) + '*/\n' # lzz sometimes deletes line breaks
comment3       = '\\*' (~'*\\' (inner_comment3 | anything))*:cmt '*\\' -> '/*' + concat(cmt) + '*/'
inner_comment3 = '\\*' (~'*\\' (inner_comment3 | anything))*:cmt '*\\' -> '/*' + concat(cmt) + '* /'

# Strings
# -------

string = simple_string | naked_raw_string | raw_string_with_delimiter | utf8_raw_string

simple_string             = <'"' (escaped | ~'"' anything)* '"'>
escaped                   = <'\\' anything> # represents one backslash
naked_raw_string          = <'R"(' (~')"' anything)* ')"'>
raw_string_with_delimiter = <'R"' (~'(' anything)*:delim (~(')' token(delim) '"') anything)* ')' token(delim) '"'>
utf8_raw_string           = '°°' (~'°°' anything)*:txt '°°' -> 'u8R"' + hash(txt) + '(' + concat(txt) + ')' + hash(txt) + '"'


#############
# Variables #
#############

declaration = val_declaration | var_declaration

val_declaration = 'Val' -> 'const auto'
var_declaration = 'Var' -> 'auto'


############
# Branches #
############

branch_statement = if_statement | switch_statement

# If Then
# -------

if_statement     = 'If'     if_condition:cond 'Then'   if_body:body (elseif_statement | else_statement | endif_statement):tail ->      'if(' + cond + '){' + concat(body) + '}' + tail
elseif_statement = 'Elseif' if_condition:cond 'Then'   if_body:body (elseif_statement | else_statement | endif_statement):tail -> 'else if(' + cond + '){' + concat(body) + '}' + tail
else_statement   = 'Else'                            else_body:body                                      endif_statement :tail -> 'else{'                  + concat(body) + '}' + tail
endif_statement  = 'Endif' -> ''
if_condition     = (~'Then' symbol)*:cond -> concat(cond)
if_body          = (~('Elseif' | 'Else' | 'Endif') symbol)*:body -> concat(body)
else_body        = (~'Endif' symbol)*:body -> concat(body)
if_stray         = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first

# Switch Case
# -----------

switch_statement     = 'Switch' switch_condition:cond switch_body:body 'Endswitch' -> 'switch(' + cond + '){\n' + body + '\n}'
switch_condition     = (~('Case' | 'Default' | 'Endswitch') symbol)*:cond -> concat(cond)
switch_body          = (case | default)*:body -> concat(body)
case                 = 'Case' case_condition_group:cond 'Do' case_body:body case_end:end -> cond + '\n\t' + body + '\n' + end
default              = 'Default' case_body:body -> '\n' 'default: ' + body
case_condition_group = case_condition:first (',' ws case_condition)*:rest ws -> ' '.join([first] + rest)
case_condition       = (~('Do' | ',') symbol)*:cond -> 'case ' + concat(cond) + ':'
case_body            = (~('Case' | 'Fall' | 'Default' | 'Endswitch')symbol)*:body -> concat(body)
case_end             = ('Fall' ws -> '') | (ws -> 'break;')
switch_stray         = ('Case' | 'Default' | 'Fall' | 'Endswitch' | 'Do')


#########
# Loops #
#########

loop_statement = for_statement | while_statement | repeat_statement

# For Loop
# --------

for_statement       = 'For' iterator_list:iters 'Do' for_body:body 'Loop' -> makeFor(iters, body, loopcount.inc_get())
iterator_list       = ws iterator_item:first ws (',' ws iterator_item)*:rest -> [first] + rest
iterator_item       = (iterator_group:iter -> iter) | (iterator:iter -> [iter])
iterator_group      = '[' iterator:first (',' ws iterator)*:rest ']' ws -> [first] + rest
iterator            = identifier:id ws ':' ws iterator_assignment:asgn -> {'id':id, 'asgn':asgn}
iterator_assignment = index | range_iterator
index               = index_from:frm index_operator:oper index_to:to -> {'type':'index', 'from':frm, 'oper':oper, 'to':to}
index_from          = (~(index_operator | ',' | ']' | 'Do')symbol)*:iter -> concat(iter) # ',' | ']' | 'Do' has to be matched in order to break out when we are actually in "range_iterator"
index_operator      = ('...' | '=>')
index_to            = (~(',' | 'Do' | ']')symbol)*:iter -> concat(iter)
range_iterator      = (~(',' | 'Do' | ']')symbol)*:asgn -> {'type':'iterator', 'iterator':concat(asgn)}
for_body            = (~'Loop' symbol)*:body -> concat(body)

# While / Repeat
# --------------

while_statement  = 'While' (~'Do' symbol)*:cond 'Do' (~'Loop' symbol)*:body 'Loop' -> 'while(' + concat(cond) + '){\n' + concat(body) + '}'
repeat_statement = 'Repeat' (~('Until' | 'Whilst')symbol)*:body (until_condition | whilst_condition):cond 'Loop' -> 'do{\n' + concat(body) + '\n}while(' + cond + ');'
until_condition  = 'Until' (~('Loop')symbol)*:cond -> '!(' + concat(cond) + ')'
whilst_condition = 'Whilst' (~('Loop')symbol)*:cond -> concat(cond)
loop_stray       = ('Do' | 'Until' | 'Whilst' | 'Loop')


#############
# Functions #
#############

function_statement   = 'Fn' ws identifier:name ws qualifiers?:qualis ws input_parameters:input ws return_values:output ws function_body:body 'Endfn'-> makeFn(name, qualis, input, output, body)
qualifiers           = '[' (~']' symbol)*:qualis ']' -> concat(qualis)
input_parameters     = ('(' fn_parameter_list:input ')' | ws:input) -> input
return_values        = ('->' ws '(' fn_parameter_list:output ')' -> output) | ('->' ws return_type:output -> concat(output)) | (ws -> 'void')
fn_parameter_list    = fn_parameter:first (',' fn_parameter)*:rest -> [first] + rest if first!=[] else []
fn_parameter         = ws (~(')' | ',' | '=')(known_symbol | identifier:id | anything))*:decl ('=' parameter_assignment)?:asgn -> {'decl':concat(decl), 'id':id, 'asgn':asgn} if decl != [] else []
return_type          = ws (~(':=' | 'Endfn')symbol)*:type -> type
parameter_assignment = (~(')' | ',')symbol)*:asgn -> concat(asgn)
function_body        = (':=' (~'Endfn' symbol)*:body -> concat(body)) | (ws -> '')
fn_stray             = ('->' | ':=' | 'Endfn')

keyword_call         = ~('for' ws '(') identifier:fname ws '(' ws key_parameter_list:params ')' -> str({'fname':fname, 'params':params})
key_parameter_list   = (par_and_comma)*:rest key_parameter:last -> rest + [last]
par_and_comma        = maybe_key_parameter:par ',' -> par
maybe_key_parameter  = key_parameter | position_parameter
key_parameter        = ws identifier:id ws ':' ws parameter_assignment:asgn -> {'tpye':'key', 'id':id, 'asgn':asgn}
position_parameter   = ws parameter_assignment:asgn -> {'tpye':'pos', 'asgn':asgn}

""", {'concat':concat, 'exception':exception, 'makeFor':makeFor, 'loopcount':loopcount, 'makeFn':makeFn, 'hash':hash})

def prettify(input):
	input = input.replace('\r\n', '\n')
	input = input.replace('\r', '\n')
	
	input = '   \n' + input + '\n   ' # so indices don't overflow
	output = ''
	tab = 0
	i = 0
	imax = len(input)-2
	while i <= imax:
		c1 = input[i]
		c12 = c1 + input[i+1]
		
		if c12 == '//': # we are inside a // comment, continue until it's over
			while i<imax and input[i] != '\n':
				output += input[i]
				i+=1
			output += input[i]
			i+=1			
			continue
			
		if c12 == '/*': # we are inside a /* */ comment, continue until it's over
			while i<imax and input[i] + input[i+1] != '*/':
				output += input[i]
				i+=1
			output += input[i] + input[i+1]
			i+=2
			continue
			
		if c12 == 'R"': # we are inside a raw string literal, continue until it's over
			#output += "S2<"
			delim = ""
			output += c12
			i+=2
			while i<imax and input[i] != '(':
				delim += input[i]
				output += input[i]
				i+=1
			endpos = input.find(')' + delim + '"', i) + len(delim) + 2
			output += input[i:endpos]
			i = endpos
			#output += ">S2"
			continue
			
		if c1 == '"': # we are inside a normal string, continue until it's over
			#output += "S1<"
			output += c1
			i+=1
			while i<imax and input[i] != '"' or input[i-1] == '\\':
				output += input[i]
				i+=1
			output += '"'
			i+=1
			#output += ">S1"
			continue
			
		if c1 == '{' or c1 == '(': # increase tab indent
			tab += 1
			
		if c1 == '}' or c1 == ')': # decrease tab indent
			tab -= 1
			
		if c1 == '\n': # line break, add tabs
			while i<imax and (input[i+1] == ' ' or input[i+1] == '\t' or input[i+1] == '\n'):
				i+=1
			tempback = 0
			if input[i+1] == ')' or input[i+1] == '}':
				tempback = 1

			output += '\n'
			for it in range(tab-tempback):
				output += '\t'
			i+=1
			continue
		
		output += input[i]
		i+=1
	return output

print("Grammar compilation time in s")
print(time()-t0)

def translate(target, source, env):

	t0=time()

	#with open(sys.argv[1], encoding='utf-8') as fin:
	with open(str(source[0]), encoding='utf-8') as fin:
		incode = fin.read()

	translated = prettify(grammar(incode).code())

	#with open(sys.argv[2], 'w', encoding='utf-8') as fout:
	with open(str(target[0]), 'w', encoding='utf-8') as fout:
		fout.write(translated)

	print("Translation time in s")
	print(time()-t0)
	
	return None



