define i32 @main(){

%a = alloca i32, align 4
store i32 8, i32* %a, align 4

%b = alloca i32, align 4
store i32 9, i32* %b, align 4

%var-7 = load i32, i32* %a, align 4
%var-8 = load i32, i32* %b, align 4
%var-5 = add i32 %var-7, %var-8
store i32 %var-5, i32* %a, align 4

ret i32 0
}

