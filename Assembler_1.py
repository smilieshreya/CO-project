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
