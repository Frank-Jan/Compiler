



define i32 @main(){

%i = alloca i32, align 4
%var16 = call i32 @f(i32 3, i32 0)
store i32 %var16, i32* %i, align 4
%o = alloca i32, align 4
%var97 = load i32, i32* %i, align 4
%var96 = call i32 @f(i32 %var97, i32 0)
%var100 = call i32 @f(i32 2, i32 0)
%var101 = call i32 @f(i32 2, i32 0)
%var98 = sdiv i32 %var100, %var101
%var93 = sub i32 %var96, %var98
%var102 = call i32 @f(i32 3, i32 0)
%var83 = mul i32 %var93, %var102
%var104 = mul i32 0, 32
%var103 = sub i32 4, %var104
%var62 = add i32 %var83, %var103
store i32 %var62, i32* %o, align 4
%k = alloca i32, align 4
%var108 = load i32, i32* %i, align 4
store i32 %var108, i32* %k, align 4
%j = alloca i32, align 4
store i32 0, i32* %j, align 4
%var112 = load i32, i32* %o, align 4
ret i32 %var112
}

define i32 @f(i32 %var1, i32 %var2){
%i = alloca i32, align 4
store i32 %var1, i32* %i, align 4
%o = alloca i32, align 4
store i32 %var2, i32* %o, align 4

%var7 = load i32, i32* %i, align 4
%var10 = load i32, i32* %o, align 4
%var13 = load i32, i32* %i, align 4
%var11 = sub i32 %var13, 0
%var8 = sdiv i32 %var10, %var11
%var5 = add i32 %var7, %var8
ret i32 %var5
}