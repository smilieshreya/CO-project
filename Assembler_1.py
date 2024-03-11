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
        print(type(z))
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
