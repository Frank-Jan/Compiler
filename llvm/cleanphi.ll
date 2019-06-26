declare i32 @printf(i8*, ...)
@format = private constant [8 x i8] c"d = %d\0A\00"

define void @print(i32 %a){
  %p = call i32 (i8*, ...)
       @printf(i8* getelementptr inbounds ([8 x i8],
                                           [8 x i8]* @format,
                                           i32 0, i32 0),
               i32 %a)
  ret void
}

define i32 @main() {
  start:
         ; set %tmp iff %a > %b
         %tmp = icmp sgt i32 2, 4
         ; %d = %tmp ? 1 : 2
         %d = select i1 %tmp, i32 1, i32 2
  ; everything below is for debugging
         call void (i32) @print(i32 %d)
  ; we exit with code 0 = success
         ret i32 0
}
