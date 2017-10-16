#!/usr/bin/env python3

import optparse,sys,os
from txtform import df_format_print, df_format_read
import pandas as pd, numpy as np
import pyperclip

class string():
    def __init__(self,*args,sep=' ',end='\n'):
        self.content = sep.join([str(i) for i in args])+end

    def read(self):
        return self.content

    def write(self,*args,sep=' ',end=''):
        self.content += sep.join([str(i) for i in args])+end


def main():
    opt = optparse.OptionParser()
    opt.add_option('-o','--output',dest='output',default=None,help='name of the outputfile.')
    opt.add_option('-c','--to-clipboard',dest='to_clipboard',action='store_true',default=False,help='redirect output to clipboard')
    opt.add_option('-C','--from-clipboard',dest='from_clipboard',action='store_true',default=False,help='redirect input from clipboard')
    opt.add_option('-v','--vim',dest='vim_edit',action='store_true',default=False,help='edit by vim')
    opt.add_option('-f','--from',dest='FROM',default=None)
    opt.add_option('-t','--to',dest='TO',default=None)
    opt.add_option('-r','--in-place',dest='in_place',default=False,action='store_true',help='replace the file')
    opt.add_option('-s','--squeeze',dest='squeeze',default=False,action='store_true',help='squeeze the form')
    opt.add_option('-n','--replace-na',dest='replace_na',default=False,action='store_true',help='replace na values by spaces (WARNING: THIS OPTION WILL MAKE OUTPUT UNCOMPATIBLE)')
    opt.add_option('-k','--kind',dest='kind',default='simple',help='select the output kind(`normal`/`simple`), default simple')
    opt.add_option('-a','--align',dest='align',default='c',help='align: [l,c,r]')
    opt.add_option('--uwidth',dest='uwidth',default=2,help='relative width of utf8 characters with latin characters')
    opt.add_option('--spcwidth',dest='spcwidth',default=1,help='relative width of space with latin characters')
    opt.add_option('--preset',dest='preset',default=None,help='presettings: [`xmind`]')
    opt.add_option('-O', '--order-by',dest='order_by',default=None)
    (options,args) = opt.parse_args()

    inp = args
    data = None
    mode = 'a'

    options.uwidth = float(options.uwidth)
    options.spcwidth = float(options.spcwidth)

    outputkind = options.kind[0]
    if outputkind not in 'sn': print('Error: outputkind %s not supported'%options.kind); return
    outputkind = 'simple' if outputkind == 's' else 'normal'

    if options.preset:
        if options.preset == 'xmind':
            options.uwidth = 2.5
            options.spcwidth = 0.605

    if options.in_place:
        mode = 'w'
        if options.vim_edit: options.output = '/tmp/excel2md_edit.md'
        elif len(inp)==0:
            print('Error: no file found for replace');return
        elif len(inp)>1:
            print('Error: More than one arguments passed');return
        if not options.output:
            options.output = inp[0]

    if len(inp) > 1: print('Error: More than one arguments passed'); return
    elif len(inp) == 0:
        instr = string()

        # get input
        if options.from_clipboard:
            instr.write(pyperclip.paste())
        elif options.vim_edit:
            try:
                os.system('touch /tmp/excel2md_edit.md')
                os.system('vim /tmp/excel2md_edit.md')
            except: print('Error: No vim editor available'); return;
            with open('/tmp/excel2md_edit.md','r') as f:
                instr.write(f.read())
            #os.remove('/tmp/excel2md_edit.md')
        else:
            r = str(sys.stdin.readline())
            while r:
                instr.write(r)
                r = str(sys.stdin.readline())

        try: data = df_format_read(instr.read(),replace_na=options.replace_na)
        except Exception as e: print(e); return

    else:
        inp = inp[0]
        FROM = options.FROM if options.FROM else (inp.split('.')[-1] if inp else None)
        # transform all data from excel file to DataFrame
        if FROM in ['xls','xlsx','excel']:
            data = pd.read_excel(inp)
        elif FROM in ['csv']:
            data = pd.read_csv(inp)
        else:
            with open(inp) as f:
                try: data = df_format_read(f.read(),replace_na=options.replace_na)
                except Exception as e: print(e);return

    data = data.applymap(str)

    # sort
    if options.order_by:
        asc = True
        if options.order_by[0] == '-':
            asc = False
            options.order_by = options.order_by[1:]
        elif options.order_by[0] == '+':
            options.order_by = options.order_by[1:]
        try: options.order_by = data.columns[int(options.order_by)]
        except: pass
        try:
            data = data.sort_values(options.order_by, ascending=asc)
        except Exception as e:
            print(e)
            exit(1)

    # output
    TO = options.TO if options.TO else (options.output.split('.')[-1]\
                                        if options.output else None)
    if TO==None:
        if options.to_clipboard == True:
            outstr = string()
            df_format_print(data,outstr,squeeze=options.squeeze,\
                    align=options.align,uwidth=options.uwidth,\
                    spcwidth=options.spcwidth,kind=outputkind)
            pyperclip.copy(outstr.read())
        else:
            df_format_print(data,squeeze=options.squeeze,\
                    align=options.align,uwidth=options.uwidth,\
                    spcwidth=options.spcwidth,kind=outputkind)
    else:
        if TO in ['xls','xlsx','excel']:
            data.to_excel(options.output,index=False)
        elif TO in ['csv']:
            if options.output: data.to_csv(options.output,index=False)
            else: data.to_csv(sys.stdout,index=False)
        else:
            with open(options.output,mode) as fo:
                df_format_print(data,file=fo,squeeze=options.squeeze,\
                        align=options.align,uwidth=options.uwidth,\
                        spcwidth=options.spcwidth,kind=outputkind)
    return 0


if __name__=='__main__':
    main()
