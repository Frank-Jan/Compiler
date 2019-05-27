int test(){
    return 5;
}

int test2(int q){
    return q;
}


int main(){
    int i = test2(3);
    i = test2(i);
    return test();
}