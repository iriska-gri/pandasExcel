from pandasimort import UploadCSV
import sys


if __name__ == '__main__':
   # h = UploadCSV(sys.argv[2])
   h = UploadCSV()
   # h.printer()
   getattr(h,sys.argv[1])()
