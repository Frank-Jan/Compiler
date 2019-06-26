declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)


define i32 @main() {
%i = alloca i32, align 4
store i32 0, i32* %i, align 4
%c = alloca i8, align 1
store i8 0, i8* %c, align 1
%f = alloca float, align 4
store float 0.0, float* %f, align 4
%pi = alloca i32*, align 8
%pc = alloca i8*, align 8
%pf = alloca float*, align 8
%ppi = alloca i32**, align 8
%ppc = alloca i8**, align 8
%ppf = alloca float**, align 8
%j = alloca i32, align 4
store i32 123, i32* %j, align 4
%d = alloca i8, align 1
store i8 83, i8* %d, align 1
%g = alloca float, align 4
store float 0x4012449ba0000000, float* %g, align 4
%pj = alloca i32*, align 8
store i32* %j, i32** %pj, align 8
%pd = alloca i8*, align 8
store i8* %d, i8** %pd, align 8
%pg = alloca float*, align 8
store float* %g, float** %pg, align 8
%ppj = alloca i32**, align 8
store i32** %pj, i32*** %ppj, align 8
%ppd = alloca i8**, align 8
store i8** %pd, i8*** %ppd, align 8
%ppg = alloca float**, align 8
store float** %pg, float*** %ppg, align 8
ret i32 0
}

