define i32 @function(i32 %var-1){
%j = alloca i32, align 4
store i32 %var-1, i32* %j, align 4

%var-3 = load i32, i32* %j, align 4
ret i32 %var-3
}

define i32 @main(){

%a = alloca i32, align 4
store i32 0, i32* %a, align 4

store %var-7 = load i32, i32* %a, align 4
%var-6 = call i32 @function(i32 %var-7)
%var-7 = load i32, i32* %a, align 4
, i32* %a, align 4

ret i32 0
}

