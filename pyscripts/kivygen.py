#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
KivyGen
-------
Generate kivy-based python3 programs (beta)
"""

import os
import sys

#import optparse

HELPSTR = '''KivyGen Utils
Usage: kivygen [command] [project_name]
Commands:
    newproj: add a new kivy project with
            a main.py file and a kv interface.
'''

CMDS = ['newproj']

KV_TEMPLATE = '''#:kivy 1.10.0

<{0}Widget>:
    Label:
        text: "Hello World"
        center_x: root.width / 2
        center_y: root.height / 2
'''

MAINTEMPLATE = '''import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label


class {0}Widget(Widget):
    pass


class {0}App(App):
    def build(self):
        return {0}Widget()


if __name__ == '__main__':
    {0}App().run()
'''


def main():
    '''Main function'''
    if len(sys.argv) != 3:
        if (sys.argv[1] not in ['-h', '--help']):
            print("KivyGen: Invalid numbers of parameters")
            exit(1)
        else:
            print(HELPSTR)
            exit(0)

    command = sys.argv[1]
    projname = sys.argv[2]

    if command not in CMDS:
        print("KivyGen: Invalid command")
        exit(2)

    if os.path.exists(projname):
        print("KivyGen: Project {0} exists".format(projname))
        exit(3)

    if command == "newproj":
        os.mkdir(projname)
        projclassname = projname[0].upper() + projname[1:]
        with open(os.path.join(projname, "main.py"), 'w') as mainfile:
            print(MAINTEMPLATE.format(projclassname), file=mainfile)

        with open(os.path.join(projname, projname.lower() + ".kv"),
                  'w') as kvfile:
            print(KV_TEMPLATE.format(projclassname), file=kvfile)

    return 0


if __name__ == "__main__":
    main()
