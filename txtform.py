import sys, re
import pandas as pd, numpy as np
from data_processing import split_wrd, space_fill


def df_format_print(df,file=sys.stdout,index=False,align='c',squeeze=False,uwidth=2,spcwidth=1,kind="simple",margin=None):
    lengths = []
    if index: df = df.reset_index()
    collen = len(df.columns)

    delta = uwidth - 1

    # fill align
    align = list(align)
    if len(align) < collen:
        align += align[-1]*(collen - len(align))
    # lengths of columns
    lengths = df.columns.map(lambda x: int(len(str(x)) + delta*(len(x.encode('utf-8')) - len(x))//2))
    dfshap = df.copy()

    # lenths of values
    for c in range(len(dfshap.columns)):
        dfshap.iloc[:,c] = dfshap.iloc[:,c].map(lambda x: int(len(str(x)) + delta*(len(x.encode('utf-8')) - len(x))//2))

    if kind=="normal":
        if not margin: margin = 0
        lengths = np.max([lengths,dfshap.max()],axis=0)+margin
        print('+'+'+'.join(['-'*i for i in lengths])+'+',file=file)
        dcfl = [space_fill(df.columns[i],length=lengths[i],align=align[i],uwidth=uwidth,spcwidth=spcwidth) for i in range(collen)]
        print('|'+'|'.join(dcfl)+'|',file=file)
        print('+'+'+'.join(['='*i for i in lengths])+'+',file=file)

        ddsm = np.array([df.ix[:,c].map(lambda x: True if x in '|-' else False) for c in range(collen)])

        ddfl = [df.ix[:,c].map(lambda x: space_fill(x,lengths[c],align[c],uwidth=uwidth,spcwidth=spcwidth) if x not in '|-' else ' '*lengths[c]) for c in range(collen)]

        if squeeze: ddflout = '\n'.join(['|'+'|'.join(i)+'|' for i in pd.DataFrame(ddfl).T.values])
        #else: ddflout = ('\n+'+'+'.join(['-'*i for i in lengths])+'+\n')\
                #.join(['|'+'|'.join(i)+'|' for i in pd.DataFrame(ddfl).T.values])
        else:
            dfproc = pd.DataFrame(ddfl).T.values
            ddflout = ['|'+'|'.join(dfproc[0])+'|']
            for ind in range(1,len(df)):
                #ddflout.append('+'+'+'.join([(' ' if ddsm[j][ind] else '-')*i for i,j in zip(lengths,range(ddsm.shape[0]))])+'+')
                line = '|' if ddsm[0][ind] else '+'
                for i,j in zip(lengths,range(ddsm.shape[0]-1)):
                    line += (' ' if ddsm[j][ind] else '-')*i + ('|' if (ddsm[j][ind] and ddsm[j+1][ind]) else '+')
                line += (' ' if ddsm[j+1][ind] else '-')*lengths[-1] + ('|' if ddsm[j+1][ind] else '+')
                ddflout.append(line)
                ddflout.append('|'+'|'.join(dfproc[ind])+'|')
            ddflout = '\n'.join(ddflout)

        print(ddflout,file=file)
        print('+'+'+'.join(['-'*i for i in lengths])+'+',file=file)

    elif kind=="simple":
        if not margin: margin = 2
        lengths = np.max([lengths,dfshap.max()],axis=0)+margin
        print(' '.join(['-'*i for i in lengths]),file=file)
        dcfl = [space_fill(df.columns[i],length=lengths[i],align=align[i],uwidth=uwidth,spcwidth=spcwidth) for i in range(collen)]
        print(' '.join(dcfl),file=file)
        print(' '.join(['-'*i for i in lengths]),file=file)
        ddfl = [df.ix[:,c].map(lambda x: space_fill(x,lengths[c],align[c],uwidth=uwidth,spcwidth=spcwidth)) for c in range(collen)]

        if squeeze: ddflout = '\n'.join([' '.join(i) for i in pd.DataFrame(ddfl).T.values])
        else: ddflout = '\n\n'.join([' '.join(i) for i in pd.DataFrame(ddfl).T.values])

        print(ddflout,file=file)
        print('-'*(sum(lengths)+collen-1),file=file)


def df_format_read(string,replace_na=True):
    ss = [i for i in split_wrd(string,list('\n\r'),ignore_space=True) if not re.findall('^[-:=|+ ]+$',i)]
    try:
        columns = np.array([i.strip() for i in split_wrd(ss[0],'|')])
        data = pd.DataFrame([split_wrd(i,'|') for i in ss[1:]]).values
        data = np.array([['na' if type(i)==type(None) else ('-' if re.findall('^\s+$',i) else i.strip()) for i in j] for j in data])
        if len(columns) != data.shape[1] or len(columns) == 1:
            columns = np.array(split_wrd(ss[0],['  ','\t']))
            data = pd.DataFrame([split_wrd(i,['  ','\t'],ignore_space=True) for i in ss[1:]]).values
        data = np.array([[j if j not in ['nan','na','None'] else None for j in i] for i in data])

        # fill data
        if columns.shape[0] != data.shape[1]:
            cs = columns.shape[0]; ds = data.shape[1]
            if cs < ds:
                columns = np.hstack([columns]+[np.nan]*(ds-cs))
            else:
                data = np.hstack([data,[[np.nan]*(cs-ds)]*data.shape[0]])

        df = pd.DataFrame(data,columns=columns)
        if replace_na: df = df.fillna(' ')
        else: df = df.fillna('na')
        return df
    except Exception as e:
        print(e)
        raise ValueError('Data Passed Unrecognizable')


def df_split_line(df,token=';'):
    out = pd.DataFrame()
    for i in df.values:
        line = [j.split(token) for j in i]
        maxitemc = max([len(i) for i in line])
        oline = []
        for t in range(maxitemc):
            oline.append([k[t] if len(k) > t else None for k in line])
        out = pd.concat([out, pd.DataFrame(oline)], ignore_index=True)
    return out.fillna('-')
