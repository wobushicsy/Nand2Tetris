@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE0
D;JEQ
@SP
A=M-1
M=0
@OUT0
0;JMP
(TRUE0)
@1
D=-A
@SP
A=M-1
M=D
(OUT0)
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE1
D;JEQ
@SP
A=M-1
M=0
@OUT1
0;JMP
(TRUE1)
@1
D=-A
@SP
A=M-1
M=D
(OUT1)
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE2
D;JEQ
@SP
A=M-1
M=0
@OUT2
0;JMP
(TRUE2)
@1
D=-A
@SP
A=M-1
M=D
(OUT2)
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@890
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE3
D;JLT
@SP
A=M-1
M=0
@OUT3
0;JMP
(TRUE3)
@1
D=-A
@SP
A=M-1
M=D
(OUT3)
@890
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE4
D;JLT
@SP
A=M-1
M=0
@OUT4
0;JMP
(TRUE4)
@1
D=-A
@SP
A=M-1
M=D
(OUT4)
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE5
D;JLT
@SP
A=M-1
M=0
@OUT5
0;JMP
(TRUE5)
@1
D=-A
@SP
A=M-1
M=D
(OUT5)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE6
D;JGT
@SP
A=M-1
M=0
@OUT6
0;JMP
(TRUE6)
@1
D=-A
@SP
A=M-1
M=D
(OUT6)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE7
D;JGT
@SP
A=M-1
M=0
@OUT7
0;JMP
(TRUE7)
@1
D=-A
@SP
A=M-1
M=D
(OUT7)
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE8
D;JGT
@SP
A=M-1
M=0
@OUT8
0;JMP
(TRUE8)
@1
D=-A
@SP
A=M-1
M=D
(OUT8)
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@SP
A=M-1
M=-M
@SP
AM=M-1
D=M
A=A-1
M=M&D
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M|D
@SP
A=M-1
M=!M
(INFINITY_LOOP)
@INFINITY_LOOP
0;JMP