import numpy as np


class CSVusage:
    def __init__(self, WriteTo, ReadFrom):
        self.wpath = WriteTo
        self.rpath = ReadFrom

    def makeArray4x1(self, value1, value2, value3, value4):
        npArray = np.array([value1, value2, value3, value4])
        return npArray
    
    def SaveCSV(self, Array):
        # Format for floating point numbers
        #fmt_str = ',%.3f'

        # Save the data to a CSV file
        np.savetxt(self.wpath, Array, delimiter=',')#, header=self.headers, fmt=fmt_str, newline='')

    def OpenCSV(self):
        data = np.loadtxt(self.wpath, delimiter=',')
        print(data)
