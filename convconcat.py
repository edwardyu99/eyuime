#20221118 : convconcat.py - print("***concat reneeyu_head.txt, reneeyu_canph2345ori.txt, reneeyu_ph2345ori.txt to reneeyu.txt")
# already in convphyus.py

#--------------------
print("***concat reneeyu_head.txt, reneeyu_canph2345ori.txt, reneeyu_ph2345ori.txt to reneeyu.txt")
filehead  = 'reneeyu_head.txt'
filecan  = 'reneeyu_canph2345ori.txt'
fileph   = 'reneeyu_ph2345ori.txt'
filetxt  = 'reneeyu.txt'
import shutil
#import glob

filenames = [filehead, filecan, fileph]

#filenames = glob.glob("*.txt")  # or "file*.txt"
#with open(filetxt, "wb") as outfile:
with open(filetxt,'w+', encoding='utf-16') as outfile:
    for filename in filenames:
#        with open(filename, "rb") as infile:
         with open(filename,'r', encoding='utf-16') as infile:
             shutil.copyfileobj(infile, outfile)
#----------------