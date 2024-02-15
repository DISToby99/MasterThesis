import numpy as np
import time


class CSVusage:
    def __init__(self, WriteTo, ReadFrom):
        self.wpath = WriteTo
        self.rpath = ReadFrom
        self.data = [0,0,0,0]

    def makeArray5x1(self, value1, value2, value3, value4, value5):
        npArray = np.array([value1, value2, value3, value4, value5])
        return npArray
    
    def SaveCSV(self, Array):
        np.savetxt(self.wpath, Array, delimiter=',')

    def OpenCSV(self):
        try:
            # Attempt to load the CSV file
            data = np.loadtxt(self.rpath, delimiter=',')

            # Check if the loaded data is empty
            if data.size == 0:
                raise ValueError("CSV file is empty")

            # If the data is not empty, store it in self.data
            self.data = data

        except (ValueError, UserWarning) as e:
            # If an error occurs during loading (e.g., file not found, empty file),
            # or a warning is raised, handle the exception here
            print("Error loading CSV file:", e)

            # Optionally, provide fallback behavior or raise the exception
            # If self.data has been previously loaded and is available, return it
            # Otherwise, return None to indicate that no valid data was loaded
            data = self.data if hasattr(self, 'data') else None

        # Return the loaded data or None if an error occurred
        return data


