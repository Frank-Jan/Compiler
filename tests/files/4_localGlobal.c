// Global type declarations
int i; // defaults to 0
char c; // defaults to 0
float f; // defaults to 0.0

int* pi; // defaults to null
char* pc;
float* pf;



// Global type definitions
int j = 123;
char d = 'S';
float g = 4.567;

int* pj = &j;
char* pd = &d;
float* pg = &g;

int** ppj = &pj;
char** ppd = &pd;
float** ppg = &pg;


// Local
int main(){
    // Type declarations
    int i; // defaults to 0
    char c; // defaults to 0
    float f; // defaults to 0.0

    int* pi;
    char* pc;
    float* pf;

    int** ppi;
    char** ppc;
    float** ppf;


    // Type definitions
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