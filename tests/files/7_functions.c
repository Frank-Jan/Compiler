#include <stdio.h>

int test1(){
    return 5;
}

char test2(int i, char c){
    c = 'c';
    return c;
}

float test3(){
    float f = 0.0213;
    return f;
}


int main(){

    int i = test1();
    char c = 'a';
    c = test2(i, c);
    float f = test3();

    printf("i is %i\n", i);
    printf("c is %c\n", c);
    printf("f is %f\n", f);

    return 0;
}