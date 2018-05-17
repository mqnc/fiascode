// test.cpp
//

#include "test.h"
#define LZZ_INLINE inline
using namespace std;
int main (int argc, char * (argv) [])
                                {
	cout << "counting a from 0 towards (and excluding) 5\n";
	{
		auto a__range = make_range(0, 5 );
		for(; !a__range.empty(); a__range.popFront()){
			const auto a = begin(a__range);
			#define Break goto loopend__1;
			cout << "set a to " << a << endl;
			if( a==0 ){
				cout << "a is 0\n";
			}
			if( a==0 ){
				cout << "a is 0\n";
			}else{
				cout << "a is not 0\n";
			}
			if( a==0 ){
				cout << "a is 0\n";
			}else if( a==1 ){
				cout << "a is 1\n";
			}else if( a==2 ){
				cout << "a is 2\n";		
			}else{
				cout << "a is not 0 or 1 or 2\n";
			}		
			/* °°this is a°° /* °°nested°° /* °°very nested°° * /* /
		°°multiline comment°° (I put the °° there to see if cpype wants to turn stuff into strings) */
			switch( a
			){
			}
			switch( a
			){
				default: 
				cout << "a is anything\n";
			}
			switch( a
			){
				case  0 :
				cout << "a is 0\n";
				break;
			}
			switch( a
			){
				case  1: case 2: case 3 :
				cout << "a is 1, 2 or 3\n";
				break;
			}
			switch( a
			){
				case  0 :
				cout << "a is 0\n";
			}		
			switch( a
			){
				case  0 :
				cout << a;
				case  1: case 2: case 3 :
				cout << "a is 1, 2 or 3 or maybe also 0\n";
				break;
				default: 
				cout << "a ain't 0, 1, 2 or 3\n";;
			}
			#undef Break
		}
	}
	loopend__1:
	int a=0;
	while( a<10 ){
		a++;
	}
	cout << "a should be 10 and is " << a << endl;
	do{
		a++;
	}while( a<20 );
	cout << "a should be 20 and is " << a << endl;
	do{
		a++;
	}while(!( a==30 ));
	cout << "a should be 30 and is " << a << endl;
	int i = 0;
	cout << "outer scope i is " << i << endl;
	cout << "first 5 primes using inner scope i: ";
	{
		auto i__range = all({2,3,5,7,11} );
		for(; !i__range.empty(); i__range.popFront()){
			auto &i = *begin(i__range);
			#define Break goto loopend__2;
			cout << i << " "; 
			#undef Break
		}
	}
	loopend__2:
	cout << "\nouter scope i is " << i << endl;
	cout << "all combinations of (1, 2, 3) and (4, 5, 6): ";
	{
		auto x__range = all({1,2,3});
		for(; !x__range.empty(); x__range.popFront()){
			auto &x = *begin(x__range);
			auto y__range = all({4,5,6} );
			for(; !y__range.empty(); y__range.popFront()){
				auto &y = *begin(y__range);
				#define Break goto loopend__3;
				cout << x << y << " ";
				#undef Break
			}
		}
	}
	loopend__3:
	cout << endl;
	vector<int> vi({1, 2, 3, 4});
	vector<int> vj({10, 20, 30, 40, 50, 60});
	cout << "elements in vi: ";
	{
		auto i__range = all(vi );
		for(; !i__range.empty(); i__range.popFront()){
			auto &i = *begin(i__range);
			#define Break goto loopend__4;
			cout << i << " ";
			#undef Break
		}
	}
	loopend__4:
	cout << endl;
	cout << "copying all elements of vi onto some of vj\n";
	{
		auto i__range = all(vi);
		auto j__range = all(vj);
		for(; !i__range.empty() && !j__range.empty(); i__range.popFront(), j__range.popFront()){
			auto &i = *begin(i__range);
			auto &j = *begin(j__range);
			#define Break goto loopend__5;
			j=i;
			#undef Break
		}
	}
	loopend__5:
	cout << "elements in vj: ";
	{
		auto j__range = all(vj );
		for(; !j__range.empty(); j__range.popFront()){
			auto &j = *begin(j__range);
			#define Break goto loopend__6;
			cout << j << " ";
			#undef Break
		}
	}
	loopend__6:
	cout << endl;
	{
		auto ei__range = all(vi);
		auto i = 0;
		for(; !ei__range.empty() && true /*i loops forever*/; ei__range.popFront(), i++){
			auto &ei = *begin(ei__range);
			auto ej__range = all(vj);
			auto j = 0;
			for(; !ej__range.empty() && true /*j loops forever*/; ej__range.popFront(), j++){
				auto &ej = *begin(ej__range);
				#define Break goto loopend__7;
				cout << i << "th element of vi / " << j << "th element of vj = " << ei << "/" << ej << endl;
				if( i==3 ){
					cout << "breaking nested loop\n";
					Break
				}
				#undef Break
			}
		}
	}
	loopend__7:
	cout << "Raw UTF8 String: " << u8R"c446a2994f(Привет, мир!)c446a2994f" << endl;
	cout << "Mean escape tests: " << u8R"098f6bcd46(test)098f6bcd46" << u8R"e9cbb018b2("\n° )e9cbb018b2" << "\"test\"" << "" "" << R"(test)" << R"//token(  test  )//token" << std::endl;
	voidFunctionWithoutNoParameters();
	voidFunctionWithNoParameters();
	cout << "7=" << inlineConstSeven() << endl;
	auto nismr = noInputSingleMultipleReturn();
	cout << "random value somewhere in memory: " << nismr.r << endl;
	auto nismdr = noInputSingleMultipleDefaultReturn();
	cout << "77: " << nismdr.r << endl;
	cout << "2 * 123 = " << twice(123) << endl;
	auto result = divWithRest(20, 3);
	cout << "20 = " << result.q << "*3 + " << result.r << endl;
	auto ab = fullMontyAndNicelyCommented(2);
	cout << "14=" << ab.a_new << ", 18=" << ab.b_new << endl;
	system("pause");
	return 0;
}
void voidFunctionWithoutNoParameters ()
                                      {}
void voidFunctionWithNoParameters ()
                                   {}
noInputSingleMultipleReturn__result noInputSingleMultipleReturn ()
                                                                 {
	int r;
	return {r};
}
noInputSingleMultipleDefaultReturn__result noInputSingleMultipleDefaultReturn ()
                                                                               {
	int r=77;
	return {r};
}
int twice (int x)
                   {
	return 2*x; 
}
divWithRest__result divWithRest (int x, int y)
                                                 {
	int q=x/y;
	int r=x%y;
	return {q, r};
}
fullMontyAndNicelyCommented__result fullMontyAndNicelyCommented (int a, int b)
 {
	int a_new=a;
	int b_new=b /* second output parameter, default equal to input*/
	;
	#define Return return {a_new, b_new};
	a_new *= 7;
	b_new *= 9;
	Return
	/* this should not happen:*/
	a_new = 0;
	b_new = 0;
	Return
	#undef Return
}
#undef LZZ_INLINE
