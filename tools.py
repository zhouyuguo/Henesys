import sys,os
p = os.path.abspath('./pycommon')
if p not in sys.path:
    sys.path.insert(0,p)



import pylogger
import garbage_cleaner

logger = pylogger.logger
cleaner = garbage_cleaner.GarbageCleaner()
