declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)

@.var-14 = private unnamed_addr constant [31 x i8] c"The value of int i is now: %i\0A\00", align 1

@.var-12 = private unnamed_addr constant [3 x i8] c"%i\00", align 1

@.var-10 = private unnamed_addr constant [31 x i8] c"Give a value for i (integer): \00", align 1

@.var-4 = private unnamed_addr constant [30 x i8] c"The value of c and f: %d, %f\0A\00", align 1

@.var-1 = private unnamed_addr constant [20 x i8] c"The value of i: %d\0A\00", align 1


define i32 @main() {
%i = alloca i32, align 4
store i32 1, i32* %i, align 4
%c = alloca i8, align 1
store i8 97, i8* %c, align 1
%f = alloca float, align 4
store float 0x3ff3be76c0000000, float* %f, align 4
%var-2 = load i32, i32* %i, align 4
%var-3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.var-1, i32 0, i32 0), i32 %var-2)
%var-5 = load i8, i8* %c, align 1
%var-6 = sext i8 %var-5 to i32
%var-7 = load float, float* %f, align 4
%var-8 = fpext float %var-7 to double
%var-9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.var-4, i32 0, i32 0), i32 %var-6, double %var-8)
%var-11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.var-10, i32 0, i32 0))
%var-13 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.var-12, i32 0, i32 0), i32* %i)
%var-15 = load i32, i32* %i, align 4
%var-16 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.var-14, i32 0, i32 0), i32 %var-15)
ret i32 0
}

