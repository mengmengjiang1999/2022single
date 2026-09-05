
import subprocess

def generate_dot(picname, n, edges, type):
    s = "digraph %s {\n" % picname
    s += "edge [fontsize=11];\n"
    s += "layout=sfdp;\n"
    for i in range(1, n + 1):
        s += "%d;\n" % i
    for edge in edges:
        s += "%d->%d [label=%s];\n" % (edge[0], edge[1], edge[2])
    s += "}\n"
    return s

def generate_figure(dotfilename,filename):
    print("generate_figure")
    subprocess.run(
        ['dot', '-Gdpi=72', '-Tpng', dotfilename, '-o', filename],
        check=True,
    )
    print("generate_figure")
