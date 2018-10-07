# -*- coding: utf-8 -*-
import logging
import math
import random
import re
import sys
import time
from time import sleep

from common import UnicodeStreamFilter, config, debug, screenshot
from common.auto_adb import auto_adb

logging.basicConfig(level='DEBUG')
adb = auto_adb()

STATES = {
    'MENU': 'menu',
    'SELECT': 'select',
    'PREP': 'preparation',
    'BATTLE': 'battle',
    'LOAD': 'loading',
    'END1': 'end1',
    'END2': 'end2',
}


def check_state(im):
    im_pixel = im.load()
    state = None
    if im_pixel[56, 105] == (199, 191, 191, 255):
        if im_pixel[113, 1243] == (75, 184, 203, 255):
            state = STATES['MENU']
        elif im_pixel[77, 370] == (255, 251, 230, 255):
            state = STATES['SELECT']
        elif im_pixel[357, 1289] == (22, 156, 215, 255):
            state = STATES['PREP']
        else:
            state = STATES['LOAD']
    else:
        state = STATES['BATTLE']

    return state


def onmenu(x):
    '''
    Selecting menu items (1-3)
    '''
    adb.run('shell input tap %d 1310' % (x * 250 - 50))
    logging.info('onmenu:touch:(%d, 1310)' % (x * 250 - 50))


def onselect():
    '''
    Selecting support users
    '''
    adb.run('shell input tap 420 1310')
    logging.info('onselect:touch:(420, 1310)')


onbattlestart = onselect


def onconfirm():
    adb.run('shell input tap 800 1230')
    logging.info('onconfirm:touch:(800, 1230)')


def tap(x, y):
    adb.run('shell input tap %d %d' % (x, y))
    logging.info('tap:touch:(%d, %d)' % (x, y))


def onskill(x):
    adb.run(
        'shell input swipe %(x)d 1720 %(x)d 1500 200' % {'x': 200 * x - 100})
    logging.info('onskill:swipe:use skill_%d' % x)


def main():
    #debug.dump_device_info()
    #screenshot.check_screenshot()

    while True:
        logging.info('Now attempting to get into battle phase')
        onmenu(1)
        time.sleep(6)
        onselect()
        time.sleep(0.3)
        onselect()
        logging.info('Get into battle')
        time.sleep(30)
        onskill(3)
        time.sleep(6.5)
        onskill(2)
        time.sleep(6.5)
        onskill(2)
        logging.info('Battle\'s over. Wait for next battle')
        time.sleep(12)
        for i in range(10):
            time.sleep(1)
            onselect()
        time.sleep(5)
        logging.info('27 s Sleeped, get into next loop')


def GWPhase2(finishSleepTime=6, firstWaitTime=28):
    onmenu(2)
    time.sleep(6)
    onselect()
    time.sleep(0.3)
    onselect()
    time.sleep(0.3)
    onconfirm()
    logging.info('Get into battle')
    time.sleep(firstWaitTime)
    onskill(4)
    time.sleep(7)
    onskill(4)
    time.sleep(7)
    onskill(3)
    time.sleep(7)
    onskill(3)
    time.sleep(7)
    onskill(2)
    time.sleep(7)
    onskill(2)
    time.sleep(12)
    for i in range(10):
        time.sleep(1)
        tap(800, 600)
    time.sleep(finishSleepTime)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        adb.run('kill-server')
        exit(0)
