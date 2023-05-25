import codecs
import os
filepath = 'reneeyu_canph4ori.txt' 
fileout  = 'reneeyu_canph4out.txt'
keypath  = 'reneeyu_canph2key.txt'
# keypath  = 'reneeyu_ph123key_oriquick.txt'
# keypath12  = 'reneeyu_ph123key2.txt'
# ---------------
# mydict12 = {}
# with codecs.open(keypath12,'r','utf-16') as f:
#    for line in f:
#       key = line[5]
#       val = line[0:2].rstrip()
#       print(key+val)
#       mydict12[key] = val
# f.close()

mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:  
          print(len(line))
          print(line[0])
          print(line[1])
          print(line[2])
          print(line[3])
          print(line[4])
          print(line[5])
          print(line[6])
          print(line[7])
          print(line[8])
#          print(line[9]) #endline
        key = line[7]
        val = line[0]+line[1]+line[2]+line[3]
#        print(key)
#        print(val) 
#        if len(val) != 4:
#           print(len)
#           print(val) 
# prevent duplicate key dict
        valdict = mydict.get(key,'??')
        if valdict == '??':
           mydict[key] = val
f.close()

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'kungfu 功夫' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   while line:
#       print(len(line))  #normal 11
#       print(line)
       if len(line) == 11:
          key1 = line[6]
          key2 = line[7]
          key3 = line[8]
          key4 = line[9] 
       if len(line) == 10:
#         print(len(line))
#         print(line[0])
#         print(line[1])
#         print(line[2])
#         print(line[3])
#         print(line[4])
#         print(line[5])
#         print(line[6])
#         print(line[7])
#         print(line[8])
#         print(line[9]) #endline
         key1 = line[5]
         key2 = line[6]
         key3 = line[7]
         key4 = line[8]
       
       if len(line) == 9:
         print(len(line)) 
         print(line) 
         key1 = line[4]
         key2 = line[5]
         key3 = line[6]
         key4 = line[7]
       if len(line) < 9:
         print(len(line)) 
         print(line) 
         print('** short'+line[9])
#       print(key1)
#       print(key2)
#       print(key3)
       val1 = mydict.get(key1, 'xx')
       val2 = mydict.get(key2, 'xx')
       val3 = mydict.get(key3, 'xx')
       val4 = mydict.get(key4, 'xx')
#       if val1 == 'xx' or val2 == 'xx' or val3 == 'xx': 
#          print(key1)
#          print(val1)
#          print(key2)
#          print(val2)
#          print(key3)
#          print(val3) 
#          print(line)
       val = val1.rstrip() + val2[0] + val3[0] + val4[0]
       if len(val) > 6:
          val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
          
          
       if len(val) == 5:
          val = val + ' ' 
       if len(val) == 4:
          val = val + '  ' 
       lineout = val + ' ' +key1+key2+key3+key4
#       if len(line) < 8:
#          print(lineout) 
       fo.write(lineout+'\r\n')
       cntout += 1
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
print('cnt=', cnt, ',cntout=', cntout)