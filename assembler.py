#Assembler code


#defining dictionaries
instruction_seta = {"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
instruction_setb = {"mov":"00010","rs":"01000","ls":"01001"}
instruction_setc = {"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
instruction_setd = {"ld":"00100","st":"00101"}
instruction_sete = {"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
instruction_setf = {"hlt":"11010"}
registers = {"R0":["000",0],"R1":["001",0],"R2":["010",0],"R3":["011",0],"R4":["100",0],"R5":["101",0],"R5":["110",0],"R6":["111",0],"FLAG":["111"]}
labels = {}
variables = {}
FLAG_data = []
error = []

#defining variables
immediate_value = ""
variable_error = False
overflow = False
write_data = []
variable_counter = 0
instruction_start = False
end = False
overflow = False
instruction_type = ""
not_defined = False
syntax_error = False
hlt_error = False
FLAG_error = False
label_counter = 0
label_need = []
label_naming_counter = 0
label_error = False
label_run = False
label_declaration = False

#decimal to binary conversion with seven digits
def decimaltobinary(ip_val):
    global immediate_value
    immediate_value = ""
    if ip_val >= 1:
        decimaltobinary(ip_val // 2)
        immediate_value += str(ip_val % 2)
    return (immediate_value)


#7 bit memory and immediate variables
def seven_bit(binary):
    global immediate_value
    global overflow
    global end
    if len(binary)>7:
        overflow = True
        error.append(["overflow",x])
        print("MORE THAN 7 BITS")
    else:
        binary = "0"*(7 - len(binary))+binary
        return binary

#assembler main program

def assembler(instruction):
    
    #defining variables
    global variable_counter
    global instruction_start
    global variable_error
    global overflow
    global instruction_type
    global end
    global not_defined
    global syntax_error
    global hlt_error
    global FLAG_error
    global label_counter
    global labels
    global x
    global label_run
    global label_need
    global label_naming_counter
    global label_error
    global labeled
    global error
    machine_code = ""
    instruction = instruction.split(" ")
    length = len(instruction)
    variable_declaration = False
    label_declaration = False
    
    #detecting the type of instruction
    if not label_run:
        if instruction == [""]:
            return 0
        elif instruction[0] in instruction_seta:
            if length == 4:
                instruction_start = True
                unused_bits = 2
                machine_code += instruction_seta[instruction[0]] + "_"
                machine_code += "0"*unused_bits + "_"
                instruction_type = "a"
        
        elif instruction[0] in instruction_setb and instruction[length-1][0] == "$":
            if length == 3:
                instruction_start = True
                unused_bits = 1
                machine_code += instruction_setb[instruction[0]] + "_"
                machine_code += "0"*unused_bits + "_"
                instruction_type = "b"
        
        elif instruction[0] in instruction_setc:
            if length == 3:
                instruction_start = True
                unused_bits = 5
                machine_code += instruction_setc[instruction[0]] + "_"
                machine_code += "0"*unused_bits + "_"
                instruction_type = "c"
        
        elif instruction[0] in instruction_setd:
            if length == 3:
                instruction_start = True
                unused_bits = 1
                machine_code += instruction_setd[instruction[0]] + "_"
                machine_code += "0"*unused_bits + "_"
                instruction_type = "d"
        
        elif instruction[0] in instruction_sete:
            if length == 2:
                instruction_start = True
                unused_bits = 4
                machine_code += instruction_sete[instruction[0]] + "_"
                machine_code += "0"*unused_bits + "_"
                instruction_type = "e"
                label_need.append(seven_bit(decimaltobinary(x)))
        
        elif instruction[0] in instruction_setf:
            if length == 1:
                instruction_start = True
                unused_bits = 11
                machine_code += instruction_setf[instruction[0]] + "_"
                machine_code += "0"*unused_bits
                instruction_type = "f"
                end = True
        
        #variable declation
        elif instruction[0].lower() == "var" and not label_run:
            if instruction_start:
                variable_error = True
                print("VARIABLE NOT DEEFINED AT THE START OF THE CODE")
            else:
                variable_counter += 1
                variables[instruction[1]] = seven_bit(decimaltobinary(variable_counter))
                variable_declaration = True
        #label defining
        elif instruction[0][-1:] == ":" :
            label_counter += 1
            labels[instruction[0][:-1]] = seven_bit(decimaltobinary(x))
            labeled = True
            assembler("".join(instruction[1:]))
            label_declaration = True
            
        else:
            error.append(["SYNTAX ERROR",x])
            print("SYNTAX ERROR")
            syntax_error = True

    