// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
    @8192
    D = A
    @R0
    M = D       // set R0 = 8192, which is the length of SCREEN
    (LOOP)
    @i
    M = 0       // set i = 0
    @KBD
    D = M
    @BLACKEN
    D;JGT       // jump BLACKEN if the keyboard is pressed
    @WHITEN
    D;JEQ       // jump WHITEN if the keyboard isn't pressed
    (RETURN)
    @LOOP
    0;JMP       

    (BLACKEN)   // a function that blacken all pixels
    (BLACKENLOOP)
    @i
    D = M
    @R0
    D = D-M
    @RETURN
    D;JEQ       // i == RAM[0], return
    @i
    D = M
    @SCREEN
    A = A+D     // A = SCREEN + i
    M = -1

    @i
    M = M+1     // i++

    @BLACKENLOOP
    0;JMP

    (WHITEN)   // a function that blacken all pixels
    (WHITENLOOP)
    @i
    D = M
    @R0
    D = D-M
    @RETURN
    D;JEQ       // i == RAM[0], return
    @i
    D = M
    @SCREEN
    A = A+D     // A = SCREEN + i
    M = 0

    @i
    M = M+1     // i++

    @WHITENLOOP
    0;JMP