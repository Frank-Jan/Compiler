//int i;
int function();

int function(){
    return 8;
}

int main(){
    int i = 1;
    int u = i;
    int l = i;
    int j = &i; // warning implicit cast
    int * p1 = &i;
    int * * p2 = &p1;
    int * * * p3 = &p2;
    int m = (*p1);
    m = 5*(4+2);
    if (2==2){
        return 8/2;
    } else{
        return function();
    }
}