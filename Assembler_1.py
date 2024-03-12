#code to make an assembler

def bitbinary20(decimal):
    """ function to convert decimal to binary in 20 bits"""
    if decimal < -524288 or decimal > 524287:
        binary = 'Error: Value of Immediate Out of Range'
    elif decimal >= 0:
        binary = bin(decimal)[2:].zfill(20)
    else:
        binary = bin(2**20 + decimal)[2:]
    return binary

def bitbinary12(decimal):
    """ function to convert decimal to binary in 12 bits"""
    if decimal < -2048 or decimal > 2047:
        binary = 'Error: Value of Immediate Out of Range'
    elif decimal >= 0:
        binary = bin(decimal)[2:].zfill(12)
    else:
        binary = bin(2**12 + decimal)[2:]
    return binary

def instruc_type(x):
    """function to check what is the type of instruction """
    #R = 1; I = 2; S = 3; B = 4; U = 5; J = 6
    type_ = 9
    if x in r_opcodes:
        type_ = 1
    elif x in i_opcodes:
        type_ = 2
    elif x in s_opcodes:
        type_ = 3
    elif x in b_opcodes:
        type_ = 4
    elif x in u_opcodes:
        type_ = 5
    elif x in j_opcodes:
        type_ = 6
    elif x not in r_opcodes or i_opcodes or s_opcodes or b_opcodes or u_opcodes or j_opcodes:
        type_= 7     
    return type_
    
    def instruc_structure(L,t,f):
        '''function to output binaries according to the risc v isa structure. Input is a list L which 
           contains all the instructions as a seperate element and variable t denoting basically the instruction type '''
        #for R type
        if t==1:
            if L[1] and L[2] and L[3] in registers:
                z = r_func7[L[0]]+registers[L[3]]+registers[L[2]]+r_func3[L[0]]+registers[L[1]]+r_opcodes[L[0]]+"\n"
                #print(z)
                return z
            elif L[1] and L[2] and L[3] in abi_registers:
                z = r_func7[L[0]]+abi_registers[L[3]]+abi_registers[L[2]]+r_func3[L[0]]+abi_registers[L[1]]+r_opcodes[L[0]]+"\n"
                #print(z)
                return z
            else:
                t = 14
        #for I type
        if t==2:
            if L[0]=="lw":
                a = bitbinary12(int(L[2]))
                if "Range" not in a:
                    if L[1] and L[3] in registers:
                        z = bitbinary12(int(L[2]))+registers[L[3]]+i_func3[L[0]]+registers[L[1]]+i_opcodes[L[0]]+"\n"
                        #print(z)
                        return z
                    elif L[1] and L[3] in abi_registers:
                        z = bitbinary12(int(L[2]))+abi_registers[L[3]]+i_func3[L[0]]+abi_registers[L[1]]+i_opcodes[L[0]]+"\n"
                        #print(z)
                        return z
                    else:
                        t = 14   
                else:
                    t = 15       
            else:
                a = bitbinary12(int(L[3]))
                if "Range" not in a:
                    if L[1] and L[2] in registers:
                        z = bitbinary12(L[3])+registers[L[2]]+i_func3[L[0]]+registers[L[1]]+i_opcodes[L[0]]+"\n"
                        #print(z)
                        return z
                    elif L[1] and L[2] in abi_registers:
                        z = bitbinary12(int(L[3]))+abi_registers[L[2]]+i_func3[L[0]]+abi_registers[L[1]]+i_opcodes[L[0]]+"\n"
                        #print(z)
                        return z
                    else:
                        t = 14
                else:
                    t = 15
    
        #for S type
        # L = ["instruction","register","imm","register"]
        if t == 3:
            a = bitbinary12(int(L[2]))
            if "Error" not in a:
                if L[1] and L[3] in registers:
                    z = a[0:7]+registers[L[1]]+registers[L[3]]+s_func3[L[0]]+a[7::]+s_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                elif L[1] and L[3] in abi_registers:
                    z = a[0:7]+abi_registers[L[1]]+abi_registers[L[3]]+s_func3[L[0]]+a[7::]+s_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                else:
                    t = 14
            else:
                t = 15
    
        #for B type
        #L = ["function","register","register","imm"]
        if t==4:
            #to handle Labels
            if L[3].isnumeric():              
                a = bitbinary12(int(L[3]))
            else:
                L[3] = 4*i-(LD[L[3]])
                a = bitbinary12((L[3]))
            if "Error" not in a:
                if L[1] and L[2] in registers:
                    z = a[0]+a[2:8]+registers[L[2]]+registers[L[1]]+b_func3[L[0]]+a[8:12]+a[1]+b_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                elif L[1] and L[2] in abi_registers:
                    z = a[0]+a[2:8]+abi_registers[L[2]]+abi_registers[L[1]]+b_func3[L[0]]+a[1]+a[8:12]+b_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                else:
                    t = 14
            else:
                t = 15
        #for U Type
        #L = ["func","register","imm"]
        if t==5:
            a = bitbinary20(int(L[2]))
            if "Error" not in a:
                if L[1] in registers:
                    z = a+registers[L[1]]+u_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                elif L[1] in abi_registers:
                    z = a+abi_registers[L[1]]+u_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                else:
                    t = 14
            else:
                t = 15
        #for J type
        #L = ["func","register","imm"]
        if t == 6:
            a = bitbinary20(int(L[2]))
            if "Error" not in a:
                if L[1] in registers:
                    z =  a[0]+a[0]+a[10:10]+a[9]+a[1:9]+registers[L[1]]+j_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                elif L[1] in abi_registers:
                    z =  a[0]+a[0]+a[10:19]+a[9]+a[1:9]+abi_registers[L[1]]+j_opcodes[L[0]]+"\n"
                    #print(z)
                    return z
                else:
                    t = 14
            else:
                t = 15
        if t == 7:
            z = "Error:Illegal Instruction"+'\n'
            #print(z)
            return z
        if t == 8 or t == 9 or t == 11 or t == 12 or t==13:
            z = 'Syntax Error (missing a "," or blankspace in the instruction) at line number '+str(i)+'\n'
            #print(type(z))
            return z
        if t == 9.5 or t == 10:
            z = 'Syntax Error (missing a "," or blankspace or () in the instruction) at line number '+str(i)+'\n'
            return z
        if t == 14:
            z = 'Synatx Error (Register Name Invalid) at line number '+str(i)+'\n'
            return z
        if t == 15:
            z = 'ValueError: Value of immediate out of range at line number '+str(i)+'\n'
            return z

#to check errors
def error_check(x,t):
    space = 0
    comma = 0
    leftbrac = 0
    rightbrac = 0
    for i in x:
        if i == " ":
            space += 1
        if i == ",":
            comma += 1
        if i == "(":
            leftbrac += 1
        if i == ")":
            rightbrac += 1

    if t == 1 and space!=1 and comma!=2:
        t = 8
    if t == 2 and space != 1 and comma != 2:
        t = 9
    if t == 2 and x[:2] == "lw" and space != 1 and comma != 1 and leftbrac != 1 and rightbrac != 1:
        t = 9.5
    if t == 3 and space != 1 and comma != 1 and leftbrac != 1 and rightbrac != 1:
        t = 10
    if t == 4 and space != 1 and comma != 2:
        t = 11
    if t == 5 and space != 1 and comma != 1:
        t = 12
    if t == 6 and space != 1 and comma!= 1:
        t = 13
    if t not in (8,9,9.5,10,11,12,13):
        t = 0
    return t


#binary encoding for registers
registers = {'x0':'00000',
             'x1':'00001',
             'x2':'00010',
             'x3':'00011',
             'x4':'00100',
             'x5':'00101',
             'x6':'00110',
             'x7':'00111',
             'x8':'01000',
             'x9':'01001',
             'x10':'01010',
             'x11':'01011',
             'x12':'01100',
             'x13':'01101',
             'x14':'01110',
             'x15':'01111',
             'x16':'10000',
             'x17':'10001',
             'x18':'10010',
             'x19':'10011',
             'x20':'10100',
             'x21':'10101',
             'x22':'10110',
             'x23':'10111',
             'x24':'11000',
             'x25':'11001',
             'x26':'11010',
             'x27':'11011',
             'x28':'11100',
             'x29':'11101',
             'x30':'11110',
             'x31':'11111'}

abi_registers = {'zero':'00000',
                 'ra':'00001',
                 'sp':'00010',
                 'gp':'00011',
                 'tp':'00100',
                 't0':'00101',
                 't1':'00110',
                 't2':'00111',
                 's0':'01000',
                 'fp':'01000',
                 's1':'01001',
                 'a0':'01010',
                 'a1':'01011',
                 'a2':'01100',
                 'a3':'01101',
                 'a4':'01110',
                 'a5':'01111',
                 'a6':'10000',
                 'a7':'10001',
                 's2':'10010',
                 's3':'10011',
                 's4':'10100',
                 's5':'10101',
                 's6':'10110',
                 's7':'10111',
                 's8':'11000',
                 's9':'11001',
                 's10':'11010',
                 's11':'11011',
                 't3':'11100',
                 't4':'11101',
                 't5':'11110',
                 't6':'11111'}

#for R Type Instructions
r_opcodes = {"add":"0110011",
             "sub":"0110011",
             "sll":"0110011",
             "slt":"0110011",
             "sltu":"0110011",
             "xor":"0110011",
             "srl":"0110011",
             "or":"0110011",
             "and":"0110011"}

r_func3 = {"add":"000",
           "sub":"000",
           "sll":"001",
           "slt":"010",
           "sltu": "011",
           "xor":"100",
           "srl":"101",
           "or":"110",
           "and":"111"}

r_func7 = {"add":"0000000",
           "sub":"0100000",
           "sll":"0000000",
           "slt":"0000000",
           "sltu":"0000000",
           "xor":"0000000",
           "srl":"0000000",
           "or":"0000000",
           "and":"0000000"}


#for I Type Instructions
i_opcodes = {"lw":"0000011",
             "addi":"0010011",
             "sltiu":"0010011",
             "jalr":"1100111"}

i_func3 = {"lw":"010",
           "addi":"000",
           "sltiu":"011",
           "jalr":"000"}


#for S Type Instruction
s_opcodes = {"sw":"0100011",
             "sb":"0100011",
             "sh":"0100011",
             "sd":"0100011"}

s_func3 = {"sw":"010"}


#for B Type Instruction
b_opcodes = {"beq":"1100011",
             "bne":"1100011",
             "blt":"1100011",
             "bge":"1100011",
             "bltu":"1100011",
             "bgeu":"1100011"}


b_func3 = {"beq":"000",
           "bne":"001",
           "blt":"100",
           "bge":"101",
           "bltu":"110",
           "bgeu":"111"}

#for U Type Instruction
u_opcodes = {"lui":"0110111","auipc":"0010111"}

#for J Type Instruction
j_opcodes = {"jal":"1101111","jalr":"1110011"}

#to check if the function exists in the isa
temp_binary_list = [
"add"
"sub"
"sll"
"slt"
"sltu"
"xor"
"srl"
"or"
"and"
"lw"
"addi"
"sltiu"
"jalr"
"sw"
"beq"
"bne"
"blt"
"bge"
"bltu"
"bgeu"
"lui"
]
in_ = input("Enter the Input File Path: ")
out = input("Enter the Output File Path")

pointer = open(in_,"r")
w_pointer = open(out,"w")
s = pointer.readlines()
#print(len(s))
pointer.seek(0)
L = [] #list to store functions
L1 = []
LD = {} #dictionaries to hold labels
for i in range(0,len(s)):
    j = pointer.readline()
    u = j.replace('\n','')
    u = u.rstrip("\n")
    k = u.split(",")
    l = k[0].split(' ')
    del k[0]
    L = l+k
    if ":" in L[0]:
        L[0] = L[0].replace(":","")
        LD[L[0]] = i*4
        del L[0]
#print(LD)

pointer.seek(0)

for i in range(0,len(s)):
    j = pointer.readline()
    u = j.replace('\n','')
    u = u.rstrip("\n")
    if "(" and ")" in u:
        u = u.replace("(",",")
        u = u.replace(")","")
    #print(u)
    k = u.split(",")
    l = k[0].split(' ')
    del k[0]
    L = l+k
    if ":" in L[0]:
        L[0] = L[0].replace(":","")
        LD[L[0]] = i*4
        del L[0]
    for b in L:
        if len(b)==0:
            continue
        else:
            L1.append(b)
    #print(L1)
    n = instruc_type(L1[0])
    print(j)
    w0 = error_check(j,n)
    #print(w0)
    if w0 == 0:
        n = instruc_type(L1[0])
        w1 = instruc_structure(L1,n,i)
        #print(w1)
        if "Synatx" in w1 or "Range" in w1:
            #w_pointer.seek(0)
            #w_pointer.truncate()
            w_pointer.write(w1)
            #break
        w_pointer.write(w1)
    else:
        #w_pointer.seek(0)
        #w_pointer.truncate()
        w1 = instruc_structure(L1,w0,i)
        w_pointer.write(w1)
        #break
    if i == len(s)-1 and w1 != "00000000000000000000000001100011":
        w_pointer.write("Error:Virtual Halt not being used in the last line")
    L1 = []
    L = []

print("Completed")
pointer.close()
w_pointer.close()
