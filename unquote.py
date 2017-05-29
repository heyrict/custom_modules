#!/usr/bin/env python3

from urllib.parse import unquote
from data_processing import space_fill
import optparse
import os

def main():
    opt = optparse.OptionParser()
    opt.add_option('-r','--no-test',dest='no_test',default=False,action='store_true')
    opt.add_option('-o','--out-dir',dest='outdir',default='.')
    (options,args) = opt.parse_args()

    data = args
    options.outdir = options.outdir if options.outdir[-1] == '/' else options.outdir + '/'

    if len(data) == 0:
        data = [i for i in os.listdir() if i.find('%')>=0]
        if len(data) == 0: return
    maxlen = max([len(i) for i in data])
    
    if options.no_test:
        for i in data: os.system('mv "%s" "%s"'%(i,options.outdir+unquote(i)))
    else:
        for i in data: print(space_fill(i,maxlen,'l'),'->',unquote(i))

main()
