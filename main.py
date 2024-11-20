from pandasimort import UploadCSV
from testwork import WorkTest
from auchan_frov import Frov
from app import MainWindow
import sys


if __name__ == '__main__':
   # h = UploadCSV(sys.argv[2])
   h = UploadCSV()
   t= WorkTest()
   f = Frov()
   # p = MainWindow()

   # getattr(p)()
   # h.printer()
   getattr(f,sys.argv[1])()
