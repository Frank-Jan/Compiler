declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)


define i32 @test1() {
ret i32 5
}


define i8 @test2(i32 %var-1, i8 %var-2) {
%i = alloca i32, align 4
store i32 %var-1, i32* %i, align 4
%c = alloca i8, align 1
store i8 %var-2, i8* %c, align 1
store i8 99, i8* %c, align 1
%var-3 = load i8, i8* %c, align 1
ret i8 %var-3
}


define float @test3() {
%f = alloca float, align 4
store float 0x3f95cfaac0000000, float* %f, align 4
%var-4 = load float, float* %f, align 4
ret float %var-4
}

@.var-22 = private unnamed_addr constant [9 x i8] c"f is %f\0A\00", align 1

@.var-18 = private unnamed_addr constant [9 x i8] c"c is %c\0A\00", align 1

@.var-15 = private unnamed_addr constant [9 x i8] c"i is %i\0A\00", align 1


define i32 @main() {
%i = alloca i32, align 4
%var-6 = call i32 @test1()
store i32 %var-6, i32* %i, align 4
%c = alloca i8, align 1
store i8 97, i8* %c, align 1
%var-11 = load i32, i32* %i, align 4
%var-12 = load i8, i8* %c, align 1
%var-10 = call i8 @test2(i32 %var-11, i8 %var-12)
store i8 %var-10, i8* %c, align 1
%f = alloca float, align 4
%var-14 = call float @test3()
store float %var-14, float* %f, align 4
%var-16 = load i32, i32* %i, align 4
%var-17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-15, i32 0, i32 0), i32 %var-16)
%var-19 = load i8, i8* %c, align 1
%var-20 = sext i8 %var-19 to i32
%var-21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-18, i32 0, i32 0), i32 %var-20)
%var-23 = load float, float* %f, align 4
%var-24 = fpext float %var-23 to double
%var-25 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-22, i32 0, i32 0), double %var-24)
ret i32 0
}

