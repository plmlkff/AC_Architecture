HELLO: word 'h'
    word 'e'
    word 'l'
    word 'l'
    word 'o'
    word ','
    word ' '
HELLO_LEN: word 7
EXCLAMATION: word '!'
WIYN: word 'W'
    word 'h'
    word 'a'
    word 't'
    word ' '
    word 'i'
    word 's'
    word ' '
    word 'y'
    word 'o'
    word 'u'
    word 'r'
    word ' '
    word 'n'
    word 'a'
    word 'm'
    word 'e'
    word '?'
    word 10
WIYN_LEN: word 19
NAME_LEN: word 0
WIYN_PTR: word WIYN
WIYN_END: word 0
HELLO_PTR: word HELLO
HELLO_END: word 0
START:
    ld WIYN_PTR
    add WIYN_LEN
    wr WIYN_END
.wiyn_loop:
    ld [WIYN_PTR]
    wr 1022
    ld WIYN_PTR
    add #1
    cmp WIYN_END
    je #.name
    wr WIYN_PTR
    jmp #.wiyn_loop
.name:
    ld 1023
    wr NAME_LEN
    cmp #0
    je #.hello
    add #BUFF
    wr BUFF_END
.read_name_loop:
    ld 1023
    wr [BUFF_PTR]
    ld BUFF_PTR
    add #1
    cmp BUFF_END
    je #.hello
    wr BUFF_PTR
    jmp #.read_name_loop
.hello:
    ld #BUFF
    wr BUFF_PTR
    ld HELLO_PTR
    add HELLO_LEN
    wr HELLO_END
.hello_loop:
    ld [HELLO_PTR]
    wr 1022
    ld HELLO_PTR
    add #1
    cmp HELLO_END
    je #.print_name_loop
    wr HELLO_PTR
    jmp #.hello_loop
.print_name_loop:
    ld [BUFF_PTR]
    wr 1022
    ld BUFF_PTR
    add #1
    cmp BUFF_END
    je #.print_exclamation
    wr BUFF_PTR
    jmp #.print_name_loop
.print_exclamation:
    ld EXCLAMATION
    wr 1022
.end:
    hlt
org 100
BUFF_END: word 0
BUFF_PTR: word BUFF
BUFF: word 0
