MAX: word 999
SUM: word 0
VAL: word 0
S_VAL: word 0
START: ld VAL
loop_three:
    ld VAL
    add #3
    cmp MAX
    jg #end
    wr VAL
    cmp S_VAL
    je #loop_five
    add SUM
    wr SUM
    ld VAL
    cmp S_VAL
    jg #loop_five
    jmp #loop_three
loop_five:
    ld S_VAL
    add #5
    cmp MAX
    jg #loop_three ; Переход на цикл тройки, так как она будет дорастать медленнее
    wr S_VAL
    cmp VAL
    je #loop_three
    add SUM
    wr SUM
    ld S_VAL
    cmp VAL
    jg #loop_three
    jmp #loop_five
end:
    ld SUM
    hlt