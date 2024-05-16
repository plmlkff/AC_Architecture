LEN: word 0
START:
    ld 1023
    wr LEN
    cmp #0
    je #end
loop:
    ld 1023
    wr 1022
    ld LEN
    sub #1
    je #end
    wr LEN
    jmp #loop
end:
    hlt