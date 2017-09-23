#!/usr/bin/env python3
import os, sys
import optparse
import json, re

metadata = {'kernelspec': {'display_name': 'Python 3', 'name': 'python3', 'language': 'python'}}

filenames = sys.argv[1:]

if __name__ == "__main__":
    #opt = optparse.OptionParser()
    #opt.add_option('-r','--reverse',help="Convert .py back to .ipynb",
    #        action="store_true",dest="reverse",default=False)

    #(options,args) = opt.parse_args()

    for filename in filenames:
        pathlessfilename = os.path.split(filename)[1]
        inputfile= os.path.splitext(pathlessfilename)

        if inputfile[1] == ".py":
            outputfilename = inputfile[0] + ".ipynb"

            with open(filename) as f:
                data = f.read()

            data_blockes = re.split(r"\n*#[-*]+#\n*", data)
            cells = []
            for i in data_blockes:
                lines = [j+'\n' for j in i.strip().split('\n') if j]
                if not lines: continue

                if re.match("^#Info: ", lines[0]): # Is info block
                    lines = [re.sub("^#Info: ", "", j) for j in lines]
                    cells.append({'cell_type':'markdown',
                        'metadata':{'deletable':True, 'editable':True, 'colab_type':'text'},
                        'source':lines})

                else: # Is code block
                    outputs = []
                    source = []
                    for j in lines:
                        if re.match("^#Output: ", j):
                            outputs.append(re.sub("^#Output: ", "", j))
                        else: source.append(j)
                    cells.append({'cell_type':'code',
                        'metadata':{'deletable':True, 'editable':True, 'colab_type':'code',
                            'cellView': 'both','collapsed': False},
                        'execution_count': 0,
                        'outputs':[{'output_type': 'stream', 'name': 'stdout', 'text':outputs}],
                        'source':source})

            obj = {'nbformat_minor': 1, 'nbformat': 4, 'metadata':metadata, 'cells':cells}
            with open(outputfilename, 'w') as f:
                json.dump(obj, f, indent=1)

        elif inputfile[1] == ".ipynb":
            outputfilename = inputfile[0] + ".py"
            with open(filename) as f:
                d = json.load(f)
                c = d['cells']

            with open(outputfilename,'w') as f:
                for b in c:
                    if b['cell_type'] == 'code':
                        f.write("".join(b['source']))
                        for o in b['outputs']:
                            if 'text' in o.keys():
                                f.write("\n\n#Output: "+"#Output: ".join(o['text']))
                    elif b['cell_type'] == "markdown":
                        f.write("#Info: "+"#Info: ".join(b['source']))
                    f.write("\n\n%s\n\n"%('#'+"-*"*30+'-#'))
