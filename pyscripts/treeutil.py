#!/usr/bin/env python3

import optparse
import re
import numpy as np

class Node():
    def __init__(self,subs,data):
        self.subs = subs
        self.data = data

def construct_tree(curdepth,tabs,data):
    tabs = np.array(tabs)
    mindep = np.min(tabs.unique())
    mintabs = np.unique((l == mindep) * (np.arange(np.shape(l)[0])+1))
    if len(mintabs)<=1 : return Node(data=data)
    mintabs = mintabs[1:]
    

# re.findall(r'^ *\|* *[\\_-]* *',s)
def main():
    opt = optparse.OptionParser()
    (options,args) = opt.parse_args()

    for filename in args:
        with open(filename) as f: data = f.readlines()
        parseddata = []
        for l in data:
            tablen = len(re.findall(r'^ *\|* *[\\_-]* *',l)[0])
            parseddata.append(tablen)
        parseddata = np.array(parseddata)
        data = [i.rstrip()[j:] for i,j in zip(data,parseddata)]
        print(parseddata)
        print(data)


main()
