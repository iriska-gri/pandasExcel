from pandasimort import UploadCSV
from testwork import WorkTest
from app import MainWindow
import sys


if __name__ == '__main__':
   # h = UploadCSV(sys.argv[2])
   h = UploadCSV()
   t= WorkTest()
   p = MainWindow()

   # getattr(p)()
   # h.printer()
   getattr(t,sys.argv[1])()
