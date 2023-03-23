import os
import sys


def main():
    if len(sys.argv) == 1:
        sys.exit("Arguments are less than expected. ")

    # pre_defined labels
    label_table = {
        "SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,
        "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,
        "R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,
        "R12":12,"R13":13,"R14":14,"R15":15,
        "SCREEN":16384,"KBD":24576
        }
    comp_table={
        "0":"0101010","1":"0111111","-1":"0111010",
        "D":"0001100","A":"0110000","!D":"0001101", 
        "!A":"0110001","-D":"0001111","-A":"0110011",
        "D+1":"0011111","A+1":"0110111","D-1":"0001110",
        "A-1":"0110010","D+A":"0000010","D-A":"0010011",
        "A-D":"0000111","D&A":"0000000","D|A":"0010101",
        "M":"1110000","!M":"1110001","-M":"1110011",
        "M+1":"1110111","M-1":"1110010","D+M":"1000010",
        "D-M":"1010011","M-D":"1000111","D&M":"1000000",
        "D|M":"1010101"
        }
    dest_table={
        "null":"000","M":"001","D":"010","MD":"011",
        "A":"100","AM":"101","AD":"110","AMD":"111"
        }
    jmp_table={
        "null":"000","JGT":"001","JEQ":"010","JGE":"011",
        "JLT":"100","JNE":"101","JLE":"110","JMP":"111"
        }
    variable_pos = 16
    fileName = sys.argv[1]
    preName = fileName.lstrip(".\\").split(".")[0]
    tmp_file1 = open(f"{preName}.tmp", "w")
    source_file = open(f"{fileName}")

    # deal with comments and empty lines of source file and store it in *filename*.tmp
    for row in source_file:
        code = row.split("//")[0].strip()
        if len(code) != 0:
            tmp_file1.write(f"{code}\n")

    # deal with (labels) and add them into label_table
    tmp_file1 = open(f"{preName}.tmp")
    tmp_file2 = open(f"{preName}.tmp1", "w")
    cnt = 0
    for row in tmp_file1:
        if row[0] == "(" and row[-2] == ")":
            label = row.lstrip("(").rstrip(")\n")
            label_table.update({f"{label}":cnt})
        else:
            tmp_file2.write(f"{row}")
            cnt += 1
    tmp_file1 = open(f"{preName}.tmp")
    for row in tmp_file1:
        if row[0] == "@" and not row[1:].strip().isnumeric() and row[1:].strip() not in label_table:
            label_table.update({row[1:].strip(): variable_pos})
            variable_pos += 1
            cnt += 1
    tmp_file1.close()
    tmp_file2.close()
    os.remove(f"{preName}.tmp")

    # translate HackAssembly language to machine language with all label processed
    tmp_file1 = open(f"{preName}.tmp1", "r")
    target_file = open(f"{preName}.hack", "w")
    target_string = ""
    for row in tmp_file1:
        # deal with "A instructions"
        if row[0] == "@":
            if row[1:].strip() in label_table:
                num = bin(label_table[row[1:].strip()])
            else:
                num = bin(int(row[1:].strip()))
            for _ in range(16-len(num[2:])):
                target_string += "0"
            target_string += num[2:]
            target_file.write(f"{target_string}\n")
        # deal with "C instructions"
        else:
            if "=" in row and ";" in row:
                dest, comp = row.split("=")
                comp, jmp = comp.split(";")
                dest = dest.strip()
                comp = comp.strip()
                jmp = jmp.strip()
            elif "=" in row and ";" not in row:
                jmp = "null"
                dest, comp = row.split("=")
                dest = dest.strip()
                comp = comp.strip()
            elif "=" not in row and ";" in row:
                dest = "null"
                comp, jmp = row.split(";")
                comp = comp.strip()
                jmp = jmp.strip()
            for _ in range(3):
                target_string += "1"
            target_string += comp_table[comp]
            target_string += dest_table[dest]
            target_string += jmp_table[jmp]
            target_file.write(f"{target_string}\n")
        target_string = ""
    tmp_file1.close()
    target_file.close()
    os.remove(f"{preName}.tmp1")



if __name__ == "__main__":
    main()