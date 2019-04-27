

define i8* @func(i8* %var-1){
%q = alloca i8*, align 4
store i8* %var-1, i8** %q, align 4

%var-3 = load i8*, i8** %q, align 8
ret i8* %var-3
}

define i32 @main(){

%a = alloca i8, align 1
store i8 97, i8* %a, align 1

%c = alloca i8*, align 8
store i8* %a, i8** %c, align 4

ret i32 0
}

