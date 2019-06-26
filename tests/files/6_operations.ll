declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)

@.var-44 = private unnamed_addr constant [15 x i8] c"while is done\0A\00", align 1

@.var-42 = private unnamed_addr constant [11 x i8] c"c changed\0A\00", align 1

@.var-32 = private unnamed_addr constant [25 x i8] c"f is kleiner dan 3.0123\0A\00", align 1

@.var-30 = private unnamed_addr constant [24 x i8] c"f is groter dan 3.0123\0A\00", align 1

@.var-20 = private unnamed_addr constant [19 x i8] c"i is groter dan 3\0A\00", align 1


define void @main() {
%i = alloca i32, align 4
%var-9 = add i32 1, 1
%var-8 = mul i32 %var-9, 1
%var-11 = sdiv i32 1, 1
%var-12 = sub i32 2, 1
%var-10 = add i32 %var-11, %var-12
%var-7 = add i32 %var-8, %var-10
store i32 %var-7, i32* %i, align 4
%var-17 = load i32, i32* %i, align 4
%var-18 = icmp sgt i32 %var-17, 3
br i1 %var-18, label %Label13, label %Label14

Label13:
%var-21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([19 x i8], [19 x i8]* @.var-20, i32 0, i32 0))
br label %Label15

Label14:
br label %Label15

Label15:
%f = alloca float, align 4
store float 0x3f8930be00000000, float* %f, align 4
%var-26 = load float, float* %f, align 4
%var-27 = fpext float %var-26 to double
%var-28 = fcmp olt double %var-27, 0x40081930c0000000
br i1 %var-28, label %Label22, label %Label23

Label22:
%var-31 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([24 x i8], [24 x i8]* @.var-30, i32 0, i32 0))
br label %Label24

Label23:
%var-33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([25 x i8], [25 x i8]* @.var-32, i32 0, i32 0))
br label %Label24

Label24:
%c = alloca i8, align 1
store i8 99, i8* %c, align 1
br label %Label34

Label34:
%var-38 = load i8, i8* %c, align 1
%var-39 = sext i8 %var-38 to i32
%var-40 = icmp eq i32 %var-39, 99
br i1 %var-40, label %Label35, label %Label36

Label35:
store i8 97, i8* %c, align 1
%var-43 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.var-42, i32 0, i32 0))
br label %Label34

Label36:
%var-45 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.var-44, i32 0, i32 0))
ret void 
}

