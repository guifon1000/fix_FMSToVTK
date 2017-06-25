#!/usr/bin/env python3
import subprocess as sp
import glob
import sys

# be sure of the path you give to your FMSToVTK executable !!
path = '/home/fon/OpenFOAM/fon-4.1/platforms/linux64GccDPInt32Opt/bin/FMSToVTK'


# How to call this ?
# python3 path/to/fixFMSToVTK.py your_fms_name
# WARNING ! DO NOT PUT THE .fms EXTENSION

def run_FMSToVTK(name):
    sp.call([path,name+'.fms',name])
    l = []
    for filename in glob.iglob('./**/*.vtp', recursive=True):
        l.append(filename)
    for li in l:
        f = open(li,'r').readlines()
        inPoints = False
        points = ''
        iStart=None
        iEnd=None
        for i,line in enumerate(f):
            if '<Points>' in line:
                inPoints=True
                iStart = i 
            if ('</Points>' in line) and (inPoints == True):
                inPoints=False
                iEnd = i
        for i in range(iStart,iEnd+1):
            points+=f[i].replace(')',' ').replace('(',' ')
        while '  ' in points:
            points = points.replace('  ',' ')
        fo = open(li,'w')
        for l in f[:iStart]:
            fo.write(l)
        fo.write(points)
        for l in f[iEnd+1:]:
            fo.write(l)
        fo.close() 

if __name__ == '__main__':
    sp.call(['rm','-r','fixed_'+sys.argv[1]])
    run_FMSToVTK(sys.argv[1])


