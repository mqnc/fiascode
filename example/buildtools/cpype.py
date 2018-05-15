import sys
import os
import hashlib
from time import time
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py


def exception(txt):
	raise SyntaxError(txt)
	return txt


class LoopCounter():
	c = 0;
	def inc_get(self):
		self.c += 1;
		return self.c;
loopcount = LoopCounter()
	
def makefor(iters, body, counter):

	res = '{\n'
	res += 'bool break_nesting = false;\n'

	for ig in iters: # iterate through groups
		for it in ig: # iterate through iterators in group
			asgn = it['asgn'];
			var = it['id'];
		
			if asgn['type'] == 'set':
				range = var + '__range'
				res += 'auto ' + range + ' = all(' + asgn['set'] + ');\n'
				it['range'] = range
				
			if asgn['type'] == 'range':
				range = var + '__range'				
				
				if asgn['oper'] == '|...' or asgn['oper'] == '|...':	
					res += 'auto ' + range + ' = all(' + asgn['from'] + ', ' + asgn['from'] + ');\n' # from, from
				else:
					res += 'auto ' + range + ' = all(' + asgn['from'] + ', ' + asgn['to'] + ');\n' # from, to
			
				if(asgn['oper'] == '..'):
					res += range + '.pushEnd();\n';
				if(asgn['oper'] == '|..'):
					res += range + '.popFront();\n';
					res += range + '.pushEnd();\n';					
				if(asgn['oper'] == '..|'):
					pass
				if(asgn['oper'] == '|..|'):
					res += range + '.popFront();\n';
				if(asgn['oper'] == '|...'):
					res += range + '.popFront();\n';
				if(asgn['oper'] == '...'):
					pass
					
				it['range'] = range				
			
		res += 'for(; '
		for it in ig: # iterate through iterators in group
			if(it['asgn']['type'] == 'range' and (it['asgn']['oper'] == '...' or it['asgn']['oper'] == '|...')):
				res += 'true /*' + it['id'] + ' loops forever*/ && '
			else:
				res += '!' + it['range'] + '.empty() && '
		res = res[:-4] # delete last " && "
		res += "; "
		for it in ig: # iterate through iterators in group
			res += it['range'] + '.popFront(), '
		res = res[:-2] # delete last ", "
		res += '){\n'
		for it in ig: # iterate through iterators in group
			res += '\t auto &' + it['id'] + ' = ' + it['range'] + '.front();\n'
			
	res += '#define Break goto loopend__' + str(counter) + ';\n\n'
	res += body
	res += '\n\n#undef Break\n'
	
	for ig in iters: # iterate through groups
		res += '\n}\n'
	
	res += '\n}\n'
	res += 'loopend__' + str(counter) + ':\n'
	return res

def makefn(name, qualis, input, output, body):

	res = ''
	if qualis==None: qualis=''
	
	if isinstance(output, str): # output is a string, not a list -> no struct for return
		res = qualis + ' ' + output + ' ' + name + '('
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n\n'
		res += body + '\n\n}\n'
	
	else:
		res = 'struct ' + name + '__result{'
		for par in output:
			res += par['decl'] + '; '
		res += '};\n'
		res += qualis + ' ' + name + '__result ' + name + '('
		for par in input:
			res += par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ', '
		if len(input) != 0: res = res[:-2]; # delete last comma
		res += '){\n'
		for par in output:
			res += '\t' + par['decl']
			if par['asgn'] != None: res += '=' + par['asgn']
			res += ';\n'
		
		if body != '':
		
			res += '#define Return return {' # ugly hack until I todo this properly
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
			res += body + '\n'
			res += '\tReturn\n#undef Return\n'
		
		else:
			res += '\treturn {'
			for par in output:
				res += par['id'] + ', '
			if len(output) != 0: res = res[:-2]; # delete last comma
			res += '};\n'
			
		res += '}\n'
	
	return res

def hash(charlist):
	return hashlib.md5(''.join(charlist).encode("utf-8")).hexdigest()[0:10]
	
t0 = time()

fiascode = parsley.makeGrammar(r"""

code = symbol*:s -> '#include "cpype.h"\n' + ''.join(s)

symbol = knownsymbol | identifier | anything
knownsymbol = (comment | string | substitution | group | stray)
stray = (groupstray | ifstray | fnstray | loopstray | switchstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2 | comment3)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = '//' (~'\n' anything)*:cmt '\n' -> '/*' + ''.join(cmt) + '*/\n' # lzz sometimes deletes line breaks
comment3 = '\\*' (~'*\\' (innercomment3 | anything))*:cmt '*\\' -> '/*' + ''.join(cmt) + '*/'
innercomment3 = '\\*' (~'*\\' (innercomment3 | anything))*:cmt '*\\' -> '/*' + ''.join(cmt) + '* /'

ws = (' ' | '\t' | '\r' | '\n' | comment)*:space -> ''.join(space)

string = simplestring | nakedrawstring | delimrawstring | superstring

simplestring = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\' anything> # represents one backslash
nakedrawstring = <'R"(' (~')"' anything)* ')"'>
delimrawstring = <'R"' (~'(' anything)*:delim (~(')' token(delim) '"') anything)* ')' token(delim) '"'>
superstring = '°°' (~'°°' anything)*:txt '°°' -> 'u8R"' + hash(txt) + '(' + ''.join(txt) + ')' + hash(txt) + '"'

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' symbol)*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' symbol)*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' symbol)*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = branchstmt | loopstmt | functionstmt # actual language grammar 


branchstmt = ifstmt | switchstmt

ifstmt     = 'If'     ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                           elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''
ifcondition = (~'Then' symbol)*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') symbol)*:body -> ''.join(body)
elsebody  = (~'Endif' symbol)*:body -> ''.join(body)
ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first

switchstmt = 'Switch' switchcondition:cond switchbody:body 'Endswitch' -> 'switch(' + cond + '){\n' + body + '\n}'
switchcondition = (~('Case' | 'Default' | 'Endswitch') symbol)*:cond -> ''.join(cond)
switchbody = (case | default)*:body -> ''.join(body)
case = 'Case' caseconditiongroup:cond 'Do' casebody:body caseend:end -> cond + '\n\t' + body + '\n' + end
default = 'Default' casebody:body -> '\n' 'default: ' + body
caseconditiongroup = casecondition:first (',' ws casecondition)*:rest ws -> ' '.join([first] + rest)
casecondition = (~('Do' | ',') symbol)*:cond -> 'case ' + ''.join(cond) + ':'
casebody = (~('Case' | 'Fall' | 'Default' | 'Endswitch')symbol)*:body -> ''.join(body)
caseend = ('Fall' ws -> '') | (ws -> 'break;')
switchstray = ('Case' | 'Default' | 'Fall' | 'Endswitch' | 'Do')


loopstmt = forstmt | whilestmt | repeatstmt

forstmt = 'For' iteratorlist:iters 'Do' forbody:body 'Loop' -> makefor(iters, body, loopcount.inc_get())
iteratorlist = ws iteratoritem:first ws (',' ws iteratoritem)*:rest -> [first] + rest
iteratoritem = (iteratorgroup:iter -> iter) | (iterator:iter -> [iter])
iteratorgroup = '[' iterator:first (',' ws iterator)*:rest ']' ws -> [first] + rest
iterator = identifier:id ws ':' ws iterassignment:asgn -> {'id':id, 'asgn':asgn}
iterassignment = rangeiterator | otheriterator
rangeiterator = rangefrom:frm rangeoperator:oper rangeto:to -> {'type':'range', 'from':frm, 'oper':oper, 'to':to}
rangefrom = (~(rangeoperator | ',' | ']' | 'Do')symbol)*:iter -> ''.join(iter) # ',' | ']' | 'Do' has to be matched in order to break out when we are actually in "otheriterator"
rangeoperator = ('|..|' | '|...' | '|..' | '..|' | '...' | '..')
rangeto = (~(',' | 'Do' | ']')symbol)*:iter -> ''.join(iter)
otheriterator = (~(',' | 'Do' | ']')symbol)*:asgn -> {'type':'set', 'set':''.join(asgn)}
forbody = (~'Loop' symbol)*:body -> ''.join(body)

whilestmt = 'While' (~'Do' symbol)*:cond 'Do' (~'Loop' symbol)*:body 'Loop' -> 'while(' + ''.join(cond) + '){\n' + ''.join(body) + '}'
repeatstmt = 'Repeat' (~('Until' | 'Whilst')symbol)*:body (untilcond | whilstcond):cond 'Loop' -> 'do{\n' + ''.join(body) + '\n}while(' + cond + ');'
untilcond = 'Until' (~('Loop')symbol)*:cond -> '!(' + ''.join(cond) + ')'
whilstcond = 'Whilst' (~('Loop')symbol)*:cond -> ''.join(cond)
loopstray = ('Do' | 'Until' | 'Whilst' | 'Loop')


functionstmt = 'Fn' ws identifier:name ws qualifiers?:qualis ws inputpars:input ws outputpars:output ws fnbody:body 'Endfn'-> makefn(name, qualis, input, output, body)
qualifiers = '[' (~']' symbol)*:qualis ']' -> ''.join(qualis)
inputpars = ('(' parameterlist:input ')' | ws:input) -> input
outputpars = ('->' ws '(' parameterlist:output ')' -> output) | ('->' ws returntype:output -> ''.join(output)) | (ws -> 'void')
parameterlist = parameter:first (',' parameter)*:rest -> [first] + rest if first!=[] else []
parameter = ws (~(')' | ',' | '=')(knownsymbol | identifier:id | anything))*:decl ('=' parassignment)?:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
returntype = ws (~(':=' | 'Endfn')symbol)*:type -> type
parassignment = (~(')' | ',')symbol)*:asgn -> ''.join(asgn)
fnbody = (':=' (~'Endfn' symbol)*:body -> ''.join(body)) | (ws -> '')
fnstray = ('->' | ':=' | 'Endfn')

""", {'exception':exception, 'makefor':makefor, 'loopcount':loopcount, 'makefn':makefn, 'hash':hash})

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
t0=time()

with open(sys.argv[1], encoding='utf-8') as fin:
	incode = fin.read()
fin.closed

translated = prettify(fiascode(incode).code())

with open(sys.argv[2], 'w', encoding='utf-8') as fout:
	fout.write(translated)
fin.closed

print("Translation time in s")
print(time()-t0)


