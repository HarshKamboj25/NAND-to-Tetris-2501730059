// Nand to Tetris Capstone: Make the Computer Draw a Box
// Student: Harsh Kamboj | Roll: 2501730059 | K = 59
// Box: starts at row 59, height 20 rows, width 64 pixels (4 words).
// While any key is pressed, draw black; otherwise clear the same rectangle.

    @18272
    D=A
    @SCREEN_PTR
    M=D
    @20
    D=A
    @ROWS_LEFT
    M=D

(LOOP)
    // Select drawing color from keyboard state.
    @KBD
    D=M
    @DRAW_BLACK
    D;JGT

(CLEAR_COLOR)
    @COLOR
    M=0
    @RENDER
    0;JMP

(DRAW_BLACK)
    @COLOR
    M=-1

(RENDER)
    @4
    D=A
    @WORDS_LEFT
    M=D

(WORD_LOOP)
    @COLOR
    D=M
    @SCREEN_PTR
    A=M
    M=D

    @SCREEN_PTR
    M=M+1

    @WORDS_LEFT
    MD=M-1
    @WORD_LOOP
    D;JGT

    // Four words were written. Skip the remaining 28 words in this row.
    @28
    D=A
    @SCREEN_PTR
    M=D+M

    @ROWS_LEFT
    MD=M-1
    @LOOP
    D;JGT

    // Start the next frame at the first box row.
    @18272
    D=A
    @SCREEN_PTR
    M=D
    @20
    D=A
    @ROWS_LEFT
    M=D
    @LOOP
    0;JMP
