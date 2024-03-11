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
