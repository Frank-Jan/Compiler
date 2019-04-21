//#include <stdio.h>

//int f(int*);

int f(int i){
    return i;
}

int main(){
    int o = (f(1) + f(2)) * f(3);
    int i = f(1);
    int k = i;
    int j = 0;
    return o;
}

