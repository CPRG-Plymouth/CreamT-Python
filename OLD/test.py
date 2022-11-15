import os

filepath = 'C:\\SCAN_DATA\\DW_FILES\\test.dat'

basepath = os.path.split(filepath)
basepath = basepath[0]

print(basepath)
