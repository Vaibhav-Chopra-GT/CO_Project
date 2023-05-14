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
