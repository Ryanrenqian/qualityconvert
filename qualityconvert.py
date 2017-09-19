###################################################################
# File Name: qualityconvert.py
# Author: renqian
# mail: renqian@yucebio.com
# Created Time: Tue 19 Sep 2017 03:52:26 PM CST
#=============================================================
#!/usr/bin/env python3

import os
from multiprocessing import Pool
from optparse import OptionParser
import gzip
def parseCommand():
    usage = "\n\twe talk this later"
    parser = OptionParser(usage = usage, version = "v1")
    parser.add_option("-r", "--read", dest = "read",
            action = "append",
            help = "file name of read file, <requried>, if contain 2 or more reads, use --read r1.fq.gz --read r2.fq.gz --read r3.gz ...")
    parser.add_option("-q","--quality",dest="quality",
            default='S',type=str,
            help='Sanger: phred+33,value=S\nIllumina 1.3+: Phred+64,value=I\nIllumina 1.5+: Phred+64,value=J\nIllumina 1.8+: Phread+33,value=L')
    parser.add_option("-a",'--aim',dest="aim",
            default='L',type=str,
            help='Sanger: phred+33,value=S\nIllumina 1.3+: Phred+64,value=I\nIllumina 1.5+: Phred+64,value=J\nIllumina 1.8+: Phread+33,value=L')
    return parser.parse_args()

def PhredToChar(phred,step):
    return chr(phred+step)
def CharToPhred(char,step):
    return ord(char)-step
def linechange(line,step1,step2):
    return(''.join([PhredToChar(j,step=step2) for j in [CharToPhred(i,step1) for i in line]])+'\n')

def qulitychange(infile,step1,step2):
    if infile==None:
        raise TypeError
    with gzip.open(infile,'rb') as f:
        with gzip.open(infile.rstrip('.gz')+'convert.gz','wb')as o:
            for i,line in enumerate(f.readlines()):
                if (i+1)%4==0:
                    line=linechange(line.decode(),step1,step2).encode()
                o.write(line)
                
import sys
if __name__=='__main__':
    (options, args) = parseCommand()
    reads = options.read
    P = Pool(processes = len(reads))
    step={'S':33,'L':33,'I':64,'J':64}
    step1=step.get(options.quality,None)
    step2=step.get(options.aim,None)
    if step1 ==None or step2==None:
        print ('Wrong quality value')
        sys.exit()
    param=[(i,step1,step2)   for i in reads]
    print(param)
    Process=P.starmap(qulitychange,param)

