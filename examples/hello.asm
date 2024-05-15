WORD: word 'h'
    word 'e'
    word 'l'
    word 'l'
    word 'o'
    word ' '
    word 'w'
    word 'o'
    word 'r'
    word 'l'
    word 'd'
POINTER: word WORD
LENGTH: word 11
START:
    ld [POINTER]
    wr 1022
    ld POINTER
    add #1
    cmp LENGTH
    je #.end
    wr POINTER
    jmp #START
.end:
    hlt
