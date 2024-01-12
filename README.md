# CO Project
This is the github repository of our Computer Organisation project.

## input.txt
This file contains the input code.

## machine_code.txt
This file contains the output code.

## assembler.py
This is the main program and it contains the code for the assembler.

Sections of code explained :-

**Defining Variables**: This section defines various variables used in the assembler. These variables keep track of the state of the assembler, such as the current instruction type, error flags, counters, and flags for different conditions. 

We define dictionaries to store the mappings between instructions and their binary representations.

**Decimal to Binary Conversion**: The decimaltobinary function converts decimal values to binary with seven digits. It uses recursion.

**Seven-bit Memory and Immediate Variables**: The seven_bit function is for checking if the binary representation exceeds seven bits. An overflow error is flagged in case it does.

**Assembler main**: The assembler function is the main part of the program. It takes an instruction as input and processes it to generate the corresponding machine code.

**Detecting the type of an instruction**: This checks the first word and the length of the instruction to determine the instruction type.It sets the appropriate variables and flags to handle the instruction later.

**Reading var declaration in assembly**: defines variable declaration in assembly code by looking for "var" in the beginning of the string.The variables dictionary is updated accordingly.

**Label definition**: label defining works by looking for ":" at the end of instruction. The labels dictionary is updated with the label's binary representation.

**Converting Registers and Memory Addresses to Machine Code**: This section converts register names and memory addresses to corresponding binary representations. It also handles the FLAGS register and immediate values.

**Storing Machine Code to Write in the File**: The machine code is stored in write_data(a list), which is later used to write the machine code into the output file.

**Label handling**: This is done by giving each line a seven bit binary address counting up. The binary representation of the label is appended to the machine code of the instruction that requires the label.

Variable address is a 7 bit number counting up for each variable.

**Label Run**: After processing all instructions once, the label_run flag is set to true to indicate that the instructions are to be processed again taking labels into account.

**Checking Halt Instruction**: For checking if the assembly code ends with 'halt'. If not, an error is flagged.

**Writing the Machine Code to a File**: If no errors were encountered during the assembly process, the machine code is written to the output file. Otherwise, the first error encountered is written to the file.

Team Members : Vaibhav Chopra - 2022552, Tarush Garg - 2022537, Tejus Madan - 2022540, Paarth Goyal - 2022343
