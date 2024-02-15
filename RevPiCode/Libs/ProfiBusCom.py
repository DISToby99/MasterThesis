import revpimodio2
import struct
import numpy  as np
import ProfiBusCom as profi

class SendAndGet():
      def __init__(self):
            self.com = ProfiBusCom()
            self.get = ProfiBusGet(self.com)
            self.send = ProfiBusSend(self.com)




      def ReciveData(self):
          OnOff =  self.get.GetValue(port=1, type='bool') 
          StartEstimation = OnOff[0]
          StartMPC = OnOff[1]

          POLF_SP09 = self.get.GetValue(port=8, type='real')
          POLF_SP09 = np.round(POLF_SP09,3) 

          FOR_QT03 = self.get.GetValue(port=16, type='real')
          FOR_QT03 = np.round(FOR_QT03,3)
          
          TRS5_FT01 = self.get.GetValue(port=20, type='real')
          TRS5_FT01 = np.round(TRS5_FT01,3)
          
          TRS5_FT02 = self.get.GetValue(port=24, type='real')
          TRS5_FT02 = np.round(TRS5_FT02,3)
          
          POLF_FT09 = self.get.GetValue(port=28, type='real')
          POLF_FT09 = np.round(POLF_FT09,3)

          PHA18_SED18_QB01 = self.get.GetValue(port=4, type='real')
          PHA18_SED18_QB01 = np.round(PHA18_SED18_QB01,3)
          
      
          storeArray = self.makeArray5x1(FOR_QT03, TRS5_FT01, TRS5_FT02, POLF_FT09, PHA18_SED18_QB01)
          return storeArray, StartEstimation, StartMPC, POLF_SP09
          
 
      def SendData(self, FOR_TRS5_QB01, POLF_SP09, AlarmList):  
          #FOR_TRS5_QB01 = CSV.OpenCSV()
          self.send.SendValue(FOR_TRS5_QB01, port=8, type='real')
          self.send.SendValue(POLF_SP09, port=12, type='real')
          self.send.SendValue(AlarmList, port=1, type='bool')

      def makeArray5x1(self, value1, value2, value3, value4, value5):
          npArray = np.array([value1, value2, value3, value4, value5])
          return npArray

      
class EdgeTrigger:
    def __init__(self):
        self.prev_state = False

    def rising_edge(self, current_state):
        edge = current_state and not self.prev_state
        self.prev_state = current_state
        return edge

    def falling_edge(self, current_state):
        edge = not current_state and self.prev_state
        self.prev_state = current_state
        return edge


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
        elif port == 4 and type=='real':
            b1, b2, b3, b4 = self.In4to7()
            Value = self.Convert4bToReal(b1,b2,b3,b4)
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

            return float_value


    def In1(self):
        b1 = self.rpi.io.Input__1.value 
        return b1 
    
    def In4to7(self):
        # Read 4 bytes from the input register
        b1 = self.rpi.io.Input__4.value
        b2 = self.rpi.io.Input__5.value
        b3 = self.rpi.io.Input__6.value
        b4 = self.rpi.io.Input__7.value
        return b1, b2, b3, b4
    
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
            Byte = self.BinaryToBit(Value)
            self.Out1(Byte)
        elif port == 8 and type=='real':
            Bytes = self.ConvertRealTo4b(Value)
            self.Out8to11(Bytes)
        elif port == 12 and type=='real':
            Bytes = self.ConvertRealTo4b(Value)
            self.Out12to15(Bytes)

    def BinaryToBit(self, binary_string):
        # Initialize an empty list to store the individual bits
        bit_list = []

        # Iterate over the binary string and convert each character to a boolean value
        for bit in binary_string:
            bit_list.append(bit)

        # Ensure that the bit list has 8 elements by padding with False if necessary
        while len(bit_list) < 8:
            bit_list.append(False)
        
        bit_list = bit_list[::-1]

        byte_value = 0
        # Iterate over the bit list and set the corresponding bit in the byte value
        for i, bit in enumerate(bit_list):
            if bit:
                byte_value |= 1 << (7 - i)  # Set the bit at position 7 - i (MSB to LSB)

 
        # Return the individual bits as a tuple
        return byte_value


    def ConvertRealTo4b(self, float_value):
        # Pack the float value into a binary string
        byte_string = struct.pack('<f', float_value)
        
        return byte_string
    
    def Out1(self, byte):
        self.rpi.io.Output__1.value = byte


    def Out8to11(self, byte_string):
        #Divieds the string into 4 bytes
        data1, data2, data3, data4 = byte_string

        self.rpi.io.Output__8.value = data4
        self.rpi.io.Output__9.value = data3
        self.rpi.io.Output__10.value = data2
        self.rpi.io.Output__11.value = data1

    def Out12to15(self, byte_string):
        #Divieds the string into 4 bytes
        data1, data2, data3, data4 = byte_string

        self.rpi.io.Output__12.value = data4
        self.rpi.io.Output__13.value = data3
        self.rpi.io.Output__14.value = data2
        self.rpi.io.Output__15.value = data1