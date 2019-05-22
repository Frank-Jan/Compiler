int function(int j){
    return j;
}

int main(){
    int a;
    int b;
    a = function(10);
    b = 8;
    a = a+b;
    int c = b-a;
    if(a < b){
        c = 7;
    }
    else{
        c = 4;
    }
    return c;
}
