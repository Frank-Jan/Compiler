@.var-18 = private unnamed_addr constant [3 x i8] c"%c\00", align 1

define void @func1(){

ret 
}

define i32 @func2(){

%i = alloca i32, align 4
store i32 8, i32* %i, align 4

%var-5 = load i32, i32* %i, align 4
%var-4 = add i32 5, %var-5
%var-3 = add i32 1, %var-4
ret i32 %var-3
}

define i8 @func3(i8 %var-6){
%c = alloca i8, align 1
store i8 %var-6, i8* %c, align 1

%i = alloca i32, align 4
store i32 0, i32* %i, align 4

%j = alloca i32, align 4
store i32 5, i32* %j, align 4

%var-14 = load i32, i32* %i, align 4
%var-15 = load i32, i32* %j, align 4
%var-12 = icmp slt i32 %var-14, %var-15
br i1 %var-12, label %label16, label %label17

label16:

ret i8 100

label17:


ret i8 99
}

define i32 @main(){

%var-20 = call i8 @func3(i8 99)
%var-21 = sext i8 %var-20 to i32
%var-19 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.var-18, i32 0, i32 0), i32 %var-21)

%var-22 = call i32 @func2()
ret i32 %var-22
}

