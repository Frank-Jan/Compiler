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
    printf("A_character_returned_by_func3():\t%c\n\n", func3('c')); //Printf
    int i = *func4(2); //Dereference


    if(i > 3){ //IfElse
        printf("i_is_lower_then_3");
    } else {
        printf("i_is_not_lower_then_3");
    }

    i = 0;
    while (i < 46){ //While
        i = i+1;
    }

    printf("The_solution_to_everything:\t%d\n\n", i);
    return func2();
}