define i32 @test() {
ret i32 5
}

define i32 @test2(i32 %var-1) {
%q = alloca i32, align 4
store i32 %var-1, i32* %q, align 4
%var-2 = load i32, i32* %q, align 4
ret i32 %var-2
}

define i32 @main() {
%j = alloca i32, align 4
store i32 0, i32* %j, align 4
%k = alloca i32, align 4
int5%var-3 = call i32 @test2(i32 5)
ret i32 %var-3
}

