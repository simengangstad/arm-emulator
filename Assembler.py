# Log output
output = "";

def log(message):
    
    logWithOptionOfBreaking(message, True);

def logWithOptionOfBreaking(message, breakLine):

    global output

    if (breakLine):

        if (debug):

            print(message);

        output += message + "\n";

    else:

        if (debug):

            print(message, end="");

        output += message;

def logForced(message):

    logForcedWithOptionOfBreaking(message, True);


def logForcedWithOptionOfBreaking(message, breakLine):

    global output

    if (breakLine):

        print(message);

        output += message + "\n";

    else:

        print(message, end="");

        output += message;

Specification = [

    "HLT",
    "MOV",
    "ADD",
    "SUB",
    "CMP",
    "B",
    "LDR",
    "STR",
    "OUT"
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


# Memory

AmountOfMemoryLocations = 32;
memory = [0]*AmountOfMemoryLocations;


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

def isValidMemoryAddress(value):

    if (value.startswith("[") and value.endswith("]")):

        address = value[1:-1];

        return isValidRegister(address);

    return False;

def setMemoryLocation(location, value):

    if (0 <= location and location <= AmountOfMemoryLocations):

        memory[location] = value;

        return True;

    else:

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

    logForced("Error at PC: " + str(pc) + " - " + message);

    status = False;

    logForced("CPU crashed!");

# ---------- START OF MAIN PROGRAM -------------

# Reading program from file input

settingsFile = None;
debug = True;

try:

    settingsFile = open("settings.txt", "r");

except FileNotFoundError:

    log("Settings file not found, creating new...\n");

    settingsFile = open("settings.txt", "w+");

    settingsFile.write("debug=true\n");
    settingsFile.write("displayLabels=true\n");
    settingsFile.write("displayMemory=true\n");
    settingsFile.write("waitAfterExecution=true");

    settingsFile.seek(0);


settingsList = settingsFile.read().split("\n");

settings = {};

for line in settingsList:

    if (line == ""):

        continue;

    setting = line.split("=")[0];
    value = line.split("=")[1];

    settings[setting] = value;

settingsFile.close();

debug = "debug" in settings and settings["debug"] == "true";
displayLabels = "displayLabels" in settings and settings["displayLabels"] == "true";
displayMemory = "displayMemory" in settings and settings["displayMemory"] == "true";
waitAfterExecution = "waitAfterExecution" in settings and settings["waitAfterExecution"] == "true";

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

status = True;
cycle = 1;

while (status):

    # DISPLAY LABELS

    if (program[pc].strip() == "" or program[pc].startswith("#")):

        pc += 1;

        continue;

    log("\n\n")

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

        value = retrieveValue(arguments[1]);

        if (value == None):

            printError("Not valid argument for instruction", pc - 1)

            break;

        else:

            if (isValidRegister(arguments[0])):

                registers[Registers.index(arguments[0])] = value;

            else:

                printError("Not valid arguments for instruction.", pc - 1);

                break;

    elif (instruction == "ADD"):

        validateArgumentsLength(arguments, 3);

        value1 = retrieveValue(arguments[1]);
        value2 = retrieveValue(arguments[2]);

        if (value1 == None or value2 == None):

            printError("Not valid argument for instruction", pc - 1)

            break;

        else:

            if (isValidRegister(arguments[0])):

                registers[Registers.index(arguments[0])] = value1 + value2;

            else:

                printError("Not valid arguments for instruction.", pc - 1);

                break;

    elif (instruction == "SUB"):

        validateArgumentsLength(arguments, 3);

        value1 = retrieveValue(arguments[1]);
        value2 = retrieveValue(arguments[2]);

        if (value1 == None or value2 == None):

            printError("Not valid argument for instruction", pc - 1)

            break;

        else:

            if (isValidRegister(arguments[0])):

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

    elif (instruction == "LDR"):

        validateArgumentsLength(arguments, 2);

        if (isValidRegister(arguments[0]) and isValidMemoryAddress(arguments[1])):

            registers[Registers.index(arguments[0])] = memory[registers[Registers.index(arguments[1][1:-1])]];

        else:

            printError("Not valid argument for instruction", pc - 1);

            break;

    elif (instruction == "STR"):

        validateArgumentsLength(arguments, 2);

        if (isValidRegister(arguments[0]) and isValidMemoryAddress(arguments[1])):

            if (not setMemoryLocation(registers[Registers.index(arguments[1][1:-1])], registers[Registers.index(arguments[0])])):

                printError("Not a valid memory address, has to be between 0 and " + AmountOfMemoryLocations + ".");

                break;

        else:

            printError("Not valid argument for instruction", pc - 1);

            break;

    elif (instruction == "HLT"):

        status = False;

    elif (instruction == "OUT"):

        validateArgumentsLength(arguments, 1);

        try:

            value = int(arguments[0]);

            if (value == 0):

                logForced("\n----- MEMORY ------");

                for y in range(0, int(AmountOfMemoryLocations / 4), 1):

                    for x in range(y, y + int(AmountOfMemoryLocations), int(AmountOfMemoryLocations / 4)):

                        logForcedWithOptionOfBreaking(str(x) + ":" + str(memory[x]) + "\t", False);

                    logForced("\n")
                
        except ValueError:

            printError("Invalid argument, not an integer type.");
        

    log("\n----- EXECUTE (Cycle " + str(cycle) + ") -----");
    printStatusOfAssembler();

    cycle += 1;

    if (displayMemory):

        log("\n----- MEMORY ------");

        for y in range(0, int(AmountOfMemoryLocations / 4), 1):

            for x in range(y, y + int(AmountOfMemoryLocations), int(AmountOfMemoryLocations / 4)):

                logWithOptionOfBreaking(str(x) + ":" + str(memory[x]) + "\t", False);

            log("\n")

    if (waitAfterExecution):

        input();

