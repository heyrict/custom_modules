#!/usr/bin/env python3
import os, sys
import json

filenames = sys.argv[1:]

if __name__ == "__main__":
    for filename in filenames:
        with open(filename) as f:
            d = json.load(f)
            c = d['cells']

        pathlessfilename = os.path.split(filename)[1]
        outputfilename = os.path.splitext(pathlessfilename)[0] + ".py"

        with open(outputfilename,'w') as f:
            for b in c:
                if b['cell_type'] == 'code':
                    f.write("".join(b['source']))
                elif b['cell_type'] == "markdown":
                    f.write("#Info: "+"#Info: ".join(b['source']))
                f.write("\n\n%s\n\n"%('#'+"-*"*30+'-#'))
