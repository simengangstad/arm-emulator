# ARM assembler written in Python

## Specification

8 registers (Rn). 
The amount of words of RAM is specified in the settings file.

For every instruction issued a condition can be added. This condition has to be
fulfilled in order for the instruction to execute.

### Instructions

0. HLT <CONDITION>                           - Halts the program
1. ADD <CONDITION> Arg1, Arg2, Arg3          - Adds the value of Arg3 and Arg2 and stores it in Arg1
2. SUB <CONDITION> Arg1, Arg2, Arg3          - Subtracts the value of Arg3 from Arg2 and stores it in Arg1
3. MOV <CONDITION> Arg1, Arg2                - Moves the value of Arg2 to Arg1
4. CMP <CONDITION> Arg1, Arg2                - Compares Arg2 to Arg1
5. BRA <CONDITION> Arg1                      - Sets the program counter to Arg1
6. LDR <CONDITION> Arg1, [Arg2]              - Load the value at the memory address Arg2 into Arg1
7. STR <CONDITION> Arg1, [Arg2]              - Store the value of Arg1 into the memory address Arg2
8. OUT <CONDITION> Arg1                      - Outputs values (0 = memory).

### Conditions

1. EQ - Equal
2. NE - Not equal
3. GE - Greater or equal
4. GT - Greater than
5. LE - Less or equal
6. LT - Less than

### Labels

Labels are defined by : and the label name. An example would be :end for the label "end". This
is a reference to the line after the label.

### Memory

[address] refers to the value at the given memory address.

### Comments

Comments are specified with a number sign, '#', at the start of the line.



## The settings file
 
The settings file defines behaviours of the assembler.

* debug - If logging should be enabled (error messages is shown either way)
* displayLabels - If the labels should be displayed every fetch cycle
* displayMemory - If the memory should be displayed every execution cycle
* waitAfterExecution - If the assembler should wait after each execution cycle
* amountOfWords - Specifies the amount of words for memory
