#!/usr/bin/env python3

import random, optparse, sys
from data_processing import split_wrd

def calc(throw_dice):
    throw_dice = throw_dice.upper()
    comp = None
    if throw_dice.find('>=') >= 0: comp = 'ge'
    elif throw_dice.find('<=') >= 0: comp = 'le'
    elif throw_dice.find('<') >= 0: comp = 'lt'
    elif throw_dice.find('>') >= 0: comp = 'gt'

    if comp:
        temp = split_wrd(throw_dice,['>=','<=','>','<'])
        thresh = float(temp[1])
        throw_dice = temp[0]

    # throw dice
    if throw_dice.find('D') > 0:
        [nums, faces] = split_wrd(throw_dice, 'D')
    else: nums = 1; [faces] = split_wrd(throw_dice, 'D')

    nums = int(nums); faces = int(faces)
    result = [random.randint(1,faces) for i in range(nums)]
    yield 'Result: '+' '.join([str(i) for i in result])

    if comp:
        if comp == 'ge': compared_result = [i >= thresh for i in result]
        elif comp == 'le': compared_result = [i <= thresh for i in result]
        elif comp == 'gt': compared_result = [i > thresh for i in result]
        elif comp == 'lt': compared_result = [i < thresh for i in result]
        compared_result = sum(compared_result)

        if len(result) == 1:
            compared_result = 'Success!' if compared_result else 'Failed'
        yield '\tSuccess: '+str(compared_result)

    return


def main():
    opt = optparse.OptionParser()
    (options,args) = opt.parse_args()

    if len(args) == 0:
        # interactive input
        try:
            i = str(sys.stdin.readline())
            while i:
                print(i,end='\t')
                print('\n'.join(calc(i)))
                i = str(sys.stdin.readline())
        except KeyboardInterrupt: pass

    else:
        for i in args: 
            print(i,end='\t')
            print('\n'.join(calc(i)))

    return


main()
