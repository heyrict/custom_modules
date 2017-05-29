# coding: utf-8
import pandas as pd, numpy as np
import re
from data_processing import *
_section_dict = pd.read_csv('section_dict.csv')
_subsection_dict = pd.read_csv('subsection_dict.csv')
_illness_dict = pd.read_csv('illness_dict.csv')
def haodf_pat_ilns_filter(patfile, section=None, subsection=None, illness=None):
    '''
    given DataFrame containing 'pat_ilns' column, return filtered DataFrame.

    Parameters
    ----------
    patfile : DataFrame
    section : scarlar or iterable
        section number or a list of it
    subsection : scarlar or iterable
        subsection number or a list of it
    illness : str or iterable
        illness name or a list of it
    '''
    patfile.dropna(subset=['pat_ilns'],inplace=True)
    if type(illness) != type(None):
        illness = [illness] if type(illness) == str else list(illness)
        patfile = patfile[patfile['pat_ilns'].map(lambda x: x in illness)]
        return patfile
    if type(section) != type(None):
        section = [section] if type(section) in (str,int,float) else list(section)

        if type(subsection) != type(None) :
            subsection = [subsection] if type(subsection) in (str,int,float) else list(subsection)
            fsubsection = pd.DataFrame()

            for i, j in zip(section,subsection):
                tsubsection = _subsection_dict[(_subsection_dict['subsection_ix'].map(lambda x: x == j)) & (_subsection_dict['section_ix'].map(lambda x: x == i))]
                fsubsection = fsubsection.append(tsubsection,ignore_index=True)

            secnsubsec = (fsubsection['section_ix']*1000+fsubsection['subsection_ix']).values
            return haodf_pat_ilns_filter(patfile,illness=list(_illness_dict[_illness_dict['illness_ix'].map(lambda x: x in secnsubsec)]['illness_link']))
        else:
            subsection = _subsection_dict[_subsection_dict['section_ix'].map(lambda x: x in section)]
            return haodf_pat_ilns_filter(patfile, section=section, subsection=list(subsection['subsection_ix']))
                   
def haodf_groupby_count(patfile, column=None, head=10, asc=False, rename=None, plot=True, *plotargs, **plotkwargs):
    '''
    groupby one column and automatically rename index if data found in current directory,
    maybe plot

    Parameters
    ----------
    patfile : DataFrame or Series
    column : scalar, default None
        by which column to group
        must set if type of patfile is DataFrame
    head : integer, default 10
        number of head records to return / plot
    asc : bool, default False
    rename : True, None, Series, DataFrame or dict
        whether and how to rename index
    plot : bool
        whether to plot or return the results
    '''
    if type(patfile) == pd.DataFrame:
        if column == None: raise ValueError('column property not passed.')
        patfile = stacked_series_flatten(patfile[column])
    else: column = patfile.name
    sf = pd.DataFrame(patfile)
    sf['count'] = 1
    sf = sf.groupby(column).count().sort_values('count',ascending=asc).head(head)

    # rename
    if type(rename) == dict:
        sf = sf.rename_axis(rename)
    elif type(rename) == pd.DataFrame:
        if rename.shape[1] == 2:
            sf = sf.rename_axis(dict(rename.values))
        else: raise ValueError('DataFrame must have 2 columns, %s passed'%rename.shape[1])
    elif type(rename) == pd.Series:
        sf = sf.rename_axis(dict(rename))
    elif rename == True:
        try:
            sf = sf.rename_axis(dict(pd.read_csv('%s.csv'%column)[['code','name']].values))
        except Exception as e:
            print(e)
            pass
    elif rename == None:
        pass
    else: raise ValueError('type %s not supported for ``rename``'%type(rename))

    if plot: return sf.plot(*plotargs, **plotkwargs)
    else: return sf


def haodf_illness_name_to_ix(names, sets=['sect','subs','ilns'], how='find'):
    '''
    get illness ix by name

    Parameters
    ----------
    names : str or a list of str
        get name filtered with ``how`` method
    sets : str or iterable
        one or list of string in:
        - 'sect' : search section_dict
        - 'subs' : search subsection_dict
        - 'ilns' : search illness_dict
    how : str
        - 'find' : call x.find(rule)
        - 're' : call re.find(rule,x)
        - 'fullmatch' : x == rule
    '''
    if type(sets) == str: sets = [sets]

    if 'sect' in sets:
        sect = df_filter(_section_dict,'section_name',names,how)
    if 'subs' in sets:
        subs = df_filter(_subsection_dict,'subsection_name',names,how)
    if 'ilns' in sets:
        ilns = df_filter(_illness_dict,'illness_name',names,how)

    if len(sets) == 1:
        return eval(sets[0])
    else:
        return [eval(i) for i in sets]

def haodf_get_illness_from_subsection(df=None,section=None,subsection=None):
    if type(df) != type(None):
        secnsubsec = (df['section_ix']*1000+df['subsection_ix']).values
    elif type(section)!=None and type(subsection)!=None:
        secnsubsec = np.array(section)*1000+np.array(subsection)
    return _illness_dict[_illness_dict['illness_ix'].map(lambda x: x//1000 in secnsubsec)]
    
