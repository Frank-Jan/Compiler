declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)

@.var-36 = private unnamed_addr constant [15 x i8] c"while is done\0A\00", align 1

@.var-34 = private unnamed_addr constant [11 x i8] c"c changed\0A\00", align 1

@.var-22 = private unnamed_addr constant [30 x i8] c"f (%f) is kleiner dan 3.0123\0A\00", align 1

@.var-18 = private unnamed_addr constant [29 x i8] c"f (%f) is groter dan 3.0123\0A\00", align 1

@.var-8 = private unnamed_addr constant [19 x i8] c"i is groter dan 3\0A\00", align 1


define void @main() {
%i = alloca i32, align 4
store i32 2, i32* %i, align 4
%var-5 = load i32, i32* %i, align 4
%var-6 = icmp slt i32 %var-5, 3
br i1 %var-6, label %Label1, label %Label2

Label1:
%var-9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.var-8, i32 0, i32 0))
br label %Label3

Label2:
br label %Label3

Label3:
%f = alloca float, align 4
store float 0x3f8930be00000000, float* %f, align 4
%var-14 = load float, float* %f, align 4
%var-15 = fpext float %var-14 to double
%var-16 = fcmp ogt double %var-15, 0x40081930c0000000
br i1 %var-16, label %Label10, label %Label11

Label10:
%var-19 = load float, float* %f, align 4
%var-20 = fpext float %var-19 to double
%var-21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([29 x i8], [29 x i8]* @.var-18, i32 0, i32 0), double %var-20)
br label %Label12

Label11:
%var-23 = load float, float* %f, align 4
%var-24 = fpext float %var-23 to double
%var-25 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.var-22, i32 0, i32 0), double %var-24)
br label %Label12

Label12:
%c = alloca i8, align 1
store i8 99, i8* %c, align 1
br label %Label26

Label26:
%var-30 = load i8, i8* %c, align 1
%var-31 = sext i8 %var-30 to i32
%var-32 = icmp eq i32 %var-31, 99
br i1 %var-32, label %Label27, label %Label28

Label27:
store i8 97, i8* %c, align 1
%var-35 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.var-34, i32 0, i32 0))
br label %Label26

Label28:
%var-37 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.var-36, i32 0, i32 0))
ret void 
}

