#Assembler code


#defining dictionaries
instruction_seta = {"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100","addf":"10000" , "subf":"10001"}
instruction_setb = {"mov":"00010","rs":"01000","ls":"01001"}
instruction_setc = {"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
instruction_setd = {"ld":"00100","st":"00101"}
instruction_sete = {"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
instruction_setf = {"hlt":"11010"}
instruction_setg = {"movf":"10010"}
registers = {"R0":["000",0],"R1":["001",0],"R2":["010",0],"R3":["011",0],"R4":["100",0],"R5":["101",0],"R6":["110",0],"R7":["111",0],"FLAGS":["111"]}
labels = {}
variables = {"FLAGS":"111"}
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
variable_need = []
variable_naming_counter = 0
label_counter = 0
label_need = []
label_naming_counter = 0
label_error = False
label_run = False
label_declaration = False
total_lines = 0

def dectoieee(number):
    global x
    global error
    l = number.split(".")
    l1 = "0." + l[1]
    decimal = float(l1)
    str1 = ""
    while decimal != 0:
        decimal*=2
        if decimal >= 1:
            decimal -= 1
            str1+='1'
        else:
            str1+='0'
    #makes the int part binary
    st1 = str(bin(int(l[0])))
    binary_of_int = st1.split("0b")[1]

    #exponent in binary and fixes it to 3 bits
    exponent_in_decimal = len(binary_of_int) + 2
    if exponent_in_decimal <=7:
        exponent_in_binary = str(bin(exponent_in_decimal)).split("0b")[1]
        if len(exponent_in_binary) <3:
            spacestr = "0"*(3-len(exponent_in_binary))
            finalexp = spacestr+exponent_in_binary
        else:
            finalexp = exponent_in_binary
    else:
        #error message if len exponent > 3 bits
        error.append(["overflow",x])
    
    #mantissa calculation
    if len(binary_of_int[1:]) == 5:
        finalmantissa = binary_of_int[1:]
    elif len(binary_of_int) < 5:
        finalmantissa = binary_of_int[1:] + str1[0:(5-len(binary_of_int[1:]))]
    return(finalexp + finalmantissa)


def bintodec(n):
    intdeclist = n.split(".")
    rev = intdeclist[0][::-1]
    sum = 0
    for i in range(0,len(intdeclist[0])):
        sum += (2**i)*int(rev[i])
    for j in range(-1, -(len(intdeclist[1])+1),-1):
        sum += int(intdeclist[1][((-j)-1)])*2**(j)
    return str(sum)


def ieeetodec(binst):
    expbin = binst[0:3]
    exbiasdec = int(expbin[0])*(2**2) + int(expbin[1])*(2**1) + int(expbin[2])*(2**0)
    exp = exbiasdec - 3
    mantissa = binst[3:]
    mantissa = "1"+mantissa
    numberbin = mantissa[0:(exp+1)] +"." + mantissa[(exp+1):]
    answer = bintodec(numberbin)
    return float(answer)



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
        return binary
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
    global variable_need
    global variable_naming_counter
    machine_code = ""
    instruction = " ".join(instruction.split("\t"))
    instruction = instruction.split(" ")
    length = len(instruction)
    variable_declaration = False
    label_declaration = False
    
    #detecting the type of instruction
    if not label_run:
        if instruction == [""]:
            return 0
        elif end:
            error.append(["Can't Execute code after hlt",x-1])
        elif instruction[0] in instruction_seta:
            if length == 4:
                instruction_start = True
                unused_bits = 2
                machine_code += instruction_seta[instruction[0]] 
                machine_code += "0"*unused_bits
                instruction_type = "a"
        
        elif instruction[0] in instruction_setb and instruction[length-1][0] == "$":
            if length == 3:
                instruction_start = True
                unused_bits = 1
                machine_code += instruction_setb[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "b"
        
        elif instruction[0] in instruction_setc:
            if length == 3:
                instruction_start = True
                unused_bits = 5
                machine_code += instruction_setc[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "c"
        
        elif instruction[0] in instruction_setd:
            if length == 3:
                instruction_start = True
                unused_bits = 1
                machine_code += instruction_setd[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "d"
        
        elif instruction[0] in instruction_sete:
            if length == 2:
                instruction_start = True
                unused_bits = 4
                machine_code += instruction_sete[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "e"
                label_need.append(seven_bit(decimaltobinary(x)))
        
        elif instruction[0] in instruction_setf:
            if length == 1:
                instruction_start = True
                unused_bits = 11
                machine_code += instruction_setf[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "f"
                end = True
        elif instruction[0] in instruction_setg:
            if length == 3:
                instruction_start = True
                unused_bits = 0
                machine_code += instruction_setg[instruction[0]]
                machine_code += "0"*unused_bits
                instruction_type = "g"

        
        #variable declation
        elif instruction[0].lower() == "var" and not label_run:
            if instruction_start:
                variable_error = True
            else:
                variables[instruction[1]] = seven_bit(decimaltobinary(total_lines + variable_counter))
                variable_counter += 1
                variable_declaration = True
        #label defining
        elif instruction[0][-1:] == ":" :
            label_counter += 1
            labels[instruction[0][:-1]] = seven_bit(decimaltobinary(x))
            labeled = True
            assembler((" ".join(instruction[1:])).strip())
            label_declaration = True
            
        else:
            error.append(["SYNTAX ERROR",x])
            syntax_error = True
    #converting registers and memory addreses to machine code
    if not syntax_error and instruction_start and instruction_type != "e" and not label_run and not label_declaration :
        for i in range(1,length):
            if instruction[i] == "FLAG":
                if instruction_type == "c":
                    if instruction[0] == "mov":
                        machine_code += registers[instruction[i]]
                    else:
                        error.append(["FLAG CAN'T BE USED THER",x])
                        FLAG_error = True 
                else:
                    error.append(["FLAG CAN'T BE USED THER",x])
                    FLAG_error = True 

            elif instruction[i][0] == "$":
                if "." in instruction[i][1:]:
                    machine_code += dectoieee(str(instruction[1][1:]))
                else:
                    decimaltobinary(int(instruction[i][1:]))
                    if len(seven_bit(immediate_value)) == 7:
                        machine_code += seven_bit(immediate_value)
            
            elif instruction[i] in variables:
                machine_code += variables[instruction[i]]
            

            elif instruction[i][0] == "R":
                if instruction[i] in registers:
                    machine_code += registers[instruction[i]][0]
                else:
                    error.append(["REGISTER NOT IN RANGE",x])
                    not_defined = True

            elif instruction[i] not in variables and instruction[i] not in registers:
                error.append(["VARIABLE NOT DEFINED",x])
                not_defined = True

    #storing machine code to write in the file
    if not variable_declaration and not label_run and not label_declaration:
        write_data.append([seven_bit(decimaltobinary(x)),machine_code])
        x += 1
    
    #label handeling
    if label_run:
        if instruction[0] in instruction_sete:
            if write_data[x][0] == label_need[label_naming_counter] :
                if instruction[1] in labels:
                    try:
                        write_data[x][1] += labels[instruction[1]]
                    except Exception as e:
                        label_error = True
                        error.append(["invalid lable stated",x])
                else:
                    label_error = True
                    error.append(["invalid lable stated",x])
            label_naming_counter += 1
            x += 1
        else:
            if instruction[0] != "var":
                x += 1

#reading the instructions
data = []
testline = " "
while True:
    if testline != "":
        testline = input()
        if testline != "":
            data.append(testline)
    else:
        break
x = 0

for code in data:
    if len(error) == 0:
        assembler(code.strip())


error = []
total_lines = x
variables = {"FLAGS":"111"}
FLAG_data = []
write_data = []
end = False
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
variable_need = []
variable_naming_counter = 0
label_counter = 0
label_need = []
label_naming_counter = 0
label_error = False
label_run = False
label_declaration = False
instruction_start = False

x = 0
for code in data:
    if len(error) == 0:
        assembler(code.strip())


label_run = True
x = 0
if len(error) == 0:
    for code in data:
        assembler(code.strip())


#checking halt instruction is given
try:
    if write_data[len(write_data)-1][1] != "1101000000000000" and len(error) == 0:
            error.append(["HALT INSTRUCTION NOT GIVEN",x])
            hlt_error = True
except Exception as e:
    pass

#writing the machine code in a file
if len(error) == 0:
    for lines in write_data:
        print(f"{lines[1]}")
else:
    print(f"{error[0][0]} at line {error[0][1]+1+variable_counter}")

