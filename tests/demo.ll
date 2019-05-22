define i32 @function(i32 %var-1){
%j = alloca i32, align 4
store i32 %var-1, i32* %j, align 4

%var-3 = load i32, i32* %j, align 4
ret i32 %var-3
}

define i32 @main(){

%a = alloca i32, align 4
store i32 0, i32* %a, align 4

%b = alloca i32, align 4
store i32 0, i32* %b, align 4

store %var-8 = call i32 @function(i32 10)
, i32* %a, align 4

store i32 8, i32* %b, align 4

%var-13 = load i32, i32* %a, align 4
%var-14 = load i32, i32* %b, align 4
%var-11 = add i32 %var-13, %var-14
store i32 %var-11, i32* %a, align 4

%c = alloca i32, align 4
%var-23 = load i32, i32* %b, align 4
%var-24 = load i32, i32* %a, align 4
%var-21 = sub i32 %var-23, %var-24
store i32 %var-21, i32* %c, align 4

%var-28 = load i32, i32* %a, align 4
%var-29 = load i32, i32* %b, align 4
%var-26 = icmp slt i32 %var-28, %var-29
br i1 %var-26, label %Label30, label %Label31
Label30:

store i32 7, i32* %c, align 4

br label %Label31
Label31:

store i32 4, i32* %c, align 4


%var-34 = load i32, i32* %c, align 4
ret i32 %var-34
}

