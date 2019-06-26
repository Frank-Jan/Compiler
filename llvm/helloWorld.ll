@formatString = private constant [1 x i32] c"%tmp2" 


define i32 @add(i32 %a, i32 %b){
entry:
	%tmp1 = add i32 %a, %b
	ret i32 %tmp1
}

define i32 @main() #0 {
  %1 = alloca i32, align 4
  %tmp2 = call i32 @add(i32 1, i32 2)
  %call = call i32 (i32*, ...)* @printf(i32* getelementptr inbounds ([1 x i32], [1 x i32]* @formatString , i32 0, i32 0), i32 %tmp2)

  store i32 0, i32* %1
  ret i32 0
}

declare i32 @printf(i32*, ...)

