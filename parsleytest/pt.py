import sys
import os
cd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cd + "/parsley")
import parsley # rename parsley/parsley.py to parsley/__init__.py

if False:
	grammar = parsley.makeGrammar("""
		test= ("a" -> 1) | ("b" -> 2)
	""", {})

	print(grammar("a").test())


def exception(txt):
	raise SyntaxError(txt)
	return txt
	
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
		res = 'struct ' + name + '_result{'
		for par in output:
			res += par['decl'] + '; '
		res += '};\n'
		res += name + '_result ' + name + '('
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
	
fiascode = parsley.makeGrammar("""

code = (known | anything)*:c -> ''.join(c)


known = (comment | string | substitution | group | stray)
stray = (groupstray | ifstray | fnstray | loopstray):estray -> exception('Stray ' + estray + ' detected')

comment = (comment1 | comment2)
comment1 = <'/*' (~'*/' anything)* '*/'>
comment2 = <'//' (~'\n' anything)* '\n'>

ws = (' ' | '\\t' | '\\r' | '\\n' | comment)*

string = <'"' (escaped | ~'"' anything)* '"'>
escaped = <'\\\\' anything> # we need a double backslash escape here for representing one backslash

group = (parenthesed | bracketed | braced)
parenthesed = '(' (~')' (known | anything))*:body ')' -> '(' + ''.join(body) + ')'
bracketed   = '[' (~']' (known | anything))*:body ']' -> '[' + ''.join(body) + ']'
braced      = '{' (~'}' (known | anything))*:body '}' -> '{' + ''.join(body) + '}'
groupstray = (')' | ']' | '}')

identifier = <(letter | '_') (letter | '_' | digit)*>


substitution = ifstmt | switchstmt | loopstmt | function # actual fiascode 


ifstmt     = 'If'     ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail ->      'if(' + cond + '){' + ''.join(body) + '}' + tail
elseifstmt = 'Elseif' ifcondition:cond 'Then'   ifbody:body (elseifstmt | elsestmt | endifstmt):tail -> 'else if(' + cond + '){' + ''.join(body) + '}' + tail
elsestmt   = 'Else'                         elsebody:body                          endifstmt :tail -> 'else{'                  + ''.join(body) + '}' + tail
endifstmt  = 'Endif' -> ''
ifcondition = (~'Then' (known | anything))*:cond -> ''.join(cond)
ifbody    = (~('Elseif' | 'Else' | 'Endif') (known | anything))*:body -> ''.join(body)
elsebody  = (~'Endif' (known | anything))*:body -> ''.join(body)
ifstray = ('Elseif' | 'Else' | 'Endif' | 'Then') # those should not be encountered first


switchstmt = 'Switch' switchcondition:cond switchbody:body 'Endswitch' -> 'switch(' + cond + '){\\n' + body + '\\n}'
switchcondition = (~'Case' (known | anything))*:cond -> ''.join(cond)
switchbody = (case | default)+:body -> ''.join(body)
case = 'Case' casecondition:cond 'Do' casebody:body caseend:end -> 'case ' + cond + ':\\n\\t' + body + '\\n' + end
default = 'Default' casebody:body
casecondition = (~'Do' (known | anything))*:cond -> ''.join(cond)
casebody = (~('Case' | 'Fall' | 'Default' | 'Endswitch')(known | anything))*:body -> ''.join(body)
caseend = ('Fall' -> '') | (ws -> 'break;')


function = 'Fn' ws identifier:name ws inputpars:input ws outputpars:output ws fnbody:body 'Endfn'-> makefn(name, input, output, body)
inputpars = ('(' parameterlist:input ')' | ws:input) -> input
outputpars = ('->' ws '(' parameterlist:output ')' -> output) | ('->' ws returntype:output -> ''.join(output)) | (ws -> 'void')
parameterlist = parameter:first (',' parameter)*:rest -> [first] + rest if first!=[] else []
parameter = ws (~(')' | ',' | '=')(known | identifier:id | anything))*:decl ('=' assignment)?:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
returntype = ws (~(':=' | 'Endfn')(known | anything))*:type -> type
assignment = (~(')' | ',')(known | anything))*:asgn -> ''.join(asgn)
fnbody = (':=' (~'Endfn' (known | anything))*:body -> ''.join(body)) | (ws -> '')
fnstray = 'Endfn'



loopstmt = forstmt | whilestmt | repeatstmt

forstmt = 'For' 
iterator = (~'='(known | identifier:id | anything))*:decl ws '=' forassignment:asgn -> {'decl':''.join(decl), 'id':id, 'asgn':asgn} if decl != [] else []
forassignment = (~(',' | 'Do')(known | anything))*:asgn -> ''.join(asgn)

whilestmt = 'While' (~'Do' (known | anything))*:cond 'Do' (~'Loop' (known | anything))*:body 'Loop' -> 'while(' + ''.join(cond) + '){\\n' + ''.join(body) + '}'
repeatstmt = 'Repeat' (~('Until' | 'Whilst')(known | anything))*:body (untilcond | whilstcond):cond 'Loop' -> 'do{\\n' + ''.join(body) + '\\n}while(' + cond + ');'
untilcond = 'Until' (~('Loop')(known | anything))*:cond -> '!(' + ''.join(cond) + ')'
whilstcond = 'Whilst' (~('Loop')(known | anything))*:cond -> ''.join(cond)
loopstray = ('Do' | 'Until' | 'Whilst' | 'Loop')



""", {'exception':exception, 'makefn':makefn})



    #for(int x=0, y=0, w=3, h=3; y<h; x++, y+=x>=w?1:0, x=x>=w?0:x){
   #     std::cout << x << y << "\n";
  #  }
'''
print(fiascode("""Fn f1(&a, int b,   c=3)->(uint d,e=4,f):= bibabu Endfn""").function())
print(fiascode("""Fn f2(int x)->(int y):= Endfn""").function())
print(fiascode("""Fn f3()->():= Endfn""").function())
print(fiascode("""Fn f4():= Endfn""").function())
print(fiascode("""Fn f5 ->():= Endfn""").function())
print(fiascode("""Fn f6:= Endfn""").function())
print(fiascode("""Fn f7 -> int := Endfn""").function())
print(fiascode("""Fn div(int x, int y)->(int q=0, int r=0):= q=x/y; r=x%y; Endfn""").function())
print(fiascode("""Fn f9(int x, int y)->(int q=x/y, int r=x%y) Endfn""").function())
'''

print(fiascode("""
Switch a
	Case 3 Do x=3; Fall
	Case 4 Do x=4;
	Default x=5
Endswitch
""").code())


