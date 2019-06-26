define i32 @foo(i32 %x) {
    start:
          ret i32 %x
}

declare i32 @printf(i8*, ...)
@format = private constant [8 x i8] c"a = %d\0A\00"

define i32 @main() {
    start:
          %a = call i32 @foo(i32 0)
          %a = add i32 %a, 1
    ; everything below is for debugging
          %p = call i32 (i8*, ...)
               @printf(i8* getelementptr inbounds ([8 x i8],
                                                   [8 x i8]* @format,
                                                   i32 0, i32 0),
                       i32 %a)
    ; we exit with code 0 = success
          ret i32 0
}
