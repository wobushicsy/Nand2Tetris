@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@THIS
A=M+D
D=A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@THAT
A=M+D
D=A
@addr
M=D
@SP
AM=M-1
D=M
@addr
A=M
M=D
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
@2
D=A
@THIS
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
@6
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D
(INFINITY_LOOP)
@INFINITY_LOOP
0;JMP