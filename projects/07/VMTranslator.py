import sys
import os

def main():
    if len(sys.argv) == 1:
        sys.exit("Arguments are less than expected. ")

    segment = {
        "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", 
    }
    constant_segment = {
        "static": "16", "temp":"5"
    }
    arithmatic_commands = ["add", "sub", "neg", "and", "or", "not"]
    logic_commands = ["eq", "gt", "lt"]
    i = 0
    fileName = sys.argv[1]
    preName = fileName.lstrip(".\\").split(".")[0]
    
    # deal with comments and empty lines of source file and store it in *filename*.tmp
    tmp_file = open(f"{preName}.tmp", "w")
    source_file = open(fileName)
    for row in source_file:
        code = row.split("//")[0].strip()
        if len(code) != 0:
            tmp_file.write(f"{code}\n")
    tmp_file.close()
    source_file.close()

    # prepared to translate VMcode to assembly code with the help of tmp_file
    tmp_file = open(f"{preName}.tmp")
    target_file = open(f"{preName}.asm", "w")
    for row in tmp_file:
        commands = row.strip().split(" ")
        if len(commands) == 3:
            # deal with push and pop commands
            if commands[0] == "push":
                push(commands, target_file, segment, constant_segment)
            elif commands[0] == "pop":
                pop(commands, target_file, segment, constant_segment)
        elif len(commands) == 1:
            # deal with Arithmatic/Logic commands
            if commands[0] in arithmatic_commands:
                arithmatic(target_file, commands)
            elif commands[0] in logic_commands:
                logic(target_file, commands, i)
                i += 1
    tmp_file.close()
    target_file.write("(INFINITY_LOOP)\n")
    target_file.write("@INFINITY_LOOP\n")
    target_file.write("0;JMP\n")
    target_file.close()
    os.remove(f"{preName}.tmp")


    
    
    tmp_file.close()

def push(commands, file, segment, constant_segment):
    value = ""
    # commands = ["push", "segment", "i"]
    if commands[1] in segment:
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A       ->  D=i
        file.write("@" + segment[commands[1]] + "\n")                   # @segment
        file.write("A=M+D\n")                                           # A=M+D     ->  A=[segment]+i
        file.write("D=M\n")                                             # D=M       ->  D=[segment+i]
    elif commands[1] in constant_segment:
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A       ->  D=i
        file.write("@" + constant_segment[commands[1]] + "\n")          # @static   ->  @static
        file.write("A=A+D\n")                                           # A=A+D     ->  A=stctic+i
        file.write("D=M\n")                                             # D=M       ->  D=[static+i]
    elif commands[1] == "constant":
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A
    else:
        # segment == pointer
        if commands[2] == "0":
            value = "THIS"
        elif commands[2] == "1":
            value = "THAT"
        file.write("@" + value + "\n")                                  # @THIS/@THAT
        file.write("D=M\n")                                             # D=A
    file.write("@SP\n")                                                 # @SP
    file.write("A=M\n")                                                 # A=M       ->  A=[SP]
    file.write("M=D\n")                                                 # M=D       ->  M=D
    file.write("@SP\n")                                                 # @SP
    file.write("M=M+1\n")                                               # M=M+1     ->  SP++

def pop(commands, file, segment, constant_segment):
    value = ""
    # commands = ["pop", "segment", "i"]
    if commands[1] in segment:
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A
        file.write("@" + segment[commands[1]] + "\n")                   # @segment
        file.write("A=M+D\n")                                           # A=M+D     ->  A=[segment]+i
        file.write("D=A\n")                                             # D=A
    elif commands[1] in constant_segment:
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A       ->  D=i
        file.write("@" + constant_segment[commands[1]] + "\n")          # @static   ->  @static
        file.write("A=A+D\n")                                           # A=A+D     ->  A=stctic+i
        file.write("D=A\n")                                             # D=M       ->  D=[static+i]
    else:
        # segment == pointer
        if commands[2] == "0":
            value = "THIS"
        elif commands[2] == "1":
            value = "THAT"
        file.write("@" + value + "\n")                                  # @THIS/@THAT
        file.write("D=A\n")                                             # D=A
    file.write("@addr\n")                                               # @addr     
    file.write("M=D\n")                                                 # M=D       ->  addr=pop_pos
    file.write("@SP\n")                                                 # @SP
    file.write("AM=M-1\n")                                              # A=M-1     ->  A=SP--
    file.write("D=M\n")                                                 # D=M       ->  d=[SP]
    file.write("@addr\n")                                               # @addr
    file.write("A=M\n")                                                 # A=M       ->  A=[addr]
    file.write("M=D\n")                                                 # M=D

def arithmatic(file, commands):
    file.write("@SP\n")                                                 # @SP
    if commands[0] == "add":
        file.write("AM=M-1\n")                                          # AM=M-1    ->  SP--
        file.write("D=M\n")                                             # D=M
        file.write("A=A-1\n")                                           # A=A-1     ->  SP--
        file.write("M=M+D\n")                                           # M=M+D     ->  [SP]=[SP]+[SP+1]
    elif commands[0] == "sub":
        file.write("AM=M-1\n")                                          # AM=M-1    ->  SP--
        file.write("D=M\n")                                             # D=M
        file.write("A=A-1\n")                                           # A=A-1     ->  SP--
        file.write("M=M-D\n")                                           # M=M+D     ->  [SP]=[SP]-[SP+1]
    elif commands[0] == "and":
        file.write("AM=M-1\n")                                          # AM=M-1    ->  SP--
        file.write("D=M\n")                                             # D=M
        file.write("A=A-1\n")                                           # A=A-1     ->  SP--
        file.write("M=M&D\n")                                           # M=M&D     ->  [SP]=[SP]&[SP+1]
    elif commands[0] == "or":
        file.write("AM=M-1\n")                                          # AM=M-1    ->  SP--
        file.write("D=M\n")                                             # D=M
        file.write("A=A-1\n")                                           # A=A-1     ->  SP--
        file.write("M=M|D\n")                                           # M=M&D     ->  [SP]=[SP]|[SP+1]
    elif commands[0] == "neg":
        file.write("A=M-1\n")                                           # A=M-1     ->  SP--
        file.write("M=-M\n")                                            # M=-M
    elif commands[0] == "not":
        file.write("A=M-1\n")                                           # A=M-1     ->  SP--
        file.write("M=!M\n")                                            # M=-M

def logic(file, commands, i):
    # push -1 if logic is true, push 0 if logic is false
    file.write("@SP\n")                                                 # @SP
    file.write("AM=M-1\n")                                              # AM=M-1    ->  SP--
    file.write("D=M\n")                                                 # D=M
    file.write("A=A-1\n")                                               # A=A-1
    file.write("D=M-D\n")                                               # D=M-D
    file.write(f"@TRUE{i}\n")
    if commands[0] == "eq":
        file.write("D;JEQ\n")                                           # D;JEQ
    elif commands[0] == "gt":
        file.write("D;JGT\n")                                           # D;JGT
    elif commands[0] == "lt":
        file.write("D;JLT\n")                                           # D;JLT
    file.write("@SP\n")                                                 # @SP
    file.write("A=M-1\n")                                               # A=A-1
    file.write("M=0\n")                                                 # M=0
    file.write(f"@OUT{i}\n")                                            # @OUTi
    file.write("0;JMP\n")                                               # 0;JMP
    file.write(f"(TRUE{i})\n")                                          # (TRUEi)
    file.write("@1\n")                                                  # @1
    file.write("D=-A\n")                                                # D=-A
    file.write("@SP\n")                                                 # @SP
    file.write("A=M-1\n")                                               # A=M-1
    file.write("M=D\n")                                                 # M=D
    file.write(f"(OUT{i})\n")                                           # (OUTi)




if __name__ == "__main__":
    main()