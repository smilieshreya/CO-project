# for implementing a risv simulator

#function to convert decimal to binary in 32 bits
def decimal_to_binary(decimal):
    """Convert decimal to binary string"""
    binary32 = bin(decimal & 0xFFFFFFFF)[2:].zfill(32)
    binary32 = '0b' + binary32
    return binary32

#function to convert bin to dec
def bin_to_dec(binary):
    '''function to convert the binary value to decimal. this function is not used for all the immediate values '''
    # Check if the number is negative (2's complement)
    if binary[0] == '1':
        # Convert binary string to decimal integer
        decimal = int(binary, 2)
        # Perform 2's complement operation
        num_bits = len(binary)
        decimal -= (1 << num_bits)
    else:
        # Convert binary string to decimal integer
        decimal = int(binary, 2)
    return decimal

#function to convert dec into 20bit bin
def bitbinary20(decimal):
    """ function to convert decimal to binary in 20 bits"""
    if decimal < -524288 or decimal > 524287:
        raise ValueError("Value out of Range")
    if decimal >= 0:
        binary = bin(decimal)[2:].zfill(20)
    else:
        binary = bin(2**20 + decimal)[2:]
    return binary

#function to convert bin to hex..
def binary_to_hex(binary_str):
    # Convert binary string to integer
    decimal_num = int(binary_str, 2)
    # Convert integer to hexadecimal string
    hex_str = hex(decimal_num)
    # Remove '0x' prefix from hexadecimal string
    hex_str = hex_str[2:]
    return hex_str.lower()


def binary_to_Udecimal(binary):
    decimal = 0
    power = len(binary) - 1  # Starting from the leftmost bit

    for bit in binary:
        if bit == '1':
            decimal += 2 ** power
        power -= 1
    return decimal

#function to create the operation bit

def combine(x):
    ''' function that combines the diff characterizing binaries in the given 
    binary and passes them onto the instr_type function'''
    f7 = x[0:7]
    f3 = x[17:20]
    op = x[25:32]
    t1 = str(f7)+str(f3)+str(op)
    t2 = str(f3)+str(op)
    t3 = str(op)
    return instr_type(t1,t2,t3)

#function to find out the type of instruction
def instr_type (x1,x2,x3):
    '''function to find the type of instruction from the given binary'''
    typ = 0
    #for r type
    if x1 in type_r:
        typ = 1
    #for i,s,b type
    elif x2 in type_i:
        typ = 2
    elif x2 in type_s:
        typ = 3
    elif x2 in type_b:
        typ = 4 
    #for u and j type
    elif x3 in type_u:
        typ = 5
    elif x3 in type_j:
        typ = 6
    else:
        typ = -1
    return typ

#function for executing the diff operations

def _execute(types,b):
    ''' function that interprets the given binary 
    and performs the operation and stores the value'''
    #for R type functions....
    if types==1:
        f7 = b[0:7]
        f3 = b[17:20]
        op = b[25:32]
        t1 = str(f7)+str(f3)+str(op)
        oper2 = abi_registers[str(b[7:12])]   # for rs2
        #print(oper2," OPER3 ")
        zz1 = abi_registers[str(b[12:17])]  # for rs1
        #print(zz1," OPER2 ")
        zz3 = abi_registers[str(b[20:25])] # for rd
        #print(zz3," OPER1 ")
        oper = type_r[t1]
        if oper == "add":
            #if str(oper1) in abi_registers_value and str(oper2) in abi_registers_value and str(oper3) in abi_registers_value:
            #print(abi_registers_value[oper1][2:0])
            abi_registers_value[str(zz3)] = (decimal_to_binary((bin_to_dec((abi_registers_value[zz1][2::]))+bin_to_dec((abi_registers_value[oper2][2::])))))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "sub":
            abi_registers_value[str(zz3)] = (decimal_to_binary((bin_to_dec((abi_registers_value[zz1][2::]))) - (bin_to_dec((abi_registers_value[oper2][2::])))))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "sll":
            #v = (int(abi_registers_value[oper2]))
            #abi_registers_value[str(oper3)] = bin_to_dec(bitbinary20(int(abi_registers_value[oper1]))[v::]+"0"*v)
            abi_registers_value[str(zz3)] = decimal_to_binary(binary_to_Udecimal(((abi_registers_value[zz1][2::]))) << binary_to_Udecimal((((abi_registers_value[oper2][2::][27::])))))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper=="slt":
            if bin_to_dec((abi_registers_value[zz1][2::])) < bin_to_dec(((abi_registers_value[oper2][2::]))):
                abi_registers_value[str(zz3)] = "0b00000000000000000000000000000001"
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
            else:
                abi_registers_value[str(zz3)] = "0b00000000000000000000000000000000"
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper=="sltu":
            if binary_to_Udecimal((abi_registers_value[zz1][2::])) < 0 or binary_to_Udecimal((abi_registers_value[oper2][2::])) < 0:
                abi_registers_value[str(zz3)] = "0b00000000000000000000000000000000"
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
            else:
                if binary_to_Udecimal(abi_registers_value[zz1][2::]) < binary_to_Udecimal((abi_registers_value[oper2][2::])):
                    abi_registers_value[str(zz3)] = "0b00000000000000000000000000000001"
                    program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
                else:
                    abi_registers_value[str(zz3)] = "0b00000000000000000000000000000000"
                    program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "xor":
            abi_registers_value[str(zz3)] = decimal_to_binary((bin_to_dec((abi_registers_value[zz1][2::]))) ^ bin_to_dec((abi_registers_value[oper2][2::])))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "srl":
            abi_registers_value[str(zz3)] = decimal_to_binary(binary_to_Udecimal((str(abi_registers_value[zz1][2::]))) >> binary_to_Udecimal(str(abi_registers_value[oper2][2::][27::])))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "or":
            abi_registers_value[str(zz3)] = decimal_to_binary(bin_to_dec((abi_registers_value[zz1][2::])) | bin_to_dec((abi_registers_value[oper2][2::])))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "and":
            #print(bin_to_dec(abi_registers_value[oper1][2::]))
            abi_registers_value[str(zz3)] = decimal_to_binary(bin_to_dec(abi_registers_value[zz1][2::]) & bin_to_dec(abi_registers_value[oper2][2::]))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
    
    #for I type functions....
    elif types == 2:
        f3 = b[17:20]
        op = b[25:32]
        t2 = str(f3)+str(op)
        oper = type_i[t2]
        q1 = abi_registers[str(b[12:17])]  # for rs1 -- should be destination
        q2 = abi_registers[str(b[20:25])] # for destination register -- should be rs1
        imm = str(b[0:12]) # for immediate values 
        if oper == "lw":
            abi_registers_value[str(q2)] = data_memory["0x000"+str(binary_to_hex(decimal_to_binary(bin_to_dec(abi_registers_value[q1][2::])+ bin_to_dec(imm))))]
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "addi":
            abi_registers_value[str(q2)] = decimal_to_binary((bin_to_dec(abi_registers_value[q1][2::])) + (bin_to_dec(imm)))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "sltiu":
            if (bin_to_dec(abi_registers_value[q1][2::])) < bin_to_dec(imm):
                abi_registers_value[str(q2)] = "0b00000000000000000000000000000001"
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
            else:
                abi_registers_value[str(q2)] = "0b00000000000000000000000000000000"
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "jalr":
            abi_registers_value[str(q2)] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
            program_counter['pc'] = (decimal_to_binary((bin_to_dec(abi_registers_value[q1][2::]))+ (bin_to_dec(imm))))[0:33] + "0"
    
    #for S type functions....
    elif types == 3:
        f3 = b[17:20]
        op = b[25:32]
        t2 = str(f3)+str(op)
        oper = type_s[t2]
        if oper == "sw":
            imm = b[0:7]+b[20:25]
            #rd = b[7:12]
            #rs = b[12:17]
            z0 = abi_registers[str(b[12:17])]
            zz0 = abi_registers[str(b[7:12])]
            #print("0x000"+str(binary_to_hex(decimal_to_binary(bin_to_dec(abi_registers_value[oper1][2::])+ bin_to_dec(imm)))))
            data_memory["0x000"+str(binary_to_hex(decimal_to_binary(bin_to_dec(abi_registers_value[z0][2::])+ bin_to_dec(imm))))] = abi_registers_value[str(zz0)]
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
    
    #for B type functions....
    elif types == 4:
        f3 = b[17:20]
        op = b[25:32]
        t2 = str(f3)+str(op)
        oper = type_b[t2]
        z5 = abi_registers[str(b[12:17])]
        z6 = abi_registers[str(b[7:12])]
        imm = "0b"+b[0]+b[24]+b[1:7]+b[20:24]+"0"
        #print (imm)

        if oper=="beq":
            if bin_to_dec(abi_registers_value[z5]) == bin_to_dec(abi_registers_value[z6]):
                #print("here")
                if z5 == "zero" and z6 == "zero" and imm=='0b0000000000000':
                    global v
                    v = -1
                else:
                    program_counter['pc'] =  decimal_to_binary(bin_to_dec(program_counter['pc'])+bin_to_dec(str(imm)[2::]))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        
        elif oper=="bne":
            if bin_to_dec(abi_registers_value[z5]) != bin_to_dec(abi_registers_value[z6]):
                program_counter['pc'] =  decimal_to_binary(bin_to_dec(program_counter['pc'])+bin_to_dec(imm[2::]))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        
        elif oper=="bge":
            if bin_to_dec(abi_registers_value[z5]) > bin_to_dec(abi_registers_value[z6]):
                program_counter['pc'] =  decimal_to_binary(bin_to_dec(program_counter['pc'])+bin_to_dec(imm[2::]))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)

        elif oper=="bgeu":
            if bin_to_dec(abi_registers_value[z5]) > bin_to_dec(abi_registers_value[z6]):
                program_counter['pc'] =  decimal_to_binary(int(program_counter['pc'],2)+int(imm,2))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)

        elif oper=="blt":
            if bin_to_dec(abi_registers_value[z5]) < bin_to_dec(abi_registers_value[z6]):
                program_counter['pc'] =  decimal_to_binary(bin_to_dec(program_counter['pc'])+bin_to_dec(imm[2::]))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)

        elif oper=="bltu":
            if bin_to_dec(abi_registers_value[z5]) < bin_to_dec(abi_registers_value[z6]):
                program_counter['pc'] =  decimal_to_binary(int(program_counter['pc'],2)+int(imm,2))
            else:
                program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        # else:
        #     program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)

    #for U Type Instruction
    elif types == 5:
        t3 = str(b[25:32])
        oper = type_u[t3]
        z7 = abi_registers[(str(b[20:25]))]
        imm = b[0:20]

        if oper == "lui":
            abi_registers_value[str(z7)] = "0b"+str(imm)+"0"*12
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
        elif oper == "auipc":
            abi_registers_value[str(z7)] = decimal_to_binary(bin_to_dec(program_counter['pc']) + bin_to_dec(str(imm)+"0"*12))
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
    
    #for J type Instruction
    elif types == 6:
        t3 = str(b[25:32])
        oper = type_j[t3]
        z8 = abi_registers[(str(b[20:25]))]
        imm = b[0]+b[1:9]+b[9]+b[10:20]
        if oper == "jal":
            abi_registers_value[str(z8)] = decimal_to_binary(bin_to_dec(program_counter['pc'])+4)
            program_counter['pc'] = decimal_to_binary(bin_to_dec(program_counter['pc']) + bin_to_dec(imm[0:12]))


#for holding the value of PC...
program_counter = {"pc":"0b00000000000000000000000000000000"}

# encoding for registers...
abi_registers = {'00000': 'zero',
             '00001': 'ra', 
             '00010': 'sp', 
             '00011': 'gp', 
             '00100': 'tp', 
             '00101': 't0', 
             '00110': 't1', 
             '00111': 't2', 
             '01000': 's0', 
             '01001': 's1', 
             '01010': 'a0', 
             '01011': 'a1', 
             '01100': 'a2', 
             '01101': 'a3', 
             '01110': 'a4', 
             '01111': 'a5', 
             '10000': 'a6', 
             '10001': 'a7', 
             '10010': 's2', 
             '10011': 's3', 
             '10100': 's4', 
             '10101': 's5', 
             '10110': 's6', 
             '10111': 's7', 
             '11000': 's8', 
             '11001': 's9', 
             '11010': 's10', 
             '11011': 's11', 
             '11100': 't3', 
             '11101': 't4', 
             '11110': 't5', 
             '11111': 't6'}

registers = {'00000': 'x0',
             '00001': 'x1', 
             '00010': 'x2', 
             '00011': 'x3', 
             '00100': 'x4', 
             '00101': 'x5', 
             '00110': 'x6', 
             '00111': 'x7', 
             '01000': 'x8', 
             '01001': 'x9', 
             '01010': 'x10', 
             '01011': 'x11', 
             '01100': 'x12', 
             '01101': 'x13', 
             '01110': 'x14', 
             '01111': 'x15', 
             '10000': 'x16', 
             '10001': 'x17', 
             '10010': 'x18', 
             '10011': 'x19', 
             '10100': 'x20', 
             '10101': 'x21', 
             '10110': 'x22', 
             '10111': 'x23', 
             '11000': 'x24', 
             '11001': 'x25', 
             '11010': 'x26', 
             '11011': 'x27', 
             '11100': 'x28', 
             '11101': 'x29', 
             '11110': 'x30', 
             '11111': 'x31'}

#for holding the data values
abi_registers_value = {'zero':"0b00000000000000000000000000000000",
                     'ra':'0b00000000000000000000000000000000',
                     'sp':'0b00000000000000000000000100000000',
                     'gp':'0b00000000000000000000000000000000',
                     'tp':'0b00000000000000000000000000000000',
                     't0':'0b00000000000000000000000000000000',
                     't1':'0b00000000000000000000000000000000',
                     't2':'0b00000000000000000000000000000000',
                     's0':'0b00000000000000000000000000000000',
                     's1':'0b00000000000000000000000000000000',
                     'a0':'0b00000000000000000000000000000000',
                     'a1':'0b00000000000000000000000000000000',
                     'a2':'0b00000000000000000000000000000000',
                     'a3':'0b00000000000000000000000000000000',
                     'a4':'0b00000000000000000000000000000000',
                     'a5':'0b00000000000000000000000000000000',
                     'a6':'0b00000000000000000000000000000000',
                     'a7':'0b00000000000000000000000000000000',
                     's2':'0b00000000000000000000000000000000',
                     's3':'0b00000000000000000000000000000000',
                     's4':'0b00000000000000000000000000000000',
                     's5':'0b00000000000000000000000000000000',
                     's6':'0b00000000000000000000000000000000',
                     's7':'0b00000000000000000000000000000000',
                     's8':'0b00000000000000000000000000000000',
                     's9':'0b00000000000000000000000000000000',
                    's10':'0b00000000000000000000000000000000',
                    's11':'0b00000000000000000000000000000000',
                     't3':'0b00000000000000000000000000000000',
                     't4':'0b00000000000000000000000000000000',
                     't5':'0b00000000000000000000000000000000',
                     't6':'0b00000000000000000000000000000000'}

registers_value= {'x0':'0b00000000000000000000000000000000',
                 'x1' :'0b00000000000000000000000000000000',
                 'x2' :'0b00000000000000000000000000000000',
                 'x3' :'0b00000000000000000000000000000000',
                 'x4' :'0b00000000000000000000000000000000',
                 'x5' :'0b00000000000000000000000000000000',
                 'x6' :'0b00000000000000000000000000000000',
                 'x7' :'0b00000000000000000000000000000000',
                 'x8' :'0b00000000000000000000000000000000',
                 'x9' :'0b00000000000000000000000000000000',
                 'x10':'0b00000000000000000000000000000000',
                 'x11':'0b00000000000000000000000000000000',
                 'x12':'0b00000000000000000000000000000000',
                 'x13':'0b00000000000000000000000000000000',
                 'x14':'0b00000000000000000000000000000000',
                 'x15':'0b00000000000000000000000000000000',
                 'x16':'0b00000000000000000000000000000000',
                 'x17':'0b00000000000000000000000000000000',
                 'x18':'0b00000000000000000000000000000000',
                 'x19':'0b00000000000000000000000000000000',
                 'x20':'0b00000000000000000000000000000000',
                 'x21':'0b00000000000000000000000000000000',
                 'x22':'0b00000000000000000000000000000000',
                 'x23':'0b00000000000000000000000000000000',
                 'x24':'0b00000000000000000000000000000000',
                 'x25':'0b00000000000000000000000000000000',
                 'x26':'0b00000000000000000000000000000000',
                 'x27':'0b00000000000000000000000000000000',
                 'x28':'0b00000000000000000000000000000000',
                 'x29':'0b00000000000000000000000000000000',
                 'x30':'0b00000000000000000000000000000000',
                 'x31':'0b00000000000000000000000000000000'}

#for holding data at memory addresses
data_memory = { "0x00010000":'0b00000000000000000000000000000000',
                "0x00010004":'0b00000000000000000000000000000000',
                "0x00010008":'0b00000000000000000000000000000000',
                "0x0001000c":'0b00000000000000000000000000000000',
                "0x00010010":'0b00000000000000000000000000000000',
                "0x00010014":'0b00000000000000000000000000000000',
                "0x00010018":'0b00000000000000000000000000000000',
                "0x0001001c":'0b00000000000000000000000000000000',
                "0x00010020":'0b00000000000000000000000000000000',
                "0x00010024":'0b00000000000000000000000000000000',
                "0x00010028":'0b00000000000000000000000000000000',
                "0x0001002c":'0b00000000000000000000000000000000',
                "0x00010030":'0b00000000000000000000000000000000',
                "0x00010034":'0b00000000000000000000000000000000',
                "0x00010038":'0b00000000000000000000000000000000',
                "0x0001003c":'0b00000000000000000000000000000000',
                "0x00010040":'0b00000000000000000000000000000000',
                "0x00010044":'0b00000000000000000000000000000000',
                "0x00010048":'0b00000000000000000000000000000000',
                "0x0001004c":'0b00000000000000000000000000000000',
                "0x00010050":'0b00000000000000000000000000000000',
                "0x00010054":'0b00000000000000000000000000000000',
                "0x00010058":'0b00000000000000000000000000000000',
                "0x0001005c":'0b00000000000000000000000000000000',
                "0x00010060":'0b00000000000000000000000000000000',
                "0x00010064":'0b00000000000000000000000000000000',
                "0x00010068":'0b00000000000000000000000000000000',
                "0x0001006c":'0b00000000000000000000000000000000',
                "0x00010070":'0b00000000000000000000000000000000',
                "0x00010074":'0b00000000000000000000000000000000',
                "0x00010078":'0b00000000000000000000000000000000',
                "0x0001007c":'0b00000000000000000000000000000000'}

#program memory implementation
program_memory = {"00000000000000000000000000000000":"0",
                  "00000000000000000000000000000100":"0",
                  "00000000000000000000000000001000":"0",
                  "00000000000000000000000000001100":"0",
                  "00000000000000000000000000010000":"0",
                  "00000000000000000000000000010100":"0",
                  "00000000000000000000000000011000":"0",
                  "00000000000000000000000000011100":"0",
                  "00000000000000000000000000100000":"0",
                  "00000000000000000000000000100100":"0",
                  "00000000000000000000000000101000":"0",
                  "00000000000000000000000000101100":"0",
                  "00000000000000000000000000110000":"0",
                  "00000000000000000000000000110100":"0",
                  "00000000000000000000000000111000":"0",
                  "00000000000000000000000000111100":"0",
                  "00000000000000000000000001000000":"0",
                  "00000000000000000000000001000100":"0",
                  "00000000000000000000000001001000":"0",
                  "00000000000000000000000001001100":"0",
                  "00000000000000000000000001010000":"0",
                  "00000000000000000000000001010100":"0",
                  "00000000000000000000000001011000":"0",
                  "00000000000000000000000001011100":"0",
                  "00000000000000000000000001100000":"0",
                  "00000000000000000000000001100100":"0",
                  "00000000000000000000000001101000":"0",
                  "00000000000000000000000001101100":"0",
                  "00000000000000000000000001110000":"0",
                  "00000000000000000000000001110100":"0",
                  "00000000000000000000000001111000":"0",
                  "00000000000000000000000001111100":"0",
                  "00000000000000000000000010000000":"0",
                  "00000000000000000000000010000100":"0",
                  "00000000000000000000000010001000":"0",
                  "00000000000000000000000010001100":"0",
                  "00000000000000000000000010010000":"0",
                  "00000000000000000000000010010100":"0",
                  "00000000000000000000000010011000":"0",
                  "00000000000000000000000010011100":"0",
                  "00000000000000000000000010100000":"0",
                  "00000000000000000000000010100100":"0",
                  "00000000000000000000000010101000":"0",
                  "00000000000000000000000010101100":"0",
                  "00000000000000000000000010110000":"0",
                  "00000000000000000000000010110100":"0",
                  "00000000000000000000000010111000":"0",
                  "00000000000000000000000010111100":"0",
                  "00000000000000000000000011000000":"0",
                  "00000000000000000000000011000100":"0",
                  "00000000000000000000000011001000":"0",
                  "00000000000000000000000011001100":"0",
                  "00000000000000000000000011010000":"0",
                  "00000000000000000000000011010100":"0",
                  "00000000000000000000000011011000":"0",
                  "00000000000000000000000011011100":"0",
                  "00000000000000000000000011100000":"0",
                  "00000000000000000000000011100100":"0",
                  "00000000000000000000000011101000":"0",
                  "00000000000000000000000011101100":"0",
                  "00000000000000000000000011110000":"0",
                  "00000000000000000000000011110100":"0",
                  "00000000000000000000000011111000":"0",
                  "00000000000000000000000011111100":"0",
                  "00000000000000000000000011111111":"0" }

#encoding for R type

type_r = {"00000000000110011":"add",
          "01000000000110011":"sub",
          "00000000010110011":"sll",
          "00000000100110011":"slt",
          "00000000110110011":"sltu",
          "00000001000110011":"xor",
          "00000001010110011":"srl",
          "00000001100110011":"or",
          "00000001110110011":"and"}

#encoding for I type
type_i ={"0100000011":"lw",
         "0000010011":"addi",
         "0110010011":"sltiu",
         "0001100111":"jalr"}

#encoding for S type
type_s = {"0100100011":"sw"}

#encoding for R type
type_b = {"0001100011":"beq",
          "0011100011":"bne",
          "1001100011":"blt",
          "1011100011":"bge",
          "1101100011":"bltu",
          "1111100011":"bgeu"}

#encoding for U type
type_u = {"0110111":"lui",
          "0010111":"auipc"}

#encoding for J type
type_j = {"1101111":"jal"}


r_pointer = "D:\\DOWNLOADS\\CO Project evaluation framework Apr2\\CO Project evaluation framework Apr2\\automatedTesting\\tests\\bin\\simple\\s_test5.txt"
w_pointer = "D:\\DOWNLOADS\\CO Project evaluation framework Apr2\\CO Project evaluation framework Apr2\\automatedTesting\\tests\\bin\\simple\\test5_data.txt"

with open(r_pointer,"r") as R:
    instruc_list = R.readlines()
    R.close()

l_instruc = len(instruc_list)
m = 0
for j in program_memory:
    if m<l_instruc:
        v = instruc_list[m].replace("\n","")
        program_memory[j] = v
        m += 1
    else:
        m = 0
        break
v = 0
with open(w_pointer,"w") as W:
    while v != -1:
        #print("here")
        T1 = program_memory[program_counter["pc"][2::]]
        T2 = combine(program_memory[program_counter["pc"][2::]])
        _execute(T2,T1)
        abi_registers_value['zero'] = "0b00000000000000000000000000000000"
        w1 = program_counter['pc']
        W.write(w1)
        W.write(" ")
        for z1 in abi_registers_value.values():
            #print(z1)
            W.write(z1)
            W.write(" ")
        W.write("\n")


    for z2 in data_memory:
            z3 = str(z2)+":"+str(data_memory[z2])
            W.write(z3)
            W.write("\n")  
    W.close()

# t = 0
# for i in program_memory:
#     if t<l_instruc:
#         print(i,":",program_memory[i])
#         t = t+1



#code to converted to comment later.......
# x = "11000000000111111111000011101111"
# print(str(x[25:32]))
# T1= combine(x)
# print(T1)
# _execute(T1,x)

# print(type(T1))
# print(abi_registers_value.values())
# print(abi_registers_value["ra"])
# print(program_counter['pc'])


#11000000000111111111000011101111
#11111111111111000000000111111111
#code to converted to comment later (END).......



