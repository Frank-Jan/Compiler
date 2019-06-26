
@.str = private unnamed_addr constant [3 x i8] c"%i\00", align 1

declare i32 @printf(i8*, ...)




define i32 @main(){

%i = alloca i32, align 4
store i32 200, i32* %i, align 4

%c = alloca i8, align 1
store i8 99, i8* %c, align 1

%var-6 = load i32, i32* %i, align 4
%var-7 = load i32, i32* %i, align 4
;%var-5 = call i32 @printf(i32 %var-6, i32 %var-7)
%var-10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %var-7)

%var-8 = load i32, i32* %i, align 4
ret i32 %var-8
}


