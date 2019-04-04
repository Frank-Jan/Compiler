//variable declarations
//base types
void v;
int i;
char c;
float f;

//pointer types
void *v;
void* v;
void * v;

int* pi;
char* pc;
float* pf;

//function declarations
//return types
void function();
int function();
char function();
float function();
void* function();
int* function();
char* function();
float* function();

//arguments
void function(char);
void function(char*);
void function(char&);
int function(void*&,int,int&,int*,float f,float& rf,float* pf, char,char&,char*,int*& rpi);
void function(char c);

//viable names:
void camelCase;
void snake_case;
void Capital;
void _under_score;
void numbers0123456789;
void function();
void camelCase();
void snake_case();
void Capital();


