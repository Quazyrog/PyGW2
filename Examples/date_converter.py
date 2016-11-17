import sys
#Add parent directory to path to import PyGW2
sys.path.append("..")

import PyGW2.calendar
import datetime

def ReadRealDate():
    y,m,d = map(int, input("Real date (YYYY-MM-DD): ").split("-"))
    return datetime.date(y, m, d)

def ReadMauvelianDate():
    yy,dd = map(int, input("Mauvelian date (like: '1306 256' for 256th day of 1306 year): ").split())
    return PyGW2.calendar.MauvelianDate(yy, dd)

print("Input reference point:")
real = ReadRealDate()
mauvelian = ReadMauvelianDate()

converter = PyGW2.calendar.DateConverter()
converter.setReferencePoint(real, mauvelian)

select = input("(1) Mauvelian -> Real; (2) Real -> Mauvelian: ")
if select == "1":
    date = ReadMauvelianDate()
    print("Converted:", str(converter.mauvelianToReal(date)))
else:
    date = ReadRealDate()
    print("Converted:", str(converter.realToMauvelian(date)))

print("Bye!")
