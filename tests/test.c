int v;

int function(){
    int i = 1;
    int u = i;
    int l = i;
    int* j = &i; // warning implicit cast
    int * p1 = &i;
    int * * p2 = &p1;
    int * * * p3 = &p2; // pointers die niet kloppen -> warnings
    int m = (*p1);
    m = 5+4*2;
    if (2*3+3==(2+1)*3){
        return 8/2;
    } else{
        return function();
    }
    }

void eenWHile_LUS12343(char , int j);

int main(){
    char c = 'r';
    c = c+c;
    eenWHile_LUS12343(c, 4);
    return 900;
}

void eenWHile_LUS12343(char c, int j){
    while(c == 'C'){
        j = j+1;
        if(j == 23){
            c = 'B';
        }
    }
    return;
}