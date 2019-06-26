#include <stdio.h>

int main(){
    int arr1[1];

    int Iarr[] = {2,3,4,5}; //determines length through initialiser

    char Carr[6] = {'a'};

    float Farr[5] = {0.01, 0.02};

    int i = Iarr[3];
    char c = Carr[0];
    float f = Farr[1];

    printf("i is %i\n", i);
    printf("c is %c\n", c);
    printf("f is %f\n", Farr[1]);

    return 0;
}