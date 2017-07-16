#! /bin/python
#2017-01-03 21:19
#2016-09-18 22:39 
#2016-09-17 7:15 ... 2016-09-17 9:41 OK
#2016-09-17 1:44 hwg

path=r'D:\soft_inst'
import sys
    
def SumDir(dir,SumFile):
    import os
    from datetime import datetime
    tfmt='%Y-%m-%d %H:%M:%S'
    outfile = open(SumFile,'w')
    t1=datetime.now()
    outfile.write('Begin '+ t1.strftime(tfmt)+ '\n')
    outfile.write(dir + '\n')

    dsize=0
    fnum=0
    for root, subdirs, files in os.walk(dir):
        for file in files:
            filefullpath = os.path.join(root,file)
            filerelpath = os.path.relpath(filefullpath,dir)
            fst=os.stat(filefullpath)
            str_fsize='{:,}'.format(fst.st_size)
            dsize += fst.st_size
            fnum +=1
            mtime = datetime.fromtimestamp(fst.st_mtime)
            str_mtime=mtime.strftime(tfmt)
            outfile.write(filerelpath + '\t' + str_fsize + '\t' + str_mtime + '\n')
    str_total='Total %d Files(\t' % (fnum)+ '{:,}'.format(dsize) + '\t Bytes)'
    print('\n\n'+str_total)
    outfile.write(str_total+'\n')
    t2=datetime.now()
    speed=dsize/((t2-t1).seconds+(t2-t1).microseconds/1e6)
    outfile.write('Finished ' + t2.strftime(tfmt) +  '\n')
    str_time='Total: ' + str(t2-t1) + '  %.1fMB/s\n' % (speed/2**20)
    print('\n'+str_time)
    outfile.write(str_time)
    outfile.close()
    print('Sum File: '+SumFile)

SumDir(path,path+'.sum')
