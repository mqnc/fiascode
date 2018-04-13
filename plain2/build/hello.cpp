// hello.cpp
//

#include "hello.h"
#include "helper.h"
#define LZZ_INLINE inline
int main (int argc, char * (argv) [])
{
	printf("Hello, World! %d \n", add1(5));
	printf("Press the any key!\n");
	getchar();
	return 0;
}
#undef LZZ_INLINE
