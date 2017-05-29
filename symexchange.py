#!/usr/bin/env python3

import optparse
from data_processing import split_wrd

HALF = list('*,.?!()[];:\'\'\"\"')
FULL = list('×，。？！（）【】；：‘’“”')

def main():
    opt = optparse.OptionParser()
    opt.add_option('-u','--to-full',dest='to_full',action='store_true',default=False)
    (options,args) = opt.parse_args()

    for i in args:
        with open(i) as f:
            data = f.read()

        if options.to_full:
            data = split_wrd(data,HALF,FULL)
        else:
            data = split_wrd(data,FULL,HALF)

        with open(i,'w') as f:
            f.write(data)

main()
