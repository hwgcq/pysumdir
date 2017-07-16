#! /bin/python
#2017-01-06 10:01	2017-01-03 21:19
#2016-09-18 22:39 
#2016-09-17 7:15 ... 2016-09-17 9:41 OK
#2016-09-17 1:44 hwg

path=r'C:\Users\user\Downloads\texlive'
fnext='.sha256'
from hashlib import sha512 as hf
import sys,os
def HashFile(filefullpath,block=2**20):
    f=open(filefullpath,'rb')
    m=hf()
    i=0
    while True:
        i+=1
        if i>=10:
            sys.stdout.write('.')
            i=0
        data=f.read(block)
        if not data:
            break
        m.update(data)
    f.close()
    return m

def GetDirSize(dir):
    from os.path import join, getsize
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size
    
def HashDir(Dir,File):
    from datetime import datetime
    tfmt='%Y-%m-%d %H:%M:%S'
    outfile = open(File,'w')
    t1=datetime.now()
    outfile.write('Begin '+ t1.strftime(tfmt)+ '\n')
    outfile.write(Dir + '\n')
    dirsize=GetDirSize(Dir)
    hashd=hf()
    dsize=0
    fnum=0
    for root, subdirs, files in os.walk(Dir):
        for file in files:
            filefullpath = os.path.join(root,file)
            print ('\n'+filefullpath,end="  ")
            filerelpath = os.path.relpath(filefullpath,Dir)
            fst=os.stat(filefullpath)
            str_fsize='{:,}'.format(fst.st_size)
            print(str_fsize,end="")
            dsize += fst.st_size
            fnum +=1
            ctime = datetime.fromtimestamp(fst.st_ctime)
            str_ctime=ctime.strftime(tfmt)
            mtime = datetime.fromtimestamp(fst.st_mtime)
            str_mtime=mtime.strftime(tfmt)
            hashf = HashFile(filefullpath)
            print(' %d' % (dsize/dirsize*100.0)+'%')
            hashd.update(hashf.digest())
            outfile.write(filerelpath + '\t' + str_fsize + '\t' + str_mtime + '\t'+ hashf.hexdigest() + '\n')
    str_total='Total %d Files(\t' % (fnum)+ '{:,}'.format(dsize) + '\t Bytes) \t'+hashd.hexdigest()
    print('\n\n'+str_total)
    outfile.write(str_total+'\n')
    t2=datetime.now()
    outfile.write('Finished ' + t2.strftime(tfmt) +  '\n')
    speed=dsize/((t2-t1).seconds+(t2-t1).microseconds/1e6)
    str_time='Total: ' + str(t2-t1) + '  %.1fMB/s\n' % (speed/2**20)
    print('\n'+str_time)
    outfile.write(str_time)
    outfile.close()
    print('Sum File: '+File)

HashDir(path,path + fnext)
