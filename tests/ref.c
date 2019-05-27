int test(){
    return 5;
}

int test2(int q){
    return q;
}


int main(){
    int k;
    int j = 0;
    int i = test2(3);
    i = test2(i);
    j = i;
    return test2(5);
}