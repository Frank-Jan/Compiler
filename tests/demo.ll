@.var-45 = private unnamed_addr constant [31 x i8] c"The_solution_to_everything:_%d\00", align 1

@.var-24 = private unnamed_addr constant [37 x i8] c"A_character_returned_by_func3():_%c\0A\00", align 1

declare i32 @printf(i8*, ...)
declare i32 @scanf(i8*, ...)



define void @func1(){

ret void
}

define i32 @func2(){

%i = alloca i32, align 4
store i32 8, i32* %i, align 4

%var-8 = load i32, i32* %i, align 4
%var-6 = sdiv i32 %var-8, 1
%var-5 = mul i32 2, %var-6
%var-4 = add i32 1, %var-5
%var-3 = sub i32 1, %var-4
ret i32 %var-3
}

define i8 @func3(i8 %var-9){
%c = alloca i8, align 1
store i8 %var-9, i8* %c, align 1

%i = alloca i32, align 4
store i32 0, i32* %i, align 4

%j = alloca i32, align 4
store i32 5, i32* %j, align 4

%var-17 = load i32, i32* %i, align 4
%var-18 = load i32, i32* %j, align 4
%var-15 = icmp slt i32 %var-17, %var-18
br i1 %var-15, label %Label19, label %Label20
Label19:

ret i8 100
br label %Label20
Label20:

ret i8 99
}

define i32* @func4(i32 %var-21){
%i = alloca i32, align 4
store i32 %var-21, i32* %i, align 4

ret i32* %i
}

define i32 @main(){

%var-26 = call i8 @func3(i8 99)
%var-27 = sext i8 %var-26 to i32
%var-25 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([37 x i8], [37 x i8]* @.var-24, i32 0, i32 0), i32 %var-27)

%j = alloca i32*, align 8
%var-30 = call i32* @func4(i32 2)
store i32* %var-30, i32** %j, align 8

%i = alloca i32, align 4
store i32 4, i32* %i, align 4

store i32 0, i32* %i, align 4

br label %Label37
Label37:
%var-40 = load i32, i32* %i, align 4
%var-38 = icmp slt i32 %var-40, 46
br i1 %var-38, label %Label35, label %Label36

Label35:

%var-43 = load i32, i32* %i, align 4
%var-41 = add i32 %var-43, 1
store i32 %var-41, i32* %i, align 4


br label %Label37
Label36:

%var-47 = load i32, i32* %i, align 4
%var-46 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.var-45, i32 0, i32 0), i32 %var-47)

%var-48 = call i32 @func2()
ret i32 %var-48
}

