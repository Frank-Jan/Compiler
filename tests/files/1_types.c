int main(){
    // Declarations
    int i;
    char c;
    float f;

    int* pi;
    char* pc;
    float* pf;

    //pointers to pointers to...
    int** ppi;
    char** ppc;
    float** ppf;


    // Definitions
    int j = 123;
    char d = 'S';
    float g = 4.567;

    int* pj = &j;
    char* pd = &d;
    float* pg = &g;

    int** ppj = &pj;
    char** ppd = &pd;
    float** ppg = &pg;

    return 0;
}