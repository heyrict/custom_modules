#!/usr/bin/env python3
"""
Convert between `.ipynb` files and `.py` files (beta).
"""
import json
import os
import re
import sys

METADATA = {
    'kernelspec': {
        'display_name': 'Python 3',
        'name': 'python3',
        'language': 'python'
    }
}

FILENAMES = sys.argv[1:]

if __name__ == "__main__":
    #opt = optparse.OptionParser()
    #opt.add_option('-r','--reverse',help="Convert .py back to .ipynb",
    #        action="store_true",dest="reverse",default=False)

    #(options,args) = opt.parse_args()

    for filename in FILENAMES:
        pathlessfilename = os.path.split(filename)[1]
        inputfile = os.path.splitext(pathlessfilename)

        if inputfile[1] == ".py":
            outputfilename = inputfile[0] + ".ipynb"

            with open(filename) as f:
                data = f.read()

            data_blockes = re.split(r"\n*#[-*]+#\n*", data)
            cells = []
            for i in data_blockes:
                lines = []
                i = i.split('\n')
                for j in range(len(i)):
                    if i[j].strip():
                        if j != len(i) - 1:
                            lines.append(i[j] + '\n')
                        else: lines.append(i[j])
                #lines = [j+'\n' for j in i.strip().split('\n') if j]
                if not lines:
                    continue

                if re.match("^#Info: ?|^#I: ?", lines[0]):  # Is info block
                    lines = [re.sub("^#Info: ?|^#I: ?", "", j) for j in lines]
                    cells.append({
                        'cell_type': 'markdown',
                        'metadata': {
                            'deletable': True,
                            'editable': True,
                            'colab_type': 'text'
                        },
                        'source': lines
                    })

                else:  # Is code block
                    outputs = []
                    stdoutputs = []
                    source = []
                    for j in lines:
                        if re.match("^#Data: ?|^#O: ?", j):
                            outputs.append(re.sub("^#Data: ?|^#O: ?", "", j))
                        if re.match("^#StdOut: ?|^#S: ?", j):
                            stdoutputs.append(re.sub("^#StdOut: ?|^#S: ?", "", j))
                        else:
                            source.append(j)
                    cells.append({
                        'cell_type': 'code',
                        'metadata': {
                            'deletable': True,
                            'editable': True,
                            'colab_type': 'code',
                            'cellView': 'both',
                            'collapsed': False
                        },
                        'execution_count': 0,
                        'outputs': [{
                            'output_type': 'stream',
                            'name': 'stdout',
                            'text': stdoutputs if stdoutputs else None,
                            'text/plain': outputs if outputs else None,
                        }],
                        'source': source
                    })

            obj = {
                'nbformat_minor': 1,
                'nbformat': 4,
                'metadata': METADATA,
                'cells': cells
            }
            with open(outputfilename, 'w') as f:
                json.dump(obj, f, indent=1)

        elif inputfile[1] == ".ipynb":
            outputfilename = inputfile[0] + ".py"
            with open(filename) as f:
                d = json.load(f)
                c = d['cells']

            with open(outputfilename, 'w') as f:
                for b in c:
                    if b['cell_type'] == 'code':
                        f.write("".join(b['source']))
                        for o in b['outputs']:
                            if 'text' in o.keys():
                                f.write("\n\n#StdOut: " +
                                        "#StdOut: ".join(o['text']))
                            elif 'data' in o.keys() and 'text/plain' in o['data']:
                                f.write("\n\n#Data: " +
                                        "#Data: ".join(o['data']['text/plain']))
                    elif b['cell_type'] == "markdown":
                        f.write("#Info: " + "#Info: ".join(b['source']))
                    f.write("\n\n%s\n\n" % ('#' + "-*" * 33 + '-#'))
