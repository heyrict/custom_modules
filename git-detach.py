#!/usr/bin/env python3
import os
import optparse

opt = optparse.OptionParser()
(options,args) = opt.parse_args()

os.system('git checkout --orphan temp %s'%args[0])
os.system('git commit -m %s'%args[1])
os.system('git rebase --onto temp %s master'%args[0])
os.system('git branch -D temp')
