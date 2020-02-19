from serializer import MdbdSerializer 
import os
import sys

PATH = './data_access/export/'

limit = 2000000

#can use parameter limit
if len(sys.argv)>1:
    limit = sys.argv[1]

if os.path.isdir(PATH):
    serializer = MdbdSerializer(PATH, limit)
    serializer.start()
else:
    print('no path to export file')
