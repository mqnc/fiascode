import sys
import os
import hashlib
from time import time
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py

# todos:
# handle mean string literals both in parser and in prettify
# handle keywords like static/inline/stuff
# for iterator with Joachim stuff, always auto

if 0:
	grammar = parsley.makeGrammar(r"""
		test= ('ʘ':u -> "yiss" + u) | (<anything*>)
	""", {})

	print(grammar("ʘ").test())

	sys.exit()

def exception(txt):
	raise SyntaxError(txt)
	return txt


def makefor(iters, body):

	res = '{\n'
	res += 'bool break_nesting = false;\n'

	for ig in iters: # iterate through groups
		for it in ig: # iterate through iterators in group
			var = it['id']
			iter = var + '__iterator';
			if it['type'] == '=':
				range = var + '__range'
				res += 'const auto ' + range + ' = ' + it['asgn'] + ';\n'
			elif it['type'] == ':':
				range = it['asgn']
			it['range'] = range
			res += 'auto *' + iter + ' = begin(' + range + ');\n';
			
		res += 'for(; '
		for it in ig: # iterate through iterators in group
			res += it['id'] + '__iterator != end(' + it['range'] + ') && '
		res = res[:-4] # delete last " && "
		res += "; "
		for it in ig: # iterate through iterators in group
			res += it['id'] + '__iterator++, '
		res = res[:-2] # delete last ", "
		res += '){\n'
		for it in ig: # iterate through iterators in group
			res += '\t auto &' + it['id'] + ' = *' + it['id'] + '__iterator;\n'
			
	res += '#define Break break_nesting = true; break;\n\n'
	res += body
	res += '\n\n#undef Break\n'
	
	for ig in iters: # iterate through groups
		res += 'if(break_nesting){break;}\n}\n'
	
	res += '\n}\n'
	return res
	
	
def makefn(name, input, output, body):

	res = ''
	
	if isinstance(output, str): # output is a string, not a list -> no struct for return
		res = output + ' ' + name + '('
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
		res += name + '__result ' + name + '('
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

code = symbol*:s -> ''.join(s)

symbol = knownsymbol | identifier | anything
knownsymbol = (comment | string | superstring | substitution | group | stray)
stray = (groupstray | ifstray | fnstray | loopstray | switchstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

ws = (' ' | '\t' | '\r' | '\n' | comment)*

string = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\' anything> # represents one backslash
#superstring = '°°' (~'°°' anything)*:txt '°°' -> 'std::string(u8R"' + hash(txt) + '(' + ''.join(txt) + ')' + hash(txt) + '")'
superstring = '°°' (~'°°' anything)*:txt '°°' -> 'u8R"' + hash(txt) + '(' + ''.join(txt) + ')' + hash(txt) + '"'

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' symbol)*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' symbol)*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' symbol)*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = branchstmt | loopstmt | functionstmt # actual fiascode 


branchstmt = ifstmt | switchstmt

ifstmt     = 'If'     ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''
ifcondition = (~'Then' symbol)*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') symbol)*:body -> ''.join(body)
elsebody  = (~'Endif' symbol)*:body -> ''.join(body)
ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first

switchstmt = 'Switch' switchcondition:cond switchbody:body 'Endswitch' -> 'switch(' + cond + '){\n' + body + '\n}'
switchcondition = (~('Case' | 'Default' | 'Endswitch') symbol)*:cond -> ''.join(cond)
switchbody = (case | default)*:body -> ''.join(body)
case = 'Case' casecondition:cond 'Do' casebody:body caseend:end -> 'case ' + cond + ':\n\t' + body + '\n' + end
default = 'Default' casebody:body -> '\n' 'default: ' + body
casecondition = (~'Do' symbol)*:cond -> ''.join(cond)
casebody = (~('Case' | 'Fall' | 'Default' | 'Endswitch')symbol)*:body -> ''.join(body)
caseend = ('Fall' ws -> '') | (ws -> 'break;')
switchstray = ('Case' | 'Default' | 'Fall' | 'Endswitch' | 'Do')


loopstmt = forstmt | whilestmt | repeatstmt

forstmt = 'For' iteratorlist:iters 'Do' forbody:body 'Loop' -> makefor(iters, body)
iteratorlist = ws iteratoritem:first ws (',' ws iteratoritem)*:rest -> [first] + rest
iteratoritem = (iteratorgroup:iter -> iter) | (iterator:iter -> [iter])
iteratorgroup = '[' iterator:first (',' ws iterator)*:rest ']' -> [first] + rest
iterator = iterdeclaration:iter (':' | '='):type iterassignment:asgn -> {'decl':iter['decl'], 'id':iter['id'], 'type':type, 'asgn':asgn}
iterdeclaration = ('::' | ~(':' | '=') (knownsymbol | identifier:id | anything))*:decl -> {'decl':''.join(decl), 'id':id}
iterassignment = (~(',' | 'Do' | ']')symbol)*:asgn -> ''.join(asgn)
forbody = (~'Loop' symbol)*:body -> ''.join(body)

whilestmt = 'While' (~'Do' symbol)*:cond 'Do' (~'Loop' symbol)*:body 'Loop' -> 'while(' + ''.join(cond) + '){\n' + ''.join(body) + '}'
repeatstmt = 'Repeat' (~('Until' | 'Whilst')symbol)*:body (untilcond | whilstcond):cond 'Loop' -> 'do{\n' + ''.join(body) + '\n}while(' + cond + ');'
untilcond = 'Until' (~('Loop')symbol)*:cond -> '!(' + ''.join(cond) + ')'
whilstcond = 'Whilst' (~('Loop')symbol)*:cond -> ''.join(cond)
loopstray = ('Do' | 'Until' | 'Whilst' | 'Loop')


functionstmt = 'Fn' ws identifier:name ws inputpars:input ws outputpars:output ws fnbody:body 'Endfn'-> makefn(name, input, output, body)
inputpars = ('(' parameterlist:input ')' | ws:input) -> input
outputpars = ('->' ws '(' parameterlist:output ')' -> output) | ('->' ws returntype:output -> ''.join(output)) | (ws -> 'void')
parameterlist = parameter:first (',' parameter)*:rest -> [first] + rest if first!=[] else []
parameter = ws (~(')' | ',' | '=')(knownsymbol | identifier:id | anything))*:decl ('=' parassignment)?:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
returntype = ws (~(':=' | 'Endfn')symbol)*:type -> type
parassignment = (~(')' | ',')symbol)*:asgn -> ''.join(asgn)
fnbody = (':=' (~'Endfn' symbol)*:body -> ''.join(body)) | (ws -> '')
fnstray = ('->' | ':=' | 'Endfn')
#todo: virtual inline static bla

""", {'exception':exception, 'makefor':makefor, 'makefn':makefn, 'hash':hash})

def prettify(input):
	input = input.replace('\r\n', '\n')
	input = input.replace('\r', '\n')
	
	input += '   '
	output = ''
	tab = 0
	i = 0
	imax = len(input)-2
	while i <= imax:
		c1 = input[i]
		c12 = c1 + input[i+1]
		if c12 == '//':
			while i<imax and input[i] != '\n':
				output += input[i]
				i+=1
			output += input[i]
			i+=1			
			continue
		if c12 == '/*':
			while i<imax and input[i] + input[i+1] != '*/':
				output += input[i]
				i+=1
			output += input[i] + input[i+1]
			i+=2
			continue
		if c1 == '{' or c1 == '(':
			tab += 1
		if c1 == '}' or c1 == ')':
			tab -= 1
		if c1 == '\n':
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

with open('test.fsc', encoding='utf-8') as fin:
	incode = fin.read()
fin.closed

'''
print(fiascode("""Repeat something Until x<54 Loop""").code())
print(fiascode("""Repeat something Whilst x>=54 Loop""").code())
'''

print(prettify(fiascode(incode).code()))

print("Translation time in s")
print(time()-t0)
t0=time()


