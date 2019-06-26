declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)


define i32 @definition(i32 %var-4) {
%i = alloca i32, align 4
store i32 %var-4, i32* %i, align 4
%var-5 = load i32, i32* %i, align 4
ret i32 %var-5
}

@.var-25 = private unnamed_addr constant [9 x i8] c"f is %f\0A\00", align 1

@.var-21 = private unnamed_addr constant [9 x i8] c"c is %c\0A\00", align 1

@.var-18 = private unnamed_addr constant [9 x i8] c"i is %i\0A\00", align 1

@.var-3 = private unnamed_addr constant [5 x float] [float 0x3f847ae140000000, float 0x3f947ae140000000, float 0.0, float 0.0, float 0.0], align 16

@.var-2 = private unnamed_addr constant [6 x i8] [i8 97, i8 0, i8 0, i8 0, i8 0, i8 0], align 16

@.var-1 = private unnamed_addr constant [4 x i32] [i32 2, i32 3, i32 4, i32 5], align 16


define i32 @main() {
%arr1 = alloca [1 x i32], align 4
%Iarr = alloca [4 x i32], align 16
%var-6 = bitcast [4 x i32]* %Iarr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-6, i8* bitcast ([4 x i32]* @.var-1 to i8*), i64 8, i32 4, i1 false)
%Carr = alloca [6 x i8], align 16
%var-7 = bitcast [6 x i8]* %Carr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-7, i8* bitcast ([6 x i8]* @.var-2 to i8*), i64 8, i32 4, i1 false)
%Farr = alloca [5 x float], align 16
%var-8 = bitcast [5 x float]* %Farr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-8, i8* bitcast ([5 x float]* @.var-3 to i8*), i64 8, i32 4, i1 false)
%i = alloca i32, align 4
%var-10 = getelementptr inbounds [4 x i32], [4 x i32]* %Iarr, i64 0, i64 3
%var-11 = load i32, i32* %var-10, align 4
store i32 %var-11, i32* %i, align 4
%c = alloca i8, align 1
%var-13 = getelementptr inbounds [6 x i8], [6 x i8]* %Carr, i64 0, i64 0
%var-14 = load i8, i8* %var-13, align 1
store i8 %var-14, i8* %c, align 1
%f = alloca float, align 4
%var-16 = getelementptr inbounds [5 x float], [5 x float]* %Farr, i64 0, i64 1
%var-17 = load float, float* %var-16, align 4
store float %var-17, float* %f, align 4
%var-19 = load i32, i32* %i, align 4
%var-20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-18, i32 0, i32 0), i32 %var-19)
%var-22 = load i8, i8* %c, align 1
%var-23 = sext i8 %var-22 to i32
%var-24 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-21, i32 0, i32 0), i32 %var-23)
%var-26 = load float, float* %f, align 4
%var-27 = fpext float %var-26 to double
%var-28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-25, i32 0, i32 0), double %var-27)
%k = alloca i32, align 4
%var-30 = call i32 @definition()
store i32 %var-30, i32* %k, align 4
ret i32 0
}

