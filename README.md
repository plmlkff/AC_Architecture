# Лабораторная работа №3
## Вариант:
asm | acc | neum | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob1 | cache

Вариант с усложнением\
Язык: Python
## Язык программирования ASM
### Синтаксис
```ebnf
<program> ::= single_line |  single_line "\n" program

<single_line> ::= label command_line | comand_line

<label> ::= label_name ":(\s | \n)"

<label_name> ::= <any of "a-z A-Z _"> | start_section

<start_section> ::= "START:" ("\s" | "\n")

<command_line> ::= op_code | op_code address | op_code address comment



<op_code> ::= nope
   | add
   | sub
   | ld
   | wr
   | push
   | pop
   | swap
   | call
   | ret
   | cmp
   | jmp
   | je
   | jne
   | jg
   | jl
   | hlt
   | word
   | org
   
<address> ::= integer
            | label
            | "#"integer
            | "#"label
            | ("+" | "-") integer
            | ("+" | "-") label
            | "["  integer "]"
            | "[" label "]"
            | "[" ("+" | "-") integer "]"
            | "[" ("+" | "-") label "]"
            | character
            
<comment> ::= ";" <any of "a-zA-Z0-9">
            
<integer> ::= <any of "0-9">

<character> ::= "'" "a-zA-Z0-9" "'"

```
### Семантика
Операции:\
+ `add` – суммировать значение по адресу с AC
+ `sub` – вычесть значение по адресу из AC
+ `ld` – загрузить значение по адресу в AC
+ `wr` – записать значение из AC по адресу
+ `push` – положить значение из AC на стек
+ `pop` – снять значение со стека в AC
+ `swap` – обменять значение на стеке и в AC
+ `call` – выполнить вызов функции
+ `ret` – выполнить возврат из функции
+ `cmp` – пробно вычесть значение из AC по адресу, расставив флаги 
+ `jmp` – выполнить безусловный переход по адресу
+ `je` – выполнить переход, если Z == 1
+ `jne` – выполнить переход, если Z == 0
+ `jg` – выполнить переход, если N == 0 и Z == 0
+ `jl` – выполнить переход, если N == 1 и Z == 0
+ `hlt` – останов
+ `word` – вынести данные в ячейку
+ `org` – переход на указанный адрес

### Адресации
+ `123` – прямая-абсолютная. Указывает на значение по адресу ячейки
+ `(+|-)123` – прямая-относительная. Указывает на значение ячейки с адресом AR + смещение
+ `[123]` – косвенная-прямая. Указывает на значение по адресу, лежащем в адресованной ячейке
+ `[(+|-)123]` – стековая относительная. Указывает на значение ячейки по адресу SP + смещение
+ `#123` – прямая загрузка операнда в команду

### Литералы
+ Поддерживается два типа: `число` и `символ`
+ `Число` – преобразуется и загружается напрямую
+ `Символ` – преобразуется в код символа и работает также, как числовой

## Организация памяти
+ Фон-Неймановская архитектура – общая память для инструкций и данных
+ Размер машинного слова не определен (данные в памяти представляют из себя структуры данных)
+ Инструкция и данные взаимо-конвертируемы

Память адресуется двумя регистрами:
+ `AR` – регистр адреса для обращения к памяти
+ `SP` – регистр, указывающий на верхушку стека

### Модель памяти
```text
   Registers
+------------------------------+
| AC     IP     SP      DR     |
| BR     AR     IP             |
+------------------------------+

  Instruction and data memory
+------------------------------+
| 00   : value                 |
| 01   : value                 |
| 02   : value                 |
|     ...                      |
| n    : program start         |
|      : hlt                   |
|     ...                      |
| i    : function 0            |
|     ...                      |
| 1022 : output                |
| 1023 : input                 |
+------------------------------+
```
## ISA
| Мнемоника | Синтаксис | Количество тактов | Описание                                                                      |
|-----------|-----------|-------------------|-------------------------------------------------------------------------------|
| add       | add 123   | 2                 | Cуммировать значение по адресу с AC                                           |
| sub       | sub 123   | 2                 | Вычесть значение по адресу из AC                                              |
| ld        | ld 123    | 2                 | Загрузить значение по адресу в AC                                             |
| wr        | wr 123    | 2                 | Записать значение из AC по адресу                                             |
| push      | push      | 3                 | Положить значение из AC на стек                                               |
| pop       | pop       | 5                 | Снять значение со стека в AC                                                  |
| swap      | swap      | 6                 | Обменять значение на стеке и в AC                                             |
| call      | call #123 | 5                 | Выполнить вызов функции (использовать прямую загрузку адреса)                 |
| ret       | ret       | 5                 | Выполнить возврат из функции                                                  |
| cmp       | cmp       | 2                 | Пробно вычесть значение из AC по адресу, расставив флаги                      |
| jmp       | jmp #123  | 2                 | Выполнить безусловный переход по адресу (использовать прямую загрузку адреса) |
| je        | je #123   | 3                 | Выполнить переход, если Z == 1 (использовать прямую загрузку адреса)          |
| jne       | jne #123  | 3                 | Выполнить переход, если Z == 0 (использовать прямую загрузку адреса)          |
| jg        | jg #123   | 3                 | Выполнить переход, если N == 0 и Z == 0 (использовать прямую загрузку адреса) |
| jl        | jl #123   | 3                 | Выполнить переход, если N == 1 и Z == 0 (использовать прямую загрузку адреса) |
| hlt       | hlt       | 1                 | Завершить работу машины                                                       |
| word      | word 123  | транслятор        | Внести данные в ячейку                                                        |
| org       | org 123   | транслятор        | Перейти по адресу                                                             |

## Формат инструкций
Инструкции хранятся в формате JSON:
```json
{
  "name": "ld",
  "op_code": "LD", 
  "addressing_type": "DIRECT_LOAD", 
  "is_start": false, 
  "address": 3
}
```
Поля инструкции:
+ `name` – мнемоника инструкции
+ `op_code` – код операции
+ `addressing_type` – тип адресации
+ `is_start` – является ли стартовой (после метки START)
+ `address` – аргумент команды

## Транслятор
### Интерфейс командной строки:
`Translator.py <input_file> <output_file>`\
[Translator.py](Translator.py)

### Этапы трансляции
+ Считывание данных из файла
+ Удаление `комментариев`
+ Поиск и замена `меток` и `символьных литералов`
+ Сбор `лексем` с помощью `регулярных выражений` и работы конечного автомата
+ `Анализ лексем` на наличие синтаксических ошибок
+ `Конвертация` лексем в команды и формирования стека памяти
+ `Сохранение` полученного файла

Сбор лексем осуществляется за счет разбиения исходного файла на слова и парсинга их регулярными выражениями.
Анализ происходит с помощью конечного автомата.
Полученная лексема отмечается и сохраняется в список лексем.\
В случае перехода автомата в состояние ошибки, трансляция прекращается, а пользователю выводится проблемная лексема и возможное исправление.\
После работы конечного автомата, полученные лексемы преобразуются в команды.\
#### Автоматная грамматика
```text
S    -> (^[a-zA-Z]+$)MNC | E
MNC  -> ( ^(\[|\+|-|#){0,1}\d+(\]){0,1}$ )ADDR | (^[a-zA-Z]+$)MNC
ADDR -> (^[a-zA-Z]+$)MNC | E
E    -> to stderr
```
## Процессор
### Интерфейс командной строки
`Machine.py <code_file> <input_stream_file> <logs_file>`\
[Machine.py](Machine.py)

### Datapath
![img.png](resources/proc.png)
#### Сигналы
+ `latch_AC` – защелкнуть AC
+ `latch_BR` – защелкнуть BR
+ `latch_DR` – защелкнуть DR
+ `latch_CR` – защелкнуть CR
+ `latch_SP` – защелкнуть SP
+ `latch_IP` – защелкнуть IP
+ `latch_AR` – защелкнуть AR
+ `rd_mem` – считать из памяти по AR
+ `wr_mem` – записать в память по AR
+ `load_AC` – загрузить AC на левый вход ALU
+ `load_BR` – загрузить BR на левый вход ALU
+ `load_DR` – загрузить DR на правый вход ALU
+ `load_CR` – загрузить CR на правый вход ALU
+ `load_SP` – загрузить SP на правый вход ALU
+ `load_IP` – загрузить IP на правый вход ALU
+ `CR_addr_to_bus` – загрузить адрес команды на правый вход ALU
+ `invert_left` – инвертировать левый вход ALU
+ `invert_right` – инвертировать правый вход ALU
+ `sum` – сложить два входа ALU
+ `and` – побитовое И
+ `inc` – инкрементировать выход ALU
+ `set_NZ` – установить значения флагов
### Control unit

![cu.png](resources/cu.png)

#### Сигналы для управляющих микроинструкций
+ `CHCK_ADDR_TYPE` – проверка типа адресации
+ `JUMP` – безусловный переход в микрокоде
+ `JUMP_TO_CR_OPCODE` – Переход на выполнение инструкции
+ `JUMP_IF` – условный переход по микрокоду
+ `CHECK_Z` – условие перехода Z==1
+ `CHECK_N` – условие перехода N==1
+ `CHECK_nZ` – условие перехода Z==0
+ `CHECK_nN` – условие перехода N==0
+ `HLT` – остановка работы тактового генератора

Метод `start` эмулирует работу полного цикла машины.
#### Цикл обработки инструкции
+ Выборка инструкции
+ Выборка адреса
+ Выборка операнда
+ Выполнение инструкции
+ Пост-выполнение инструкции для инкремента IP

#### Принцип работы
+ Создание лога процессора
+ Микроинструкция загружается по адесу из mIP
+ Проверяется тип микроинструкции(управляющая или обычная)
+ Обработка сигналов, содержащихся в микроинструкции в следующем порядке:
    + Сигналы чтения из регистров
    + Сигнал чтения из памяти
    + Сигналы работы с ALU и флагами
    + Сигналы защелкивания регистров
    + Сигнал записи в память
+ Инкремент счетчика микрокоманд (mIP)
+ Возврат значения: нужно ли продолжать симуляцию

## Тестирование
+ Тестирование осуществляется при помощи golden test-ов.
+ Код golden тестирования находится в [файле](./golden_test.py)
+ Конфигурация golden test-ов находится в [директории](./golden)
+ Файлы с исходным кодом находятся в [директории](./examples)

Конфигурация CI через GitHub Actions:
```yaml
name: Stack-Machine

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          pip3 install poetry
          poetry install

      - name: Run tests and collect coverage
        run: |
          poetry run coverage run -m pytest .
          poetry run coverage report -m
        env:
          CI: true

  lint:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          pip3 install poetry
          poetry install

      - name: Check code formatting with Ruff
        run: poetry run ruff format --check .

      - name: Run Ruff linters
        run: poetry run ruff check .
 ```

## Кэш
+ Полностью ассоциативный
+ 4 кэш-линии
+ Политика вытеснения: случайная
+ Политика записи: write-through
![AddressDecoder.png](resources/AddressDecoder.png)
Показатели работы кэша на алгоритме `prob1`, сумма делителей от 1 до 999(доступ к памяти – 10 тактов, к кэшу – 1):

| Кол-во линий | Кол-во тактов |
|------------|---------------|
| 0          | 186198        |
| 3          | 185094        |
| 4          | 182333        |
| 5          | 180142        |
| 6          | 177351        |
| 7          | 174060        |
| 8          | 171079        |
| 9          | 168058        |
| 10         | 165087        |

Из-за случайной политики вынесения из кэша, 
количества тактов при одном и том же числе кэш-линий может незначительно меняться.

Основной цикл программы состоит из 29 инструкций.

## Пример использования
Рассмотрим программу сложения двух чисел:
```nasm
X: word 1
Y: word 2
RES: word 0
START:
    ld X
    add Y
    wr RES
```
После трансляции она будет выглядеть вот так:
```text
[1, 2, 0, {"name": "ld", "op_code": "LD", "addressing_type": "ABSOLUTE_STRAIGHT", "is_start": true, "address": 0}, {"name": "add", "op_code": "ADD", "addressing_type": "ABSOLUTE_STRAIGHT", "is_start": false, "address": 1}, {"name": "wr", "op_code": "WR", "addressing_type": "ABSOLUTE_STRAIGHT", "is_start": false, "address": 2}, {"name": "hlt", "op_code": "HLT", "addressing_type": "NO_ADDRESS", "is_start": false, "address": 0}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```
В начале во время работы транслятора произойдет замена меток и
помещение данных в ячейки.

Мы загружаем значение X из памяти, на что уходит время, и прибавляем к нему
значение Y, которое также надо достать из памяти. Результат сохраняем в RES, что также
требует время для записи в память.

Лог процессора:
```text
Tick #0:  mIP: 0; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #1:  mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #2: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #3: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #4: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #5: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #6: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #7: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #8: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #9: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #10: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #11: MEMORY ACCESS TICK mIP: 1; AC: 0; BR: 0; DR: 0; SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #12:  mIP: 2; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='nope', op_code=<OpCode.NOPE: 63>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #13:  mIP: 3; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #14:  mIP: 4; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 3; N: 0; Z: 0
Tick #15:  mIP: 5; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #16:  mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #17: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #18: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #19: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #20: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #21: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #22: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #23: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #24: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #25: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #26: MEMORY ACCESS TICK mIP: 18; AC: 0; BR: 0; DR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #27:  mIP: 19; AC: 0; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #28:  mIP: 24; AC: 0; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #29:  mIP: 25; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #30:  mIP: 69; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 3; AR: 0; N: 0; Z: 0
Tick #31:  mIP: 70; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 0; N: 0; Z: 0
Tick #32:  mIP: 0; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 0; N: 0; Z: 0
Tick #33:  mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #34: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #35: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #36: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #37: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #38: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #39: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #40: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #41: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #42: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #43: MEMORY ACCESS TICK mIP: 1; AC: 1; BR: 0; DR: 1; SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #44:  mIP: 2; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='ld', op_code=<OpCode.LD: 24>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=True, address=0); IP: 4; AR: 4; N: 0; Z: 0
Tick #45:  mIP: 3; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 4; N: 0; Z: 0
Tick #46:  mIP: 4; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 4; N: 0; Z: 0
Tick #47:  mIP: 5; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #48:  mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #49: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #50: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #51: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #52: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #53: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #54: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #55: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #56: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #57: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #58: MEMORY ACCESS TICK mIP: 18; AC: 1; BR: 0; DR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #59:  mIP: 19; AC: 1; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #60:  mIP: 20; AC: 1; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: 0; Z: 0
Tick #61:  mIP: 21; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: False; Z: False
Tick #62:  mIP: 69; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 4; AR: 1; N: False; Z: False
Tick #63:  mIP: 70; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 1; N: False; Z: False
Tick #64:  mIP: 0; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 1; N: False; Z: False
Tick #65:  mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #66: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #67: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #68: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #69: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #70: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #71: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #72: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #73: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #74: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #75: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 2; SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #76:  mIP: 2; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='add', op_code=<OpCode.ADD: 20>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=1); IP: 5; AR: 5; N: False; Z: False
Tick #77:  mIP: 3; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 5; N: False; Z: False
Tick #78:  mIP: 4; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 5; N: False; Z: False
Tick #79:  mIP: 5; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #80:  mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #81: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #82: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #83: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #84: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #85: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #86: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #87: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #88: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #89: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #90: MEMORY ACCESS TICK mIP: 18; AC: 3; BR: 0; DR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #91:  mIP: 19; AC: 3; BR: 0; DR: 0; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #92:  mIP: 26; AC: 3; BR: 0; DR: 0; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #93: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #94: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #95: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #96: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #97: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #98: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #99: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #100: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #101: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #102: MEMORY ACCESS TICK mIP: 26; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #103:  mIP: 27; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #104:  mIP: 69; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 5; AR: 2; N: False; Z: False
Tick #105:  mIP: 70; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 2; N: False; Z: False
Tick #106:  mIP: 0; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 2; N: False; Z: False
Tick #107:  mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #108: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #109: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #110: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #111: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #112: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #113: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #114: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #115: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #116: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #117: MEMORY ACCESS TICK mIP: 1; AC: 3; BR: 0; DR: 3; SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #118:  mIP: 2; AC: 3; BR: 0; DR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); SP: -3; CR: Command(name='wr', op_code=<OpCode.WR: 26>, addressing_type=<AddressingType.ABSOLUTE_STRAIGHT: 0>, is_start=False, address=2); IP: 6; AR: 6; N: False; Z: False
Tick #119:  mIP: 3; AC: 3; BR: 0; DR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); SP: -3; CR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 6; AR: 6; N: False; Z: False
Tick #120:  mIP: 19; AC: 3; BR: 0; DR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); SP: -3; CR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 6; AR: 6; N: False; Z: False
Tick #121:  mIP: 68; AC: 3; BR: 0; DR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); SP: -3; CR: Command(name='hlt', op_code=<OpCode.HLT: 68>, addressing_type=<AddressingType.NO_ADDRESS: 5>, is_start=False, address=0); IP: 6; AR: 6; N: False; Z: False
```
В итоге мы получаем в аккумуляторе значение 3.

## Статистика
Статистика с 6 линиями кэша, чтение из кэша - 1 такт, из памяти 10 - тактов.
```
| ФИО                         | алг   | LoC | такт.  | вариант                                                                                    |
| Мальков Павел Александрович | hello | 24  | 2651   | asm | acc | neum | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob1 | cache |
| Мальков Павел Александрович | cat   | 16  | 883    | asm | acc | neum | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob1 | cache |
| Мальков Павел Александрович | prob1 | 36  | 177351 | asm | acc | neum | mc -> hw | tick -> instr | struct | stream | mem | pstr | prob1 | cache |
```