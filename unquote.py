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

    outputname = []
    for i in data:
        topn = os.path.split(i)[1]
        if not topn: topn = os.path.split(os.path.split(i)[0])[1] + '/'
        outputname.append(options.outdir+unquote(topn))
    
    if options.no_test:
        for i in range(len(data)): os.system('mv "%s" "%s"'%(data[i],outputname[i]))
    else:
        for i in range(len(data)): print(space_fill(data[i],maxlen,'l'),'->',outputname[i])

main()
