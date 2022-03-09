
import os

def generate_dot(picname, edges):
    s = "digraph "+picname+" {\n"
    for edge in edges:
        s = s + str(edge[0])+"->"+str(edge[1])+"[label=\""+str(edge[2])+"\"]"+"\n"
    s = s + "}\n"
    return s

def generate_png(dotfilename,pngfilename):
    os.system('dot -Tpng ' + dotfilename + ' -o ' + pngfilename)