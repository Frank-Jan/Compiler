

define i32 @main(){

%a = alloca i8, align 1
store i8 97, i8* %a, align 1

%c = alloca i8*, align 8

store i8* %a, i8** %c, align 8

ret i32 0
}

