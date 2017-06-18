#!/usr/bin/env python3

import optparse
from data_processing import split_wrd, auto_newline

HALFFULL=[('*','×'),(',','，'),('.','。'),('.','．'),\
         ('?','？'),('!','！'),('(','（'),(')','）'),\
         ('[','【'),(']','】'),(';','；'),('\'','‘'),\
         ('\'','’'),('\"','“'),('\"','”'),]

def main():
    global HALFFULL
    opt = optparse.OptionParser()
    opt.set_usage(auto_newline('%%prog will replace the symbols in SBC case(full) to '\
            'DBC case(half) or the reverse(by using -u, --to-full option. '\
            '%%prog has a preset DBC cases of %s '\
            'and you can adapt it to your preferences by using '\
            '-a and -x options.'%[i[1] for i in HALFFULL]))
    opt.add_option('-u','--to-full',dest='to_full',action='store_true',default=False)
    opt.add_option('-x',dest='exclude',help='place `half` and `full` symbols '\
            'to exclude separated by a space',action='append',default=[])
    opt.add_option('-a',dest='include',help='place `half` and `full` symbols '\
            'to include separated by a space',action='append',default=[])
    opt.add_option('-s','--space',dest='space',help='add space after each replacement'\
            '(doesn\'t work if -u/--to-full is set',action='store_true',default=False)
    opt.add_option('-o','--only',dest='only',help='to contain only the given rules'\
            'separated by a space',action='append',default=[])
    (options,args) = opt.parse_args()

    options.include = [i.split(' ') for i in options.include]
    options.exclude = [i.split(' ') for i in options.exclude]
    options.only = [i.split(' ') for i in options.only]

    for l in [options.include, options.exclude, options.only]:
        if len(l) == 0: continue
        temp = [len(i) for i in l]
        if (max(temp) != min(temp)) | (max(temp) != 2):
            print('ERROR: the value of include/exclude/only is invalid')
            exit(1)

    if options.only:
        HALF = [i[0] + ' '*options.space for i in options.only]
        FULL = [i[1] for i in options.only]
    else:
        for i in options.exclude:
            try: HALFFULL.remove(i)
            except: print('WARNING:',i,'is not in preset cases')
        HALFFULL += options.include

        HALF = [i[0] + ' '*options.space for i in HALFFULL]
        FULL = [i[1] for i in HALFFULL]

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
