import codecs
import os
filepath = 'reneeyu.txt'  
fileout  = 'reneeyu_ibusout.txt'
fileoutr = 'reneeyu_rimeout.txt'
fileoutg = 'reneeyu_gcinout.txt'

#if os.path.exists(fileout):
#    os.remove(fileout)
#fo = open(fileout,'a+', encoding='utf-16') 
fo = open(fileout,'w+', newline='\n', encoding='utf-8') 
#if os.path.exists(fileoutr):
#    os.remove(fileoutr)
#fr = open(fileoutr,'a+', encoding='utf-16') 
fr = open(fileoutr,'w+', newline='\n', encoding='utf-8') 
fg = open(fileoutg,'w+', newline='\n', encoding='utf-8') 
lineout = 'kungfu>功夫>1' 
lineoutr = '功夫>kungfu>1' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   cntout1 = 0
   cntout2 = 0 
   cntout3 = 0
   cntout4 = 0 
   cnterr1 = 0
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   while line:
#       print(len(line))
#       print(line)
# ignore blank lines and first 2 lines /S Aa b c ...
       if len(line)<2 or line[0] == ' ' or line[0] == '/':
          cnterr1 += 1
          line = fp.readline()
          cnt += 1
          continue
       wordlist = line.split() 
#      print(wordlist[0])
# handled spc whitespace line
       if wordlist[0] == 'spc':
       #if line[0]=='s' and line[1]=='p' and line[2]=='c' and line[3]==' ':
          print(line)
          lineout = 'spc\t' + '　' + '\t1'
          lineoutr = '　' + 'spc\t' + '\t1'
       else:
          #wordlist = line.split()
          #print(wordlist[0],wordlist[1]) #last line must not be eof, else error list index out of range 
          lineout = wordlist[0] + '\t' + wordlist[1] + '\t' + str(500000-cntout1)
          lineoutr = wordlist[1] + '\t' + wordlist[0] + '\t' + str(500000-cntout1)
       fo.write(lineout+'\n')
       fr.write(lineoutr+'\n')
       fg.write(line)
       cntout1 += 1

       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
fr.close()
fg.close()
cntout = cntout1+cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout1=', cntout1, ',cnterr1=', cnterr1)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
#-----------------------------
print("***concat ./reneeRime/renee.dict_head.yaml, reneeyu_rimeout.txt to ./reneeRime/renee.dict.yaml")
filehead  = './reneeRime/renee.dict_head.yaml'
filerime = 'reneeyu_rimeout.txt'
filetxt  = './reneeRime/renee.dict.yaml'
import shutil
#import glob

filenames = [filehead, filerime]

#filenames = glob.glob("*.txt")  # or "file*.txt"
#with open(filetxt, "wb") as outfile:
with open(filetxt,'w+', newline='\n', encoding='utf-8') as outfile:
    for filename in filenames:
#        with open(filename, "rb") as infile:
         with open(filename,'r', newline='\n', encoding='utf-8') as infile:
             shutil.copyfileobj(infile, outfile)
#-----------------------------
print("***concat ./gcinRenee/renee_head.cin, reneeyu_gcinout.txt to ./gcinRenee/renee.cin")
fileheadg  = './gcinRenee/renee_head.cin'
fileg = 'reneeyu_gcinout.txt'
filegcin  = './gcinRenee/renee.cin'
filenames = [fileheadg, fileg]
with open(filegcin,'w+', newline='\n', encoding='utf-8') as outfile:
    for filename in filenames:
         with open(filename,'r', newline='\n', encoding='utf-8') as infile:
             shutil.copyfileobj(infile, outfile)
#----------------
'''
#filenames = [f'file{i}.txt' for i in range(1,368)]
with open(filetxt,'w+', newline='\n', encoding='utf-8') as outfile:
    for filename in filenames:
        with open(filename,'r', encoding='utf-8') as infile:
            contents = infile.read()
            outfile.write(contents)
'''
#----------------
import os
deploybat = "reneeRimeDeployDict.bat"
#deploybat = "C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe /deploy"
#print("starting ... ", deploybat)
os.chdir("./reneeRime/")
#os.system(r"C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe /deploy")
os.startfile(deploybat)
os.chdir("../")
#os.system(r"D:\xxx1\xxx2XMLnew\otr.bat")