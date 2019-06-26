#include <stdio.h>

int main(){
    int i = 1;
    char c = 'a';
    float f = 1.234;
    printf("The value of i: %d\n", i);
    printf("The value of c and f: %d, %f\n", c, f);
    printf("Give a value for i (integer): ");
    scanf("%i", &i);
    printf("The value of int i is now: %i\n", i);
    return 0;
}