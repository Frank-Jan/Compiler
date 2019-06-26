declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

declare i32 @scanf(i8*, ...)


define i32 @main() {
%i = alloca i32, align 4
store i32 1, i32* %i, align 4
%c = alloca i8, align 1
store i8 97, i8* %c, align 1
%f = alloca float, align 4
store float 0x3ff3be76c0000000, float* %f, align 4
ret i32 0
}

