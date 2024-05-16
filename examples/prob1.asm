NUMBER: word 999
SUM: word 0
LOOP: ld #3
    push
    call #check_div
    cmp #1
    je #make_sum
    ld #5
    push
    call #check_div
    cmp #1
    je #make_sum
    ld NUMBER
    sub #1
    je #end
    wr NUMBER
    jmp #LOOP
make_sum: ld SUM
    add NUMBER
    wr SUM
    ld NUMBER
    sub #1
    je #end
    wr NUMBER
    jmp #LOOP
end:
    ld SUM
    hlt
DIVIDER: word 0
check_div: pop
    swap
    wr DIVIDER
    cmp #0
    je #bad_end
    ld NUMBER
loop: sub DIVIDER
    jl #bad_end
    je #good_end
    jmp #loop
good_end: ld #1
    ret
bad_end: ld #0
    ret
