#!/usr/bin/env python3

from urllib.parse import unquote
from data_processing import space_fill
import optparse
import pyperclip
import os, sys

def main():
    opt = optparse.OptionParser()
    opt.add_option('-r','--no-test',dest='no_test',default=False,action='store_true')
    opt.add_option('-o','--out-dir',dest='outdir',default='')
    opt.add_option('-s','--std',help='from stdin to stdout',default=False,
            dest='std',action='store_true')
    opt.add_option('-C','--from-clipboard',default=False,dest='from_clipboard',action='store_true',
            help='read from clipboard. only works with `-s` option')
    opt.add_option('-c','--to-clipboard',default=False,dest='to_clipboard',action='store_true',
            help='print output to clipboard. only works with `-s` option')
    (options,args) = opt.parse_args()

    data = args

    if options.std:
        # read
        if options.from_clipboard: data = pyperclip.paste()
        else: data = sys.stdin.readline().strip()
        data = unquote(data)

        # write
        if options.to_clipboard: pyperclip.copy(data)
        else: print(data)

        return 0

    if len(data) == 0:
        data = [i for i in os.listdir() if i.find('%')>=0]
        if len(data) == 0: return
    maxlen = max([len(i) for i in data])

    outputname = []
    for i in data:
        topn = os.path.split(i)[1]
        if not topn: topn = os.path.split(os.path.split(i)[0])[1] + '/'
        outputname.append(os.path.join(options.outdir,unquote(topn)))

    if options.no_test:
        for i in range(len(data)): os.system('mv "%s" "%s"'%(data[i],outputname[i]))
    else:
        for i in range(len(data)): print(space_fill(data[i],maxlen,'l'),'->',outputname[i])

main()
