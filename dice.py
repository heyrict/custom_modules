#!/usr/bin/env python3

import random, optparse, sys
from data_processing import split_wrd

def calc(throw_dice):
    throw_dice = throw_dice.upper()
    comp = None
    if throw_dice.find('>=') >= 0 or throw_dice.find('GE') >= 0: comp = 'ge'
    elif throw_dice.find('<=') >= 0 or throw_dice.find('LE') >= 0: comp = 'le'
    elif throw_dice.find('<') >= 0 or throw_dice.find('LT') >= 0 or throw_dice.find('L') >= 0: comp = 'lt'
    elif throw_dice.find('>') >= 0 or throw_dice.find('GT') >= 0 or throw_dice.find('G') >= 0: comp = 'gt'

    if comp:
        temp = split_wrd(throw_dice,['>=','<=','>','<','GE','LE','LT','GT','G','L'])
        thresh = float(temp[1])
        throw_dice = temp[0]

    # throw dice
    if throw_dice.find('D') > 0:
        [nums, faces] = split_wrd(throw_dice, 'D')
    else: nums = 1; [faces] = split_wrd(throw_dice, 'D')

    nums = int(nums); faces = int(faces)
    result = [random.randint(1,faces) for i in range(nums)]
    yield '\tResult: '+' '.join([str(i) for i in result])

    if comp:
        if comp == 'ge': compared_result = [i >= thresh for i in result]
        elif comp == 'le': compared_result = [i <= thresh for i in result]
        elif comp == 'gt': compared_result = [i > thresh for i in result]
        elif comp == 'lt': compared_result = [i < thresh for i in result]
        compared_result = sum(compared_result)

        if len(result) == 1:
            compared_result = '\033[1;32mSuccess!\033[0m' if compared_result else '\033[1;31mFailed\033[0m'
            yield('\t'+compared_result)
        else: yield '\tSuccess: '+str(compared_result)

    return


def main():
    opt = optparse.OptionParser()
    (options,args) = opt.parse_args()

    if len(args) == 0:
        # interactive input
        try:
            i = str(sys.stdin.readline()).strip()
            while i:
                try: print('\n'.join(calc(i)))
                except Exception as e: print(e)
                i = str(sys.stdin.readline()).strip()
        except KeyboardInterrupt as e: pass

    else:
        for i in args: 
            print(i+'\n',end='')
            print('\n'.join(calc(i)))

    return


main()
