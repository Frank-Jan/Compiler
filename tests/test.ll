

define i32 @main(){

%i = alloca i32, align 4
store i32 2, i32* %i, align 4

%var-4 = load i32, i32* %i, align 4
%var-3 = icmp slt i32 1, %var-4
br label %label7
label7:
br i1 %var-3, label %label5, label %label6

label5:

%var-10 = load i32, i32* %i, align 4
%var-8 = sub i32 %var-10, 1
store i32 %var-8, i32* %i

br label %label7
label6:

%var-13 = load i32, i32* %i, align 4
ret i32 %var-13
}

