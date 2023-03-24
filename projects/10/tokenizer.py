import os
import sys

class tokenizer():
    keyword = ["class", "constructor", "function",
               "method", "field", "static", "var",
               "int", "char", "boolean", "void", 
               "true", "flase", "null", "this", "let",
               "do", "if", "else", "while", "return"
               ]
    symbol = ["{", "}", "(", ")", "[", "]", ".", ",",
              ";", "+", "-", "*", "/", "&", "|", "<", 
              ">", "=", "~"]

    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        self.tabcnt = 0
    
    def seperator(self):
        # comments process, sqperate symbols and write it into tmpfile
        tmpfile = open(self.path + self.filename.split(".")[0] + ".tokentmp", "w")
        srcfile = open(self.path + self.filename)
        commentsflag = 0
        strflag = 0
        for row in srcfile:
            if "/*" in row and "*/" not in row:
                commentsflag = 1
                continue
            if "*/" in row:
                commentsflag = 0
                row = row.split("*/")[1].strip()
            if commentsflag and "*/" not in row:
                continue
            row = row.split("//")[0].strip()
            if len(row) == 0:
                continue
            newrow = ""
            for i in range(len(row)-1):
                newrow += row[i]
                if strflag == 0:
                    if row[i] == '"':
                        strflag = 1
                        continue
                else:
                    if row[i] == '"':
                        strflag = 0
                    continue
                if isIdentifier(row[i]) and isIdentifier(row[i+1]):
                    continue
                else:
                    newrow += " "
            newrow += row[-1]
            if '"' in newrow:
                strcons = newrow.split('"')
                for i in range(len(strcons)):
                    if i % 2 == 1:
                        strcons[i] = '"' + strcons[i] + '"'
                newrow = []
                for token in strcons:
                    if '"' in token:
                        newrow.append(token)
                    else:
                        newrow += (token.split(" "))
            else:
                newrow = newrow.split(" ")
            for token in newrow:
                token = token.strip()
                if token == "\n" or len(token) == 0:
                    continue
                tmpfile.write(token + '\n')
        tmpfile.close()
        srcfile.close()

    def tokenizer(self):
        srcfile = open(self.path + self.filename.split(".")[0] + ".tokentmp")
        decfile = open(self.path + self.filename.split(".")[0] + ".token", "w")
        for row in srcfile:
            if row in self.keyword:
                tokentype = "keyword"
            elif row in self.symbol:
                tokentype = "symbol"
            elif row.isnumeric():
                tokentype = "integerConstant"
            elif '"' in row:
                tokentype = "StringConstant"
            else:
                tokentype = "identifier"
            decfile.write("<"+tokentype+"> "+row.strip()+" </"+tokentype+">\n")
        srcfile.close()
        decfile.close()

def isIdentifier(char):
    return char.isalnum() or char == "_"


            





def main():
    test = tokenizer("F:\\CSSelfLearning\\5Nand2Tetris\\projects\\10\\ArrayTest\\", "Main.jack")
    test.seperator()
    test.tokenizer()

if __name__ == "__main__":
    main()