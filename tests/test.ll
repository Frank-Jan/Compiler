

@str-i = private unnamed_addr constant [3 x i8] c"%i\00", align 1
@str-f = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@str-c = private unnamed_addr constant [3 x i8] c"%c\00", align 1

declare i32 @printf(i8*, ...)



define i32 @main(){

%i = alloca i32, align 4
store i32 0, i32* %i, align 4

%j = alloca i32, align 4
store i32 2, i32* %j, align 4

%q = alloca i8, align 1
store i8 99, i8* %q, align 1

%c = alloca i8*, align 8

store i8* %q, i8** %c, align 8

ret i32 0
}

