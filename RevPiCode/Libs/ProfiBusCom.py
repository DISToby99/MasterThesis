import revpimodio2
import struct
import numpy as np
import ProfiBusCom as profi

class SendAndGet():
    def __init__(self):
        """Initialize the SendAndGet class."""
        self.com = profi.ProfiBusCom()  # Initialize ProfiBus communication
        self.get = profi.ProfiBusGet(self.com)  # Initialize ProfiBusGet instance
        self.send = profi.ProfiBusSend(self.com)  # Initialize ProfiBusSend instance

    def ReciveData(self):
        """Receive data from ProfiBus."""
        # Get values from ProfiBus
        OnOff = self.get.GetValue(port=1, type='bool')
        StartEstimation = OnOff[0]
        StartMPC = OnOff[1]
        UseMeas = OnOff[2]

        POLF_SP09 = self.get.GetValue(port=8, type='real')
        POLF_SP09 = np.round(POLF_SP09, 3)

        FOR_QT03 = self.get.GetValue(port=16, type='real')
        FOR_QT03 = np.round(FOR_QT03, 3)

        TRS5_FT01 = self.get.GetValue(port=20, type='real')
        TRS5_FT01 = np.round(TRS5_FT01, 3)

        TRS5_FT02 = self.get.GetValue(port=24, type='real')
        TRS5_FT02 = np.round(TRS5_FT02, 3)

        POLF_FT09 = self.get.GetValue(port=28, type='real')
        POLF_FT09 = np.round(POLF_FT09, 3)

        PHA18_SED18_QB01 = self.get.GetValue(port=4, type='real')
        PHA18_SED18_QB01 = np.round(PHA18_SED18_QB01, 3)

        FOR_QT01 = self.get.GetValue(port=12, type='real')
        FOR_QT01 = np.round(FOR_QT01, 3)

        # Store received data in an array
        storeArray = self.makeArray5x1(FOR_QT03, TRS5_FT01, TRS5_FT02, POLF_FT09, PHA18_SED18_QB01)

        # Return received data along with control flags
        return storeArray, StartEstimation, StartMPC, POLF_SP09, FOR_QT01, UseMeas

    def SendData(self, FOR_TRS5_QB01, POLF_SP09, AlarmList):
        """Send data over ProfiBus."""
        # Send values over ProfiBus
        self.send.SendValue(FOR_TRS5_QB01, port=8, type='real')
        self.send.SendValue(POLF_SP09, port=12, type='real')
        self.send.SendValue(AlarmList, port=1, type='bool')

    def makeArray5x1(self, value1, value2, value3, value4, value5):
        """Create a 5x1 numpy array from individual values."""
        npArray = np.array([value1, value2, value3, value4, value5])
        return npArray


class EdgeTrigger:
    def __init__(self):
        """Initialize the EdgeTrigger class."""
        self.prev_state = False  # Initialize previous state as False

    def rising_edge(self, current_state):
        """Detect rising edge."""
        edge = current_state and not self.prev_state
        self.prev_state = current_state
        return edge

    def falling_edge(self, current_state):
        """Detect falling edge."""
        edge = not current_state and self.prev_state
        self.prev_state = current_state
        return edge


class ProfiBusCom:
    def __init__(self):
        """Initialize ProfiBus communication."""
        rpi_ = revpimodio2.RevPiModIO(autorefresh=True)
        self.rpi = rpi_


class ProfiBusGet:
    def __init__(self, COM):
        """Initialize ProfiBusGet class."""
        self.rpi = COM.rpi

    def GetValue(self, port, type):
        """Get value from ProfiBus."""
        self.rpi.core.a1green.value = not self.rpi.core.a1green.value  # Toggle a1green
        if port == 1 and type == 'bool':
            b1 = self.In1()
            Value = self.ByteToBinary(b1)
        elif port == 2:
            return 'NaN'
        elif port == 3:
            return 'NaN'
        elif port == 4 and type == 'real':
            b1, b2, b3, b4 = self.In4to7()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 8 and type == 'real':
            b1, b2, b3, b4 = self.In8to11()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 12 and type == 'real':
            b1, b2, b3, b4 = self.In12to15()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 16 and type == 'real':
            b1, b2, b3, b4 = self.In16to19()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 20 and type == 'real':
            b1, b2, b3, b4 = self.In20to23()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 24 and type == 'real':
            b1, b2, b3, b4 = self.In24to27()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        elif port == 28 and type == 'real':
            b1, b2, b3, b4 = self.In28to31()
            Value = self.Convert4bToReal(b1, b2, b3, b4)
        return Value

    def ByteToBinary(self, byte1):
        """Convert byte value to binary representation."""
        # Convert the byte value to binary representation
        binary_string = bin(byte1)[2:].zfill(8)
        bool_list = [bit == '1' for bit in binary_string]
        return tuple(bool_list[::-1])

    def Convert4bToReal(self, byte1, byte2, byte3, byte4):
        """Convert 4 bytes to a real number."""
        # Concatenate the bytes in little-endian order
        byte_string = bytes([byte4, byte3, byte2, byte1])
        # Unpack the byte string as a float
        float_value = struct.unpack('<f', byte_string)[0]
        return float_value

    def In1(self):
        """Read value from Input__1."""
        return self.rpi.io.Input__1.value

    def In4to7(self):
        """Read values from Input__4 to Input__7."""
        return (self.rpi.io.Input__4.value, self.rpi.io.Input__5.value,
                self.rpi.io.Input__6.value, self.rpi.io.Input__7.value)

    def In8to11(self):
        """Read values from Input__8 to Input__11."""
        return (self.rpi.io.Input__8.value, self.rpi.io.Input__9.value,
                self.rpi.io.Input__10.value, self.rpi.io.Input__11.value)

    def In12to15(self):
        """Read values from Input__12 to Input__15."""
        return (self.rpi.io.Input__12.value, self.rpi.io.Input__13.value,
                self.rpi.io.Input__14.value, self.rpi.io.Input__15.value)

    def In16to19(self):
        """Read values from Input__16 to Input__19."""
        return (self.rpi.io.Input__16.value, self.rpi.io.Input__17.value,
                self.rpi.io.Input__18.value, self.rpi.io.Input__19.value)

    def In20to23(self):
        """Read values from Input__20 to Input__23."""
        return (self.rpi.io.Input__20.value, self.rpi.io.Input__21.value,
                self.rpi.io.Input__22.value, self.rpi.io.Input__23.value)

    def In24to27(self):
        """Read values from Input__24 to Input__27."""
        return (self.rpi.io.Input__24.value, self.rpi.io.Input__25.value,
                self.rpi.io.Input__26.value, self.rpi.io.Input__27.value)

    def In28to31(self):
        """Read values from Input__28 to Input__31."""
        return (self.rpi.io.Input__28.value, self.rpi.io.Input__29.value,
                self.rpi.io.Input__30.value, self.rpi.io.Input__31.value)


class ProfiBusSend:
    def __init__(self, COM):
        """Initialize ProfiBusSend class."""
        self.rpi = COM.rpi

    def SendValue(self, Value, port, type):
        """Send value over ProfiBus."""
        if port == 1 and type == 'bool':
            Byte = self.BinaryToBit(Value)
            self.Out1(Byte)
        elif port == 8 and type == 'real':
            Bytes = self.ConvertRealTo4b(Value)
            self.Out8to11(Bytes)
        elif port == 12 and type == 'real':
            Bytes = self.ConvertRealTo4b(Value)
            self.Out12to15(Bytes)

    def BinaryToBit(self, binary_string):
        """Convert binary string to byte value."""
        # Initialize an empty list to store the individual bits
        bit_list = [bit for bit in binary_string]
        # Ensure that the bit list has 8 elements by padding with False if necessary
        while len(bit_list) < 8:
            bit_list.append(False)
        byte_value = 0
        # Iterate over the bit list and set the corresponding bit in the byte value
        for i, bit in enumerate(bit_list):
            if bit:
                byte_value |= 1 << (7 - i)  # Set the bit at position 7 - i (MSB to LSB)
        return byte_value

    def ConvertRealTo4b(self, float_value):
        """Convert real number to 4-byte string."""
        # Pack the float value into a binary string
        byte_string = struct.pack('<f', float_value)
        return byte_string

    def Out1(self, byte):
        """Send byte value to Output__1."""
        self.rpi.io.Output__1.value = byte

    def Out8to11(self, byte_string):
        """Send 4-byte string to Output__8 to Output__11."""
        # Divides the string into 4 bytes
        data1, data2, data3, data4 = byte_string
        # Assign each byte to corresponding output
        self.rpi.io.Output__8.value = data4
        self.rpi.io.Output__9.value = data3
        self.rpi.io.Output__10.value = data2
        self.rpi.io.Output__11.value = data1

    def Out12to15(self, byte_string):
        """Send 4-byte string to Output__12 to Output__15."""
        # Divides the string into 4 bytes
        data1, data2, data3, data4 = byte_string
        # Assign each byte to corresponding output
        self.rpi.io.Output__12.value = data4
        self.rpi.io.Output__13.value = data3
        self.rpi.io.Output__14.value = data2
        self.rpi.io.Output__15.value = data1
