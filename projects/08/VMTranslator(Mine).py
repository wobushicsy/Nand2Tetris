import sys
import os

def main():
    if len(sys.argv) == 1:
        sys.exit("Arguments are less than expected. ")

    # initialization of virables
    segment = {
        "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", 
    }
    constant_segment = {
        "static": "16", "temp":"5"
    }
    staticRecord = {"Main":0}
    arithmatic_commands = ["add", "sub", "neg", "and", "or", "not"]
    logic_commands = ["eq", "gt", "lt"]
    logic_cnt = 0
    retAddr_cnt = 0

    if sys.argv[1][-3:] == ".vm":
        # only translate one VM file
        # Input: fileName.vm    Output: fileName.asm
        fileName = sys.argv[1]
        preName = fileName.lstrip(".\\").split(".")[0]
        
        # deal with comments and empty lines of source file and store it in *filename*.tmp
        tmp_file = open(f"{preName}.tmp", "w")
        source_file = open(fileName)
        write_code(source_file, tmp_file, staticRecord)
        tmp_file.close()
        source_file.close()
    else:
        # taranslate a whole directory of VM file
        # Input: directoryName  Output: directoryName.asm
        # write Sys.vm to tmp.vm first, then Main.vm, then else
        path = sys.argv[1]
        directoryName = path.strip().split("\\")[-2]
        tmp_file = open(f"{path}{directoryName}.tmp", "w")
        files = os.listdir(path)
        if "Sys.vm" in files:
            source_file = open(f"{path}Sys.vm")
            write_code(source_file, tmp_file, staticRecord)
        if "Main.vm" in files:
            source_file = open(f"{path}Main.vm")
            write_code(source_file, tmp_file, staticRecord)
        for file in files:
            if file[-3:] == ".vm" and file != "Main.vm" and file != "Sys.vm":
                source_file = open(f"{path}{file}")
                write_code(source_file, tmp_file, staticRecord)
        tmp_file.close()


    # prepared to translate VMcode to assembly code with the help of tmp_file
    if sys.argv[1][-3:] == ".vm":
        tmp_file = open(f"{preName}.tmp")
        target_file = open(f"{preName}.asm", "w")
    else:
        tmp_file = open(f"{path}{directoryName}.tmp")
        target_file = open(f"{path}{directoryName}.asm", "w")
    currentFunc = "Main"
    for row in tmp_file:
        commands = row.strip().split(" ")
        if len(commands) == 3:
            if commands[0] == "call":
                # deal with call commands
                call(target_file, commands, retAddr_cnt, staticRecord)
                retAddr_cnt += 1
            elif commands[0] == "function":
                # deal with function commands
                func_declaration(target_file, commands)
            else:
                # deal with push and pop commands
                if commands[0] == "push":
                    push(commands, target_file, segment, constant_segment, staticRecord)
                elif commands[0] == "pop":
                    pop(commands, target_file, segment, constant_segment, staticRecord)
        elif len(commands) == 2:
            # deal with branching commands
            if commands[0].find("goto") != -1:
                goto, label = commands
                if goto == "if-goto":
                    # deal with conditional jump
                    conditional_jump(target_file, label)
                else:
                    # deal with unconditional jump
                    unconditionl_jump(target_file, label)
            else:
                # deal with label declaration
                label = commands[1]
                label_declaration(target_file, label)
        elif len(commands) == 1:
            # deal with Arithmatic/Logic commands
            if commands[0] in arithmatic_commands:
                arithmatic(target_file, commands)
            elif commands[0] in logic_commands:
                logic(target_file, commands, logic_cnt)
                logic_cnt += 1
            elif commands[0] == "return":
                # deal with return commands
                ret(target_file)
    tmp_file.close()
    target_file.write("(INFINITY_LOOP)\n")
    target_file.write("@INFINITY_LOOP\n")
    target_file.write("0;JMP\n")
    target_file.close()
    if sys.argv[1][-3:] == ".vm":
        os.remove(f"{preName}.tmp")
    else:
        os.remove(f"{path}{directoryName}.tmp")

    tmp_file.close()



def write_code(source_file, target_file, staticRecord):
    for row in source_file:
        code = row.split("//")[0].strip()
        commands = code.split(" ")
        if len(code) != 0:
            target_file.write(f"{code}\n")
        if "function" in commands:
            currentFunc = commands[1]
            if currentFunc not in staticRecord.keys():
                staticRecord.update({currentFunc:0})
        elif "push" in commands and "static" in commands:
            staticRecord[currentFunc] += 1

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
        if commands[1] == "static":
            ...
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

def pop(commands, file, segment, constant_segment, staticRecord):
    value = ""
    # commands = ["pop", "segment", "i"]
    if commands[1] in segment:
        file.write("@" + commands[2] + "\n")                            # @i
        file.write("D=A\n")                                             # D=A
        file.write("@" + segment[commands[1]] + "\n")                   # @segment
        file.write("A=M+D\n")                                           # A=M+D     ->  A=[segment]+i
        file.write("D=A\n")                                             # D=A
    elif commands[1] in constant_segment:
        if commands[1] == "static":
            file.write(f"@{sum+16}\n")
        else:
            file.write("@" + commands[2] + "\n")                        # @i
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
    file.write("@255\n")                                               # @addr     
    file.write("M=D\n")                                                 # M=D       ->  addr=pop_pos
    file.write("@SP\n")                                                 # @SP
    file.write("AM=M-1\n")                                              # A=M-1     ->  A=SP--
    file.write("D=M\n")                                                 # D=M       ->  d=[SP]
    file.write("@255\n")                                               # @addr
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

def conditional_jump(file, label):
    file.write("@SP\n")
    file.write("AM=M-1\n")
    file.write("D=M\n")     
    file.write(f"@{label}\n")
    file.write("D;JNE\n")

def unconditionl_jump(file, label):
    file.write(f"@{label}\n")
    file.write("0;JMP\n")

def label_declaration(file, label):
    file.write(f"({label})\n")

def call(target_file, commands, retAddr_cnt, staticRecord):
    if commands[1] not in staticRecord.keys():
        staticRecord.update({commands[1]:0})
    target_file.write(f"@retAddrLabel{retAddr_cnt}\n")
    target_file.write("D=A\n")
    target_file.write("@SP\n")
    target_file.write("A=M\n")
    target_file.write("M=D\n")
    target_file.write("@SP\n")
    target_file.write("M=M+1\n")
    stack_push(target_file, "LCL")
    stack_push(target_file, "ARG")
    stack_push(target_file, "THIS")
    stack_push(target_file, "THAT")
    target_file.write(f"@{5+int(commands[2])}\n")
    target_file.write("D=A\n")
    target_file.write("@SP\n")
    target_file.write("D=M-D\n")
    target_file.write("@ARG\n")
    target_file.write("M=D\n")
    target_file.write("@SP\n")
    target_file.write("D=M\n")
    target_file.write("@LCL\n")
    target_file.write("M=D\n")
    unconditionl_jump(target_file, commands[1])
    target_file.write(f"(retAddrLabel{retAddr_cnt})\n")

def func_declaration(file, command):
    file.write(f"({command[1]})\n")
    for _ in range(int(command[2])):
        file.write("@SP\n")
        file.write("A=M\n")
        file.write("M=0\n")
        file.write("@SP\n")
        file.write("M=M+1\n")

def ret(file):
    file.write("@5\n")
    file.write("D=A\n")
    file.write("@LCL\n")
    file.write("A=M-D\n")
    file.write("D=M\n")
    file.write("@255\n")
    file.write("M=D\n")
    file.write("@SP\n")
    file.write("A=M-1\n")
    file.write("D=M\n")
    file.write("@ARG\n")
    file.write("A=M\n")
    file.write("M=D\n")
    file.write("@ARG\n")
    file.write("D=M+1\n")
    file.write("@254\n")
    file.write("M=D\n")
    file.write("@LCL\n")
    file.write("D=M\n")
    file.write("@SP\n")
    file.write("M=D\n")
    stack_pop(file, "THAT")
    stack_pop(file, "THIS")
    stack_pop(file, "ARG")
    stack_pop(file, "LCL")
    file.write("@254\n")
    file.write("D=M\n")
    file.write("@SP\n")
    file.write("M=D\n")
    file.write("@255\n")
    file.write("A=M\n")
    file.write("0;JMP\n")

def stack_push(file, label):
    file.write(f"@{label}\n")
    file.write("D=M\n") 
    file.write("@SP\n")
    file.write("A=M\n")
    file.write("M=D\n")
    file.write("@SP\n")
    file.write("M=M+1\n")

def stack_pop(file, label):
    file.write("@SP\n")
    file.write("AM=M-1\n")
    file.write("D=M\n")
    file.write(f"@{label}\n")
    file.write("M=D\n")




if __name__ == "__main__":
    main()