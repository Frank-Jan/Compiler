//#include <stdio.h>
//
//void func1(){
//    return;
//}
//
//int func2(){
//    int i = 8;
//    return 1+5+i;
//}
//
//char func3(char c){
//    int i = 0;
//    int j = 5;
//    if(i < j){
//        return 'd';
//    }
//    return 'c';
//}
//
//int* func4(int i){
//    return &i;
//}
//
//int main(){
//    printf("%c", func3('c'));
//    return func2();
//}

#include <stdio.h> //Import

void func1(){ //Type void
    return;
}

int func2(){ //Type int
    int i = 8;
    return 1-1+2*i/1; //Operations (with respect to the order)
}

char func3(char c){ //Type char
    int i = 0;
    int j = 5;
    if(i < j){
        return 'd';
    }
    return 'c';
}

int* func4(int i){ //Type Pointer
    return &i; //Reference
}

int main(){
    printf("A character returned by func3():\n %c", func3('c')); //Printf
    return func2();
}