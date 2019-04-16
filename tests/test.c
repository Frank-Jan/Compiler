//#include <stdio.h>

int i = 3*8-3*8/1+0;
float j = 0.01;

int* heyhey(int* a, float* b, int c);

int* heyhey(int* i1, float* fl, int hey){ //hey= 0 lukt niet, int*  <- geen naam mag niet
    int dit;
    float is;
    char geen;
//    void goede();// void return type, declaratie wel definieren niet
    int* code = &dit;
    return code;
}

int main(){
    int j = 5;
    j = 5+6*8;
    {
        int j = 8;
        printf(j); // Moet 8 zijn
    }
    printf(j,j); // Moet 55 zijn
    j = j * (j + j) * (j + j) *3; //haakjes

}