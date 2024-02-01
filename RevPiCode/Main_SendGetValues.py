import ProfiBusCom as profi
import ReadWriteCSVs as rwCSV
from time import sleep
import numpy  as np
import sysidentpy

com = profi.ProfiBusCom()
get = profi.ProfiBusGet(com)
send = profi.ProfiBusSend(com)

CSV = rwCSV.CSVusage(WriteTo='/home/pi/Desktop/CSVs/X.csv', ReadFrom='/home/pi/Desktop/CSVs/y.csv')

Value = 9.33


while True:
    DigValue = get.GetValue(port=1, type='bool')
    StartBit = DigValue[0]
    if StartBit:
          send.SendValue(Value, port=8, type='real')
          FOR_QT03 = get.GetValue(port=16, type='real')
          FOR_QT03 = np.round(FOR_QT03,3)
          sleep(0.1) 
          
          TRS5_FT01 = get.GetValue(port=20, type='real')
          TRS5_FT01 = np.round(TRS5_FT01,3)
          sleep(0.1) 
          
          TRS5_FT02 = get.GetValue(port=24, type='real')
          TRS5_FT02 = np.round(TRS5_FT02,3)
          sleep(0.1) 
          
          POLF_FT09 = get.GetValue(port=28, type='real')
          POLF_FT09 = np.round(POLF_FT09,3)
          
          print('FOR_QT03:', FOR_QT03, 'TRS5_FT01:', TRS5_FT01, 'TRS5_FT02:', TRS5_FT02, 'POLF_FT09:', POLF_FT09)
          storeArray = CSV.makeArray4x1(FOR_QT03, TRS5_FT01, TRS5_FT02, POLF_FT09)
          CSV.SaveCSV(storeArray)
          CSV.OpenCSV()

          print('\n')

    sleep(10) 