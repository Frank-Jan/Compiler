void func1(){
    return;
}

int func2(){
    int i = 8;
    return 1+5+i;
}

char func3(char c){
    int i = 0;
    int j = 5;
    if(i < j){
        return 'd';
    }
    return 'c';
}

int main(){
    printf("%c", func3('c'));
    return func2();
}