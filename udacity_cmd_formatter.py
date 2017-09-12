#!/usr/bin/env python3
import os, sys, re

curdir = os.curdir

def get_folders():
    folders = []
    for f in os.listdir():
        try:
            folders.extend([os.path.join(f,i)
                for i in os.listdir(f)])
        except: pass
    return folders

def match_file(regex, iterator):
    for i in iterator:
        if re.findall(regex, i):
            return i
    return


if __name__ == "__main__":
    folders = get_folders()
    for arg in sys.argv[1:]:
        fn, ext = os.path.splitext(arg)
        fn = re.sub(r'\d+ - ', '', fn)
        try:
            src = match_file(fn+"\.srt$", folders)
            os.system('mplayer -fs -sub "%s" "%s"'%(src, arg))
            print('mplayer -fs -sub "%s" "%s"'%(src, arg))
        except:
            print('File "%s" has no src file matched'%(arg))
