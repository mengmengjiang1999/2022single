
import os

def generate_dot(picname, n, edges, type):
    s = "digraph %s {\n" % picname
    s += "layout=sfdp;\n"
    for i in range(1, n + 1):
        s += "%d;\n" % i
    for edge in edges:
        s += "%d->%d [label=%s];\n" % (edge[0], edge[1], edge[2])
    s += "}\n"
    return s

def generate_png(dotfilename,pngfilename):
    print("generate_png")
    os.system('dot -Tpng ' + dotfilename + ' -o ' + pngfilename)
    print("generate_png")
