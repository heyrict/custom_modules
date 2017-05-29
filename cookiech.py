#!/usr/bin/env python3
import pyperclip

def main():
    data = pyperclip.paste()
    dl = []
    for line in data.split('\n'):
        dl.append({i.split('=')[0]:i.split('=')[1] for i in line.split(';')\
                if len(i.split('='))==2})
    pyperclip.copy(str(dl))

main()
