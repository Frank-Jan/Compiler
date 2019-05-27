define i32 @test(i32 %var-1) {
%i = alloca i32, align 4
store i32 %var-1, i32* %i, align 4
}

define i32 @main() {

}

