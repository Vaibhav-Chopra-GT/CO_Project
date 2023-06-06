instructions = []
simulator_registers = {"000" : 0 , "001" : 0 , "010" : 0 , "011" : 0 , "100" : 0 , "101" : 0 , "110" : 0}
simulator_variables = {}
Flag = [0,0,0,0]
line = ""
line_number = 0
hlt_achieved = False
testline = " "
program_counter = 0
jump = False
jump_hit = False
counter = ""

def btod(binstr):
    l = []
    for i in binstr:
        l.append(i)
    n = len(l) - 1
    sum = 0 
    for i in range(len(l)):
        sum += int(l[i])*(2**n)
        n = n-1
    return(sum)

def dtob(num):
    binary_str = format(int(num), 'b')
    bstr = str(binary_str)
    return(bstr)

def padding(bits,bstr):
    l = []
    for i in bstr:
        l.append(i)
    l.reverse()
    for j in range(bits-len(l)):
        l.append('0')
    l.reverse()
    jl = ''.join(l)
    return(jl)


while True:
    try:
        testline = input()
        instructions.append([padding(7,dtob(line_number)),testline])
        line_number += 1
    except EOFError:
        break
def instruction_given(line):
    return(line[:5])

def data_given(line):
    if line[-2:] == "\r":
        return line[5:-2]
    else:
        return line[5:]


def addition(line):
    global simulator_registers
    global Flag
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    if reg2[-2:] == "\r":
        reg2 = reg2[:-2]
    if simulator_registers[reg2] + simulator_registers[reg3] <= 65535:
        simulator_registers[reg1] = simulator_registers[reg2] + simulator_registers[reg3]
        Flag = [0,0,0,0]
    else:
        Flag = [0,0,0,0]
        Flag[0] = 1
        simulator_registers[reg1] = 0

def subtraction(line):
    global simulator_registers
    global Flag
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    if simulator_registers[reg3] <= simulator_registers[reg2]:
        simulator_registers[reg1] = simulator_registers[reg2] - simulator_registers[reg3]
        Flag = [0,0,0,0]
    else:
        Flag = [0,0,0,0]
        Flag[0] = 1
        simulator_registers[reg1] = 0

def multiply(line):
    global simulator_registers
    global Flag
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    if simulator_registers[reg2] * simulator_registers[reg3] <= 65535:
        simulator_registers[reg1] = simulator_registers[reg2] - simulator_registers[reg3]
        Flag = [0,0,0,0]
    else:
        Flag = [0,0,0,0]
        Flag[0] = 1
        simulator_registers[reg1] = 0

def XOR(line):
    global Flag
    global simulator_registers
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    simulator_registers[reg1] = simulator_registers[reg2] ^ simulator_registers[reg3]
    Flag = [0,0,0,0]

def OR(line):
    global Flag
    global simulator_registers
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    simulator_registers[reg1] = simulator_registers[reg2] | simulator_registers[reg3]
    Flag = [0,0,0,0]

def AND(line):
    global Flag
    global simulator_registers
    line = line[2:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    reg2 = line[3:6].replace('\r', '')
    reg3 = line[6:].replace('\r', '')
    if reg3[-2:] == "\r":
        reg3 = reg3[:-2]
    simulator_registers[reg1] = simulator_registers[reg2] & simulator_registers[reg3]
    Flag = [0,0,0,0]

def load(line):
    global simulator_variables
    global simulator_registers
    global Flag
    line = line[1:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    mem = line[3:].replace('\r', '')
    if mem[-2:] == "\r":
        mem = mem[:-2]
    if mem not in simulator_variables:
        simulator_variables[mem] = 0
    simulator_registers[reg1] = simulator_variables[mem]
    Flag = [0,0,0,0]

def store(line):
    global simulator_registers
    global simulator_variables
    global Flag
    line = line[1:].replace('\r', '')
    reg1 = line[:3].replace('\r', '')
    mem = line[3:].replace('\r', '')
    if mem[-2:] == "\r":
        mem = mem[:-2]
    if mem not in simulator_variables:
        simulator_variables[mem] = 0
    simulator_variables[mem] = simulator_registers[reg1]
    Flag = [0,0,0,0]

def unconditional_jump(line):
    global Flag
    global jump
    global program_counter
    global jump_hit
    jump_hit = True
    label = line[4:].replace('\r', '')
    if label[-2:] == "\r":
        label = label[:-2]
    l = 0
    z = ""
    Flag = [0,0,0,0]
    if hlt_achieved:
        return 0
    program_counter = int(btod(counter))
    print(f"{padding(7,dtob(program_counter))}        ",end="")
    for i in simulator_registers.values():
        print(padding(16,dtob(i)),end=" ")
    for i in Flag:
        z += str(i)
    print("0"*12 + z)
    for data in instructions:
        if label in data:
            for i in range(l,len(instructions)):
                simulator(instructions[i])
                return 0
            break
        l += 1
    Flag = [0,0,0,0]



def jump_less(line):
    global Flag
    global jump
    global program_counter
    global jump_hit
    label = line[4:].replace('\r', '')
    if label[-2:] == "\r":
        label = label[:-2]
    l = 0
    z = ""
    if hlt_achieved:
        return 0
    
    if Flag[1] == 1:
        jump_hit = True
        jump = True
        program_counter = int(btod(counter))
        program_counter += 1
        Flag = [0,0,0,0]
        print(f"{padding(7,dtob(program_counter))}        ",end="")
        for i in simulator_registers.values():
            print(padding(16,dtob(i)),end=" ")
        for i in Flag:
            z += str(i)
        print("0"*12 + z)
        for data in instructions:
            if label in data:
                for i in range(l,len(instructions)):
                    simulator(instructions[i])
                    return 0
                break
            l += 1
    Flag = [0,0,0,0]


def jump_greater(line):
    global Flag
    global jump
    global program_counter
    global jump_hit
    label = line[4:].replace('\r', '')
    if label[-2:] == "\r":
        label = label[:-2]
    l = 0
    z = ""
    if hlt_achieved:
        return 0
    
    if Flag[2] == 1:
        program_counter = int(btod(counter))
        jump_hit =True
        jump = True
        Flag = [0,0,0,0]
        print(f"{padding(7,dtob(program_counter))}        ",end="")
        for i in simulator_registers.values():
            print(padding(16,dtob(i)),end=" ")
        for i in Flag:
            z += str(i)
        print("0"*12 + z)
        for data in instructions:
            if label in data:
                for i in range(l,len(instructions)):
                    simulator(instructions[i])
                break
            l += 1
    Flag = [0,0,0,0]


def jump_equal(line):
    global Flag
    global jump
    global program_counter
    global jump_hit
    label = line[4:].replace('\r', '')
    if label[-2:] == "\r":
        label = label[:-2]
    l = 0
    z = ""
    if hlt_achieved:
        return 0
    
    if Flag[0] == 1:
        jump_hit = True
        jump = True
        program_counter += 1
        Flag = [0,0,0,0]
        print(f"{padding(7,dtob(program_counter))}        ",end="")
        for i in simulator_registers.values():
            print(padding(16,dtob(i)),end=" ")
        for i in Flag:
            z += str(i)
        print("0"*12 + z)
        for data in instructions:
            l += 1
            if label in data:
                for i in range(l,len(instructions)):
                    simulator(instructions[i])
                    return 0
                break
            l += 1
    Flag = [0,0,0,0]

def mov_imm(line):
    global Flag
    reg = line[1:4].replace('\r', '')
    imm = line[4:].replace('\r', '')
    if imm[-2:] == "\r":
        imm = imm[:-2]
    val = btod(imm)
    simulator_registers[reg] = val
    Flag = [0,0,0,0]


def rshift(line):
    global Flag
    l = []
    reg = line[1:4].replace('\r', '')
    imm = line[4:].replace('\r', '')
    if imm[-2:] == "\r":
        imm = imm[:-2]
    shiftval = btod(imm)
    regvalue = dtob(simulator_registers[reg])
    pdregvalue = padding(16,regvalue)
    for i in pdregvalue:
        l.append(i)
    for j in range(shiftval):
        l.pop(j)
        l.append('0')
    jl = "".join(l)
    simulator_registers[reg] = btod(jl)
    Flag = [0,0,0,0]

def lshift(line):
    global Flag
    l = []
    reg = line[1:4].replace('\r', '')
    imm = line[4:].replace('\r', '')
    if imm[-2:] == "\r":
        imm = imm[:-2]
    shiftval = btod(imm)
    regvalue = dtob(simulator_registers[reg])
    pdregvalue = padding(16,regvalue)
    for i in pdregvalue:
        l.append(i)
    l.reverse()
    for j in range(shiftval):
        l.pop(j)
        l.append('0')
    l.reverse()
    jl = "".join(l)
    simulator_registers[reg] = btod(jl)
    Flag = [0,0,0,0]

def mov_reg(line):
    global Flag
    reg1 = line[5:8].replace('\r', '')
    reg2 = line[8:].replace('\r', '')
    if reg2[-2:] == "\r":
        reg2 = reg2[:-2]
    if reg2 == "111":
        reg2 = ""
        for i in Flag:
            reg2 += str(i)
        simulator_registers[reg1] = btod(reg2)
        Flag = [0,0,0,0]
    else:
        simulator_registers[reg1] = simulator_registers[reg2]
        Flag = [0,0,0,0]

def invert(line):
    global Flag
    l = []
    reg1 = line[5:8].replace('\r', '')
    reg2 = line[8:].replace('\r', '')
    if reg2[-2:] == "\r":
        reg2 = reg2[:-2]
    reg2val = dtob(simulator_registers[reg2])
    pdreg2val = padding(16,reg2val)
    for i in pdreg2val:
        l.append(i)
    for j in range(len(l)):
        if l[j] == '0':
            l[j] = '1'
        else:
            l[j] = '0'
    invstr = "".join(l)
    simulator_registers[reg1] = btod(invstr)
    Flag = [0,0,0,0]

def cmp(line):
    global Flag
    reg1 = line[5:8].replace('\r', '')
    reg2 = line[8:].replace('\r', '')
    if reg2[-2:] == "\r":
        reg2 = reg2[:-2]
    reg1val = simulator_registers[reg1]
    reg2val = simulator_registers[reg2]
    if reg1val > reg2val:
        Flag = [0,0,0,0]
        Flag[2] = 1
    if reg1val < reg2val:
        Flag = [0,0,0,0]
        Flag[1] = 1
    if reg1val == reg2val:
        Flag = [0,0,0,0]
        Flag[3] = 1

def divde(line):
    global Flag
    reg1 = line[5:8].replace('\r', '')
    reg2 = line[8:].replace('\r', '')
    if reg2[-2:] == "\r":
        reg2 = reg2[:-2]
    reg1val = simulator_registers[reg1]
    reg2val = simulator_registers[reg2]
    if reg2val == 0:
        Flag = [0,0,0,0]
        Flag[0] = 1
        simulator_registers["000"] = 0
        simulator_registers["001"] = 0 
    else:
        simulator_registers["000"] = reg1val//reg2val
        simulator_registers["001"] = reg1val%reg2val
        Flag = [0,0,0,0]



def halt(line):
    global Flag
    Flag = [0,0,0,0]
    global hlt_achieved
    global program_counter
    hlt_achieved = True
    z = ""
    program_counter = btod(counter)
    print(f"{padding(7,dtob(program_counter))}        ",end="")
    for i in simulator_registers.values():
        print(padding(16,dtob(i)),end=" ")
    for i in Flag:
        z += str(i)
    print("0"*12 + z)

instructions_functions = {"00000" : addition , "00001" : subtraction , "00110" : multiply , "01010" : XOR , "01011" : OR , "01100" : AND , "00100" : load , "00101" : store , "01111" : unconditional_jump , "11100" : jump_less , "11101" : jump_greater , "11111" : jump_equal , "11010" : halt , "00010" : mov_imm , "01000" : rshift , "01001" : lshift , "00011" : mov_reg , "01101" : invert , "01110" : cmp , "00111" : divde}

def simulator(binary_instruction):
    global program_counter
    global hlt_achieved
    global simulator_registers
    global jump
    global counter
    l = ""
    counter = binary_instruction[0]
    input_instructions = binary_instruction[1]
    if not hlt_achieved:
        if not jump:
            instruction = instruction_given(input_instructions)
            data = data_given(input_instructions)
            instruction = instruction.replace('\r', '')
            data = data.replace('\r', '')
            instructions_functions[instruction](data)
            if not hlt_achieved and not jump:
                print(f"{padding(7,dtob(program_counter))}        ",end="")
                for i in simulator_registers.values():
                    print(padding(16,dtob(i)),end=" ")
                for i in Flag:
                    l += str(i)
                print("0"*12 + l)
                program_counter += 1
        else:
                jump = False
                program_counter += 1
                data = data_given(input_instructions)
                instruction = instruction_given(input_instructions)
                instructions_functions[instruction](data)
                if not hlt_achieved:
                    print(f"{padding(7,dtob(program_counter))}        ",end="")
                    for i in simulator_registers.values():
                        print(padding(16,dtob(i)),end=" ")
                    for i in Flag:
                        l += str(i)
                    print("0"*12 + l)
    else:
        return 0

data_dump_counter = 0

for binary_instruction in instructions:
    if not hlt_achieved:
        if jump_hit:
            break
        simulator(binary_instruction)


if data_dump_counter  < 128:
    for i in instructions:
        if data_dump_counter < 128:
            print(i[1])
            data_dump_counter += 1


if data_dump_counter  < 128:
    for i in simulator_variables.values():
        if data_dump_counter  < 128:
            print(padding(16,dtob(i)))
            data_dump_counter += 1
if data_dump_counter  < 128:
    for i in range(128 - data_dump_counter):
        print(f"0000000000000000")