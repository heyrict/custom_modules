#!/usr/bin/env python
# coding: utf-8
import shutil
import os
import sys
from datetime import datetime


def restruct(file_list):
    while file_list:
        file = file_list.pop()
        if os.path.isdir(file):
            file_list.extend([os.path.join(file, i) for i in os.listdir(file)])
            continue

        ctime = datetime.utcfromtimestamp(os.path.getctime(file))
        directory = ctime.strftime("%Y-%m-%d")
        if not os.path.exists(directory):
            os.mkdir(directory)
        try:
            shutil.move(file, directory)
        except Exception as e:
            print(e)


def main():
    file_list = sys.argv[1:]
    restruct(file_list)


if __name__ == "__main__":
    main()
