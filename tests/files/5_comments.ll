declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)


define i32 @main() {
%iets = alloca i32, align 4
store i32 0, i32* %iets, align 4
ret i32 0
}

