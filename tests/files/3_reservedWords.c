#include <stdio.h>

// void return will generate a warning
void main(){

    int i = 2;

    if(i < 3){
        printf("i is groter dan 3\n");
    }


    float f = 0.0123;

    if(f > 3.0123){
        printf("f (%f) is groter dan 3.0123\n", f);
    } else {
        printf("f (%f) is kleiner dan 3.0123\n", f);
    }


    char c = 'c';

    while(c == 'c'){
        c = 'a';
        printf("c changed\n");
    }

    printf("while is done\n");

    return;
}