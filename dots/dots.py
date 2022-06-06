
import os

def generate_dot(picname, edges, type:int):
    s = "digraph "+picname+" {\n"
    s = s + "layout=sfdp;\n"
    for edge in edges:
        s = s + str(edge[0])+"->"+str(edge[1])+"[label=\""+str(edge[2])+"\"]"+"\n"
    s = s + "}\n"
    return s

def generate_png(dotfilename,pngfilename):
    print("generate_png")
    os.system('dot -Tpng ' + dotfilename + ' -o ' + pngfilename)
    print("generate_png")