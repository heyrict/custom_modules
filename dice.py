#!/usr/bin/env python3

import optparse
import random
import sys

from data_processing import colorit, split_wrd


def dice_output_formatter(nums, faces, comp, thresh):
    result = [random.randint(1, faces) for i in range(nums)]

    if comp and thresh:
        if comp == 'ge':
            compared_result = [i >= thresh for i in result]
        elif comp == 'le':
            compared_result = [i <= thresh for i in result]
        elif comp == 'gt':
            compared_result = [i > thresh for i in result]
        elif comp == 'lt':
            compared_result = [i < thresh for i in result]
        compared_result = sum(compared_result)

        if len(result) == 1:
            compared_result = colorit('Success', 'green')\
                    if compared_result else colorit('Failed', 'red')
            return ('\t' + compared_result)
        else:
            return '\tSuccess: ' + str(compared_result)
    return '\tResult: ' + ' '.join([str(i) for i in result])


def dice_handler(throw_dice):
    comp = None
    thresh = None
    if throw_dice.find('>=') >= 0 or\
       throw_dice.find('GE') >= 0:
        comp = 'ge'
    elif throw_dice.find('<=') >= 0 or\
         throw_dice.find('LE') >= 0:
        comp = 'le'
    elif throw_dice.find('<') >= 0 or\
         throw_dice.find('LT') >= 0 or\
         throw_dice.find('L') >= 0:
        comp = 'lt'
    elif throw_dice.find('>') >= 0 or\
         throw_dice.find('GT') >= 0 or\
         throw_dice.find('G') >= 0:
        comp = 'gt'

    if comp:
        temp = split_wrd(
            throw_dice,
            ['>=', '<=', '>', '<', 'GE', 'LE', 'LT', 'GT', 'G', 'L'])
        thresh = float(temp[1])
        throw_dice = temp[0]

    [nums, faces] = throw_dice.split('D', 1)
    nums = int(nums)
    faces = int(faces)
    return dice_output_formatter(nums, faces, comp, thresh)


def unsqueeze_alnumlist(alnumlist):
    alnumlist = [i.split('-') for i in alnumlist.split(',')]
    out = []
    for i in alnumlist:
        if len(i) == 1:
            if i[0].isnumeric():
                out.append([int(i[0])])
            else:
                out.append([i[0]])
        else:
            out.append(list(range(int(i[0]), int(i[1]) + 1)))
    return sum(out, [])


def sequence_handler(throw_dice):
    [nums, sequence] = throw_dice.split('S', 1)
    if sequence.isnumeric():
        sequence_list = range(1, int(sequence) + 1)
    else:
        sequence_list = unsqueeze_alnumlist(sequence)
    return sequence_output_formatter(int(nums), sequence_list)


def sequence_output_formatter(nums, seq):
    if nums > len(seq):
        return colorit(
            f'\tThe sequence length ({len(seq)}) is below your sample number ({nums}).',
            'magenta')

    result = random.sample(seq, nums)
    return '\tResult: ' + ' '.join([str(i) for i in result])


def calc(throw_dice):
    throw_dice = throw_dice.upper()

    # throw dice
    if throw_dice.find('S') > 0:
        yield sequence_handler(throw_dice)
    elif throw_dice.find('S') == 0:
        yield sequence_handler("1" + throw_dice)
    elif throw_dice.find('D') > 0:
        yield dice_handler(throw_dice)
    elif throw_dice.find('D') == 0:
        yield dice_handler("1" + throw_dice)

    return


def main():
    opt = optparse.OptionParser()
    (options, args) = opt.parse_args()

    if len(args) == 0:
        # interactive input
        try:
            i = str(sys.stdin.readline()).strip()
            while i:
                try:
                    print('\n'.join(calc(i)))
                except:
                    print(colorit('\tCannot recognize the input.', 'magenta'))
                i = str(sys.stdin.readline()).strip()
        except KeyboardInterrupt as e:
            print('\b\b', end='')

    else:
        for i in args:
            print(i + '\n', end='')
            try:
                print('\n'.join(calc(i)))
            except:
                print(colorit('\tCannot recognize the input.', 'magenta'))

    return


if __name__ == "__main__":
    main()
