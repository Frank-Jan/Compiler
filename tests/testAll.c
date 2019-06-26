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
        i = 0; //gets ignored
    }
    return 'c';
}

int* func4(int i){ //Type Pointer
    return &i; //Reference
}

int main(){
    printf("A character returned by func3():\n %c", func3('c')); //Printf
    int i = *func4(2); //Dereference


    if(i < 3){
        printf("i is lower then 3");
    } else {
        printf("i is not lower then 3");
    }

    i = 0;
    while (i < 46){
        i = i+1;
    }

    printf("The solution to everything:\t %d", i1);
    return func2();
}
