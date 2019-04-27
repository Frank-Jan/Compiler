char* func(char* q){
    return q;
}

int main(){
    char a = 'a';
    char* c;
    c = func(&a);

    return 0;
}
