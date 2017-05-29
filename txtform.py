import sys, re
import pandas as pd, numpy as np
from data_processing import split_wrd

def _space_fill(string,length,align='c'):
    '''
    fill spaces to a certain length.

    Parameters
    ----------
    string : str
    length : int
    align : char
        - `c` : centered
        - 'l' : left-aligned
        - 'r' : right-aligned
    '''
    string = str(string)
    strlen = (len(string.encode('utf-8')) + len(string))//2
    if length < strlen: length = strlen
    if align[0] == 'c':
        leftspc = (length-strlen)//2
        rightspc = length-strlen-leftspc
    elif align[0] == 'l':
        leftspc = 0
        rightspc = length-strlen
    elif align[0] == 'r':
        rightspc = 0
        leftspc = length-strlen
    else:
        raise ValueError('align not in [`c`,`l`,`r`]')
    return ' '*leftspc+string+' '*rightspc

    
def df_format_print(df,file=sys.stdout,index=False,align='c',squeeze=False):
    lengths = []
    if index: df = df.reset_index()
    collen = len(df.columns)

    # fill align
    align = list(align)
    if len(align) < collen:
        align += align[-1]*(collen - len(align))
    # lengths of columns
    lengths = df.columns.map(lambda x: (len(str(x).encode('utf-8'))+len(str(x)))//2)
    dfshap = df.copy()

    # lenths of values
    for c in range(len(dfshap.columns)):
        dfshap.iloc[:,c] = dfshap.iloc[:,c].map(lambda x: (len(str(x).encode('utf-8'))+len(str(x)))//2)
    lengths = np.max([lengths,dfshap.max()],axis=0)+2
    print(' '.join(['-'*i for i in lengths]),file=file)
    dcfl = [_space_fill(df.columns[i],length=lengths[i],align=align[i]) for i in range(collen)]
    print(' '.join(dcfl),file=file)
    print(' '.join(['-'*i for i in lengths]),file=file)
    ddfl = [df.ix[:,c].map(lambda x: _space_fill(x,lengths[c],align[c])) for c in range(collen)]

    if squeeze: ddfl = '\n'.join([' '.join(i) for i in pd.DataFrame(ddfl).T.values])
    else: ddfl = '\n\n'.join([' '.join(i) for i in pd.DataFrame(ddfl).T.values])

    print(ddfl,file=file)
    print('-'*(sum(lengths)+collen-1),file=file)


def df_format_read(string,replace_na=True):
    ss = [i for i in split_wrd(string,list('\n\r'),ignore_space=True) if not re.findall('^[- ]+$',i)]
    try:
        data = pd.DataFrame([split_wrd(i,['  ','\t'],ignore_space=True) for i in ss[1:]]).values
        columns = np.array(split_wrd(ss[0],[' ','\t']))
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

