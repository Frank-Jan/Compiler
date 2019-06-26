declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)

@.var-23 = private unnamed_addr constant [9 x i8] c"f is %f\0A\00", align 1

@.var-19 = private unnamed_addr constant [9 x i8] c"c is %c\0A\00", align 1

@.var-16 = private unnamed_addr constant [9 x i8] c"i is %i\0A\00", align 1

@.var-3 = private unnamed_addr constant [5 x float] [float 0x3f847ae140000000, float 0x3f947ae140000000, float 0.0, float 0.0, float 0.0], align 16

@.var-2 = private unnamed_addr constant [6 x i8] [i8 97, i8 0, i8 0, i8 0, i8 0, i8 0], align 16

@.var-1 = private unnamed_addr constant [4 x i32] [i32 2, i32 3, i32 4, i32 5], align 16


define i32 @main() {
%arr1 = alloca [1 x i32], align 4
%Iarr = alloca [4 x i32], align 16
%var-4 = bitcast [4 x i32]* %Iarr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-4, i8* bitcast ([4 x i32]* @.var-1 to i8*), i64 8, i32 4, i1 false)
%Carr = alloca [6 x i8], align 16
%var-5 = bitcast [6 x i8]* %Carr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-5, i8* bitcast ([6 x i8]* @.var-2 to i8*), i64 8, i32 4, i1 false)
%Farr = alloca [5 x float], align 16
%var-6 = bitcast [5 x float]* %Farr to i8*
call void @llvm.memcpy.p0i8.p0i8.i64(i8* %var-6, i8* bitcast ([5 x float]* @.var-3 to i8*), i64 8, i32 4, i1 false)
%i = alloca i32, align 4
%var-8 = getelementptr inbounds [4 x i32], [4 x i32]* %Iarr, i64 0, i64 3
%var-9 = load i32, i32* %var-8, align 4
store i32 %var-9, i32* %i, align 4
%c = alloca i8, align 1
%var-11 = getelementptr inbounds [6 x i8], [6 x i8]* %Carr, i64 0, i64 0
%var-12 = load i8, i8* %var-11, align 1
store i8 %var-12, i8* %c, align 1
%f = alloca float, align 4
%var-14 = getelementptr inbounds [5 x float], [5 x float]* %Farr, i64 0, i64 1
%var-15 = load float, float* %var-14, align 4
store float %var-15, float* %f, align 4
%var-17 = load i32, i32* %i, align 4
%var-18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-16, i32 0, i32 0), i32 %var-17)
%var-20 = load i8, i8* %c, align 1
%var-21 = sext i8 %var-20 to i32
%var-22 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-19, i32 0, i32 0), i32 %var-21)
%var-24 = getelementptr inbounds [5 x float], [5 x float]* %Farr, i64 0, i64 1
%var-25 = load float, float* %var-24, align 4
%var-26 = fpext float %var-25 to double
%var-27 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([9 x i8], [9 x i8]* @.var-23, i32 0, i32 0), double %var-26)
ret i32 0
}

