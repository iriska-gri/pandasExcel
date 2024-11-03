from pandasimort import UploadCSV
from testwork import WorkTest
import sys


if __name__ == '__main__':
   # h = UploadCSV(sys.argv[2])
   h = UploadCSV()
   t= WorkTest()
   # h.printer()
   getattr(t,sys.argv[1])()
