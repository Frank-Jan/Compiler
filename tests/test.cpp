int i;
float j = 0.01;
int main(){
    int j = 5;
    j = 5;
    {
        int j = 8;
        printf(j); // Moet 8 zijn
    }
    printf(j,j); // Moet 5 zijn

}