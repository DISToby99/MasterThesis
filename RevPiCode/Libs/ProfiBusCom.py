import revpimodio2
import struct

class ProfiBusCom:
    def __init__(self):
        rpi_ = revpimodio2.RevPiModIO(autorefresh=True)
        self.rpi = rpi_

class ProfiBusGet:
    def __init__(self, COM):
        self.rpi = COM.rpi

    def GetValue(self, port, type):
        self.rpi.core.a1green.value = not self.rpi.core.a1green.value
        if port == 1 and type=='bool':
            b1 = self.In1()
            Value = self.ByteToBinary(b1)
        elif port == 2:
            return 'NaN'
        elif port == 3:
            return 'NaN'
        elif port == 4:
            return 'NaN'
        elif port == 5:
            return 'NaN'
        elif port == 6:
            return 'NaN'
        elif port == 7:
            return 'NaN'
        elif port == 8 and type=='real':
            b1, b2, b3, b4 = self.In8to11()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
        elif port == 16 and type=='real':
            b1, b2, b3, b4 = self.In16to19()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
        elif port == 20 and type=='real':
            b1, b2, b3, b4 = self.In20to23()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
        elif port == 24 and type=='real':
            b1, b2, b3, b4 = self.In24to27()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
        elif port == 28 and type=='real':
            b1, b2, b3, b4 = self.In28to31()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
        
        return Value 


    def ByteToBinary(self, byte1):
        # Convert the byte value to binary representation
        binary_string = bin(byte1)[2:].zfill(8)
        
        # Ensure that the binary string has 8 digits by padding with zeros if necessary
        padded_binary_string = binary_string.zfill(8)


        bool_list = []
        for bit in binary_string:
            bool_list.append(bit == '1')

        bit1 = bool(bool_list[7])
        bit2 = bool(bool_list[6])
        bit3 = bool(bool_list[5])
        bit4 = bool(bool_list[4])
        bit5 = bool(bool_list[3])
        bit6 = bool(bool_list[2])
        bit7 = bool(bool_list[1])
        bit8 = bool(bool_list[0])
        
        return bit1, bit2, bit3, bit4, bit5, bit6, bit7, bit8       
    
    def Convert4bToReal(self, byte1,byte2,byte3,byte4):
        # Concatenate the bytes in little-endian order
            byte_string = bytes([byte4, byte3, byte2, byte1])

            # Unpack the byte string as a float
            float_value = struct.unpack('<f', byte_string)[0]

            # Print the float value
            #print(float_value)
            return float_value


    def In1(self):
        b1 = self.rpi.io.Input__1.value 
        return b1 
    
    def In8to11(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__8.value
        b2 = self.rpi.io.Input__9.value
        b3 = self.rpi.io.Input__10.value
        b4 = self.rpi.io.Input__11.value
        return b1, b2, b3, b4
    
    def In16to19(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__16.value
        b2 = self.rpi.io.Input__17.value
        b3 = self.rpi.io.Input__18.value
        b4 = self.rpi.io.Input__19.value
        return b1, b2, b3, b4
    
    def In20to23(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__20.value
        b2 = self.rpi.io.Input__21.value
        b3 = self.rpi.io.Input__22.value
        b4 = self.rpi.io.Input__23.value
        return b1, b2, b3, b4
    
    def In24to27(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__24.value
        b2 = self.rpi.io.Input__25.value
        b3 = self.rpi.io.Input__26.value
        b4 = self.rpi.io.Input__27.value
        return b1, b2, b3, b4
    
    def In28to31(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__28.value
        b2 = self.rpi.io.Input__29.value
        b3 = self.rpi.io.Input__30.value
        b4 = self.rpi.io.Input__31.value
        return b1, b2, b3, b4
      

class ProfiBusSend:
    def __init__(self, COM):
        self.rpi = COM.rpi

    def SendValue(self, Value, port, type):
        if port == 1 and type=='bool':
            return 'NaN'    
        elif port == 2:
            return 'NaN'
        elif port == 3:
            return 'NaN'
        elif port == 4:
            return 'NaN'
        elif port == 5:
            return 'NaN'
        elif port == 6:
            return 'NaN'
        elif port == 7:
            return 'NaN'
        elif port == 8 and type=='real':
            Bytes = self.ConvertRealTo4b(Value)
            Value = self.Out8to11(Bytes)
        
        return Value 
    
    def ConvertRealTo4b(self, float_value):
        # Pack the float value into a binary string
        byte_string = struct.pack('<f', float_value)
        
        return byte_string

    def Out8to11(self, byte_string):
        #Divieds the string into 4 bytes
        data1, data2, data3, data4 = byte_string

        self.rpi.io.Output__8.value = data4
        self.rpi.io.Output__9.value = data3
        self.rpi.io.Output__10.value = data2
        self.rpi.io.Output__11.value = data1