import tkinter

# TODO:
# Memory in a file (?)

# Log output
output = "";

def log(message):

    global output

    print(message);

    output += message + "\n";

# Specification
#
# In every instruction except the HLT instruction a condition can be added. This condition has to be
# fulfilled in order for the instruction to execute.
#
# 0 - HLT                                       - Halts the program
# 1 - ADD <CONDITION> Arg1, Arg2, Arg3          - Adds the value of Arg3 and Arg2 and stores it in Arg1
# 2 - SUB <CONDITION> Arg1, Arg2, Arg3          - Subtracts the value of Arg3 from Arg2 and stores it in Arg1
# 3 - MOV <CONDITION> Arg1, Arg2                - Moves the value of Arg2 to Arg1
# 4 - CMP <CONDITION> Arg1, Arg2                - Compares Arg2 to Arg1
# 5 - BRA <CONDITION> Arg1                      - Sets the program counter to Arg1
#
#
# Labels
#
# Labels are defined by : and the label name. An example would be :end for the label end. This
# points to the line after the label.

Specification = [

    "HLT",
    "MOV",
    "ADD",
    "SUB",
    "CMP",
    "B"
];

Conditions = [

    "EQ",
    "NE",
    "GE",
    "GT",
    "LE",
    "LT"
];

# Registers and statuses
Registers = [

    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7"
];

AmountOfRegisters = 7;

registers = [0 for i in range(7)];
pc = 0;
cir = "";
statusNegative = False;
statusZero = False;



# Helper functions

def printStatusOfAssembler():

    log("PC:" + str(pc));
    log("CIR:" + cir);

    log("\nStatus negative:" + str(statusNegative));
    log("Status zero:" + str(statusZero));
    log("Status:" + str(status) + "\n");

    for i in range(len(registers)):

        log(Registers[i] + ": " + str(registers[i]));

def isValidRegister(register):

    return register in Registers;

def isValidLabel(label):

    return label in labels;

def isValidValue(value):

    #if (value[0] != "#"):

     #   printError("Argument is not an immediate value", pc - 1);

    try:

        int(value[1:]);

        return True;

    except ValueError:

        return False;

def validateArgumentsLength(arguments, length):

    if (len(arguments) != length):

        printError(("Invalid amount of arguments."), pc - 1);

def retrieveValue(argument):

    value = None;

    if (isValidRegister(argument)):

        value = registers[Registers.index(argument)];

    elif (isValidLabel(argument)):

        value = int(labels[argument]);

    elif (isValidValue(argument)):

        value = int(argument[1:]);

    return value;


def printError(message, pc):

    log("Error at PC: " + str(pc) + " - " + message);

    status = False;

# ---------- START OF MAIN PROGRAM -------------

# Reading program from file input

settingsFile = None;

try:

    settingsFile = open("settings.txt", "r");

except FileNotFoundError:

    log("Settings file not found, creating new...\n");

    settingsFile = open("settings.txt", "w+");

    settingsFile.write("displayLabels=true");

    settingsFile.seek(0);


settingsList = settingsFile.read().split("\n");

settings = {};

for line in settingsList:

    setting = line.split("=")[0];
    value = line.split("=")[1];

    settings[setting] = value;

settingsFile.close();

displayLabels = "displayLabels" in settings and settings["displayLabels"] == "true";

file = None;

fileNotFound = True;

while (fileNotFound):

    try:

        file = open(input("File to assemble and run: "), "r");

        fileNotFound = False;

    except FileNotFoundError:

        log("File not found, try again...");


log("Fetching code from file...\n")
program = file.read().split("\n");

file.close();


# Decoding the input

labels = {};

for index in range(len(program)):

    line = program[index].strip().upper();

    if (line.startswith(":")):

        label = line[1:].strip();

        # Check if label is on the same line as the instruction
        try:

            label = label[:label.index(" ")];

        except ValueError:

            # Lol
            label = label;

        labels[label] = index;

    program[index] = line;

for index in range(len(program)):

    line = program[index];

    log(str(index) + ". " + line);

log("\n\n");



# Interpreting and executing

# The interpreter has to grab each line and trim it the left side of it before
# checking for valid instruction. When it has got that instruction it removes
# that part of the copy of the line and trims, removes spaces and splits up
# the rest of the copy of the line.

#window = tkinter.Tk();

status = True;
cycle = 1;

while (status):

    # DISPLAY LABELS

    if (displayLabels):

        log("----- LABELS -----");

        for label in labels:

            log(str(labels[label]) + ": " + label);

        log("\n");


    # FETCH

    # Fetch line and trim string
    if (pc < 0 or len(program) <= pc):

        printError("PC is out of boundry for memory", pc);

        break;

    cir = program[pc];

    if (cir.startswith(":")):

        label = cir[1:].strip();

        if (" " in label):

            label = label[:label.index(" ")].strip();


        cirCopy = cir.replace(":", "").strip().replace(label, "").strip();

        if (0 < len(cirCopy)):

            cir = cirCopy;

        else:

            log("----- FETCH (Cycle " + str(cycle) + ") -----");
            printStatusOfAssembler();

            cycle += 1;
            pc += 1;

            continue;


    # Check if the inputted instruction is in the specification
    instruction = None;

    for Instruction in Specification:

        if (cir[:len(Instruction)] == Instruction):

            instruction = Instruction;

            break;

    if (instruction == None):

        printError(("Instruction is not a valid instruction."), pc);

        status = False;

        break;

    # Check if there is a condition given and if it is in the specification

    condition = cir[len(instruction):][:2];
    hasCondition = condition in Conditions;
    arguments = None;

    log("----- FETCH (Cycle " + str(cycle) + ") -----");
    printStatusOfAssembler();

    cycle += 1;
    pc += 1;

    if (hasCondition):

        arguments = cir[len(instruction):][2:].strip().replace(" ", "").split(",");

        if (condition == "EQ" and not statusZero):

            continue;

        elif (condition == "NE" and statusZero):

            continue;

        elif (condition == "GE" and (not statusZero and statusNegative)):

            continue;

        elif (condition == "GT" and statusNegative):

            continue;

        elif (condition == "LE" and (not statusZero and not statusNegative)):

            continue;

        elif (condition == "LT" and not statusNegative):

            continue;

    else:

        arguments = cir[len(instruction):].replace(" ", "").split(",");

    # EXECUTE

    if (instruction == "MOV"):

        validateArgumentsLength(arguments, 2);

        if (isValidRegister(arguments[0])):

            value = retrieveValue(arguments[1]);

            if (value == None):

                printError("Not valid argument for instruction", pc - 1)

                break;

            else:

                registers[Registers.index(arguments[0])] = value;

        else:

            printError("Not valid arguments for instruction.", pc - 1);

    elif (instruction == "ADD"):

        validateArgumentsLength(arguments, 3);

        if (isValidRegister(arguments[0])):

            value1 = retrieveValue(arguments[1]);
            value2 = retrieveValue(arguments[2]);

            if (value1 == None or value2 == None):

                printError("Not valid argument for instruction", pc - 1)

                break;

            else:

                registers[Registers.index(arguments[0])] = value1 + value2;

        else:

            printError("Not valid arguments for instruction.", pc - 1);

            break;

    elif (instruction == "SUB"):

        validateArgumentsLength(arguments, 3);

        if (isValidRegister(arguments[0])):

            value1 = retrieveValue(arguments[1]);
            value2 = retrieveValue(arguments[2]);

            if (value1 == None or value2 == None):

                printError("Not valid argument for instruction", pc - 1);

                break;

            else:

                registers[Registers.index(arguments[0])] = value1 - value2;

        else:

            printError("Not valid arguments for instruction.", pc - 1);

            break;

    elif (instruction == "CMP"):

        validateArgumentsLength(arguments, 2);

        value1 = retrieveValue(arguments[0]);
        value2 = retrieveValue(arguments[1]);

        if (value1 == None or value2 == None):

            printError("Not valid argument for instruction", pc - 1);

            break;

        else:

            statusNegative = value2 < value1;
            statusZero = value1 == value2;

    elif (instruction == "B"):

        validateArgumentsLength(arguments, 1);

        value = retrieveValue(arguments[0]);

        if (value == None):

            printError("Not valid argument for instruction", pc - 1);

            break;

        else:

            pc = value;

    elif (instruction == "HLT"):

        status = False;


    log("\n----- EXECUTE (Cycle " + str(cycle) + ") -----");
    printStatusOfAssembler();

    cycle += 1;

    input();

print(output);
