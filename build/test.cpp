// test.cpp
//

#include "test.h"
#define LZZ_INLINE inline
using namespace std;
int main (int argc, char * (argv) [])
                                {
	int a=0, b=0;
	if( a==0 ){
		cout << "a is 0";
	}
	if( a==0 ){
		cout << "a is 0";
	}else{
		cout << "a is not 0";
	}
	if( a==0 ){
		cout << "a is 0";
	}else if( a==1 ){
		cout << "a is 1";
	}else if( a==2 ){
		cout << "a is 2";		
	}else{
		cout << "a is not 0 or 1 or 2";
	}		
	/* °°this is a°° /* °°nested°° /* °°very nested°° * /* /
	°°multiline comment°° */
	switch( a
	){
	}
	switch( a
	){
		default: 
		cout << a;
	}
	switch( a
	){
		case  0 :
		cout << a;
		break;
	}
	switch( a
	){
		case  1: case 2: case 3 :
		cout << a;
		break;
	}
	switch( a
	){
		case  0 :
		cout << a;
	}		
	switch( a
	){
		case  0 :
		cout << a;
		case  1: case 2: case 3 :
		cout << a;
		break;
		default: 
		cout << a;
	}
	while( b<10 ){
		b++;
	}
	do{
		b++;
	}while( b<20 );
	do{
		b++;
	}while(!( b==30 )); 
	{
		auto i__range = all({1,2,3} );
		for(; !i__range.empty(); i__range.popFront()){
			auto i = i__range.front();
			#define Break goto loopend__1;
			cout << i; 
			#undef Break
		}
	}
	loopend__1:
	{
		auto x__range = all({1,2,3});
		for(; !x__range.empty(); x__range.popFront()){
			auto x = x__range.front();
			auto y__range = all({4,5,6} );
			for(; !y__range.empty(); y__range.popFront()){
				auto y = y__range.front();
				#define Break goto loopend__2;
				cout << x << y;
				#undef Break
			}
		}
	}
	loopend__2:
	vector<int> vi({15,16,17,18});
	vector<int> vj({25,26,27,28,29});
	{
		auto i__range = all(vi );
		for(; !i__range.empty(); i__range.popFront()){
			auto i = i__range.front();
			#define Break goto loopend__3;
			cout << i;
			#undef Break
		}
	}
	loopend__3:
	{
		auto i__range = all(vi);
		auto j__range = all(vj);
		for(; !i__range.empty() && !j__range.empty(); i__range.popFront(), j__range.popFront()){
			auto i = i__range.front();
			auto j = j__range.front();
			#define Break goto loopend__4;
			j=i;
			#undef Break
		}
	}
	loopend__4:
	{
		auto x__range = all({1,2,3});
		for(; !x__range.empty(); x__range.popFront()){
			auto x = x__range.front();
			auto y__range = all({4,5,6});
			for(; !y__range.empty(); y__range.popFront()){
				auto y = y__range.front();
				auto i__range = all(vi);
				auto j__range = all(vj);
				for(; !i__range.empty() && !j__range.empty(); i__range.popFront(), j__range.popFront()){
					auto i = i__range.front();
					auto j = j__range.front();
					#define Break goto loopend__5;
					j=i;
					#undef Break
				}
			}
		}
	}
	loopend__5:
	{
		auto i__range = make_range(1, 5);
		auto j = 1;
		for(; !i__range.empty() && true /*j loops forever*/; i__range.popFront(), j++){
			auto i = i__range.front();
			#define Break goto loopend__6;
			#undef Break
		}
	}
	loopend__6:
	cout << u8R"098f6bcd46(test)098f6bcd46" << u8R"d41d8cd98f()d41d8cd98f" << "\"test\"" << "" "" << R"(test)" << R"/token(  test  )/token" << std::endl;
	system("pause");
	return 0;
}
void f1 ()
         {}
void f2 ()
         {}
int f3 ()
         {}
f4__result f4 ()
               {
	int r;
	return {r};
}
void f5 ()
         {
	return 0; 
}
f7__result f7 (int a, int b)
 {
	int a_new=a;
	int b_new=b /* second output parameter, default equal to input*/
	;
	#define Return return {a_new, b_new};
	a_new *= 17;
	b_new *= 19;
	Return
	a_new = 0;
	b_new = 0;
	Return
	#undef Return
}
#undef LZZ_INLINE
