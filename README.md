# C-Pype 0.0.1

A preprepreprocessor for C++ 14 written in Python. Its purpose is to reduce the pain of C++ programming as much as possible.

Your program is written as a bunch of .cpy files. They are translated into lzz files which are then split into c++ headers and sources.

## Examples

So far, C-Pype supports the following constructs:  
(powerful for loops and functions with multiple return parameters are the main selling points, scroll down a bit if you are in a hurry)

### If statements without parantheses and braces
```
If a==0 Then
	cout << "a is 0\n";
Elseif a==1 Then
	cout << "a is 1\n";
Else
	cout << "a is not 0 or 1 or 2\n";
Endif
```

### Switch branches without traps
```
Switch a
	Case 0 Do
		cout << a;
		Fall // break is default and Fall prevents that
	Case 1, 2, 3 Do
		cout << "a is 1, 2 or 3 or maybe also 0\n";
	Default
		cout << "a ain't 0, 1, 2 or 3\n";
Endswitch
```

### While and Repeat loops
```
While a<10 Do 
	a++;
Loop

Repeat
	a++;
Whilst a<20 Loop // the "While" keyword is already occupied

Repeat
	a++;
Until a==30 Loop
```

### Readable nested and parallel For loops
```
For a:0=>5 Do // for a from 0 towards 5 (5 is not included, like in Python)
	cout << a;
Loop

For a:{2, 3, 5, 7, 11} Do Loop // supports std::initializer_list

vector<int> va({1, 2, 3, 4});
For a:va Do Loop // vectors and generally things that support begin() and end() work

For x:0=>width, y:0=>height Do // For loops can be nested like in Julia
	If x==10 && y==10 Then Break Endif // and escaped through all levels
Loop

For [a:va, b:vb] Do // And you can iterate through arrays parallely, stopping when the shortest array ends
	a=b;
Loop

For [a:va, b:vb], [c:{1,2,3,4,5}, d:0...] Do // And you can nest and parallelize at the same time
	// d:0... starts at 0 and does not have an end condition
Loop
```

### Functions with multiple return values that are actually usable
```
// definition:
Fn twice(int a_in, int b_in, int c_in) -> (int a_out, int b_out, int c_out):=
	a_out = 2*a_in;
	b_out = 2*b_in;
	c_out = 2*c_in;
Endfn

Fn div(int x=0, int y=1) -> (int q=x/y, int r=x%y) Endfn // default input and return parameters

// call:
auto abc = twice(20, 30, 40);
cout << abc.aout << abc.bout << abc.cout << endl;

auto result = div(20, 7);
cout << "20/7 is " << result.q << " with remainder " << result.r << endl;
```

### The little things
```
cout <<
```

See test.cpy for more details and look at the generated test.lzz (or test.cpp and test.h) files to see what happens to your code.

## Dependencies

C-Pype is based on
* Parsley 1.3, a parser generator for Python (https://github.com/pyga/parsley)
* Lazy C++ 2.8.2, a compiler that splits lzz files into C++ source and header files (http://www.lazycplusplus.com/)
* SCons 3.0.0, a build system written in Python (https://scons.org/)

All dependencies are included and everything should work out of the box hopefully maybe. (Lzz is compiled for 32 bit and you might go through a little trouble to make it work on 64bit Linux)

## Background

See https://www.codeproject.com/Messages/5496927/What-is-the-fastest-and-bestest-programming-langua.aspx

## Caveats

Be aware that there is currently no editor that supports code completion, folding or syntax highlighting for this. And you have to debug in three layers of code. If you can live with that, have fun! Once the incredible value of this project has been recognized by a large community, all those things will probably be dealt with by the cloud crowd in no time, right? :-)

## Acknowledgement

Props and kudos to jkuebart for a ton of discussion, support and contribution!

## License

C-Pype is released under GPLv3 (because Lazy C++ is).

And yes, you can sell closed-source programs that you created with it.