declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)

@.var-32 = private unnamed_addr constant [15 x i8] c"while is done\0A\00", align 1

@.var-30 = private unnamed_addr constant [11 x i8] c"c changed\0A\00", align 1

@.var-20 = private unnamed_addr constant [25 x i8] c"f is kleiner dan 3.0123\0A\00", align 1

@.var-18 = private unnamed_addr constant [24 x i8] c"f is groter dan 3.0123\0A\00", align 1

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
%var-19 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([24 x i8], [24 x i8]* @.var-18, i32 0, i32 0))
br label %Label12

Label11:
%var-21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.var-20, i32 0, i32 0))
br label %Label12

Label12:
%c = alloca i8, align 1
store i8 99, i8* %c, align 1
br label %Label22

Label22:
%var-26 = load i8, i8* %c, align 1
%var-27 = sext i8 %var-26 to i32
%var-28 = icmp eq i32 %var-27, 99
br i1 %var-28, label %Label23, label %Label24

Label23:
store i8 97, i8* %c, align 1
%var-31 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.var-30, i32 0, i32 0))
br label %Label22

Label24:
%var-33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.var-32, i32 0, i32 0))
ret void 
}

