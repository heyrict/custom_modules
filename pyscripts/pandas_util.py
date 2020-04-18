from data_processing import _in_list
import pandas as pd, numpy as np

def stacked_series_flatten(ser):
    '''
    flatten a series containing 1-D list-like items

    Parameters
    ----------
    ser : Series

    Returns
    -------
    sser : Series
        series item with all items flatten

    Example
    -------
    >>> import pandas as pd
    >>> ser = pd.Series([[1,2,3],[4,5,6],[7,8,9]], name='array')
    0    [1, 2, 3]
    1    [4, 5, 6]
    2    [7, 8, 9]
    Name: array, dtype: object

    >>> stacked_series_flatten(ser, name='array'))
    0    1
    1    4
    2    7
    3    2
    4    5
    5    8
    6    3
    7    6
    8    9
    Name: array, dtype: int64
    '''
    ser = ser.map(transfer_datatype)
    sser = ser[ser.map(type) != list]
    lser = ser[ser.map(type) == list]
    maxn = lser.map(len).max()
    if np.isnan(maxn): return sser
    for i in range(int(maxn)):
        sser = sser.append(lser.map(lambda x: x[i] if len(x)>i else None),ignore_index=True)
    return sser.dropna()

    
def stacked_series_map(ser,mapfunc='count',label=None,ascending=False):
    '''
    map every item in a 1-D stacked series
    
    Parameters
    ----------
    ser : Series or DataFrame
    mapfunc : str or function, default 'count'
        - 'count' : count every element in series
        - 'sum' : sum index of every element in series
        - function
    label : str, default None
        ignored if type of ser is Series.
        Do stacked_series_map on DataFrame's label column
    ascending : bool, default False

    See Also
    --------
    stacked_series_flatten

    Examples
    --------
    >>> t = pd.Series([1,[4,5,6],[6,5],[3,6],[]],name='array')
    >>> t
    0            1
    1    [4, 5, 6]
    2       [6, 5]
    3       [3, 6]
    4           []
    Name: array, dtype: object
    >>> stacked_series_map(t)
           count
    array       
    6.0        3
    5.0        2
    1.0        1
    3.0        1
    4.0        1
    >>> stacked_series_map(t,'sum')
           sum
    array     
    6.0     18
    5.0     11
    3.0      3
    4.0      1
    1.0      0

    mapfunc can also be a function applying to a Groupby object.
    >>> stacked_series_map(t,lambda x: x.max())
           result
    array        
    6.0       9.0
    5.0       6.0
    3.0       3.0
    4.0       1.0
    1.0       0.0
    '''
    ser.name = ser.name if ser.name else 'ser'
    df = stacked_series_flatten(ser).reset_index().rename_axis({'index':'result'}, axis=1)
    if type(mapfunc) == str:
        if mapfunc not in ['count','sum']: raise ValueError('mapfunc param not supported, please input count or sum')
        elif mapfunc == 'sum':
            dfp = df.groupby(ser.name).sum().rename_axis({'result':'sum'},axis=1).sort_values('sum',ascending=ascending)
        elif mapfunc == 'count':
            dfp = df.groupby(ser.name).count().rename_axis({'result':'count'},axis=1).sort_values('count',ascending=ascending)
    else:
        dfp = df.groupby(ser.name).apply(mapfunc).sort_values('result',ascending=ascending)
        del dfp[ser.name]
    if type(label) == type(None): return dfp
    else:
        if type(label) in [dict,pd.Series]: return dfp.rename_axis(label)
        elif type(label) == pd.DataFrame:
            if label.shape[1]!=2:
                raise ValueError('Length of DataFrame columns must be 2; %i detected'%label.shape[1])
            return dfp.rename_axis(dict(label.values))


def df_filter(df, column, condition, how='find', include=True):
    '''
    find all records satisfying given condition

    Parameters
    ----------
    df : DataFrame
    column : str
    condition : iterable or scalar
        list of filter rules
    how : str 
        - 'find' : call x.find(rule)
        - 're' : call re.find(rule,x)
        - 'fullmatch' : x == rule
    include : bool
        True if you want to include all found data in df
        False if you want to exclude all found data in df
    '''
    if not condition: return df
    if type(column)==str:
        condition = [condition] if type(condition) in (str,int,float) else list(condition)
        df.dropna(subset=[column],inplace=True)
        if include:
            df = df[df[column].map(lambda x: _in_list(x,condition,how=how))]
        else:
            df = df[df[column].map(lambda x: not _in_list(x,condition,how=how))]
        return df
    else:
        if include:
            dfs = pd.concat([df_filter(df,c,condition,how,include) for c in column],ignore_index=True)
            return dfs.drop_duplicates()
        else:
            dfs = df.copy()
            for c in column:
                dfs = df_filter(dfs,c,condition,how,include)
            return dfs.drop_duplicates()

