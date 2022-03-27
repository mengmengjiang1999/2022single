import random
import os

filepath_in = './data/data.in' #输入数据地址
filepath_ans = './data/data.ans' #答案地址
filepath_problem = './data/problem.md' #题面地址
filepath_problem_html = './data/problem.html' #题面地址
filepath_image = './images/dijkstra.png' #图片地址

filepath_exe = './algorithm/shortestpath/program/main' #可执行文件地址
filepath_code = './algorithm/shortestpath/program/dijkstra.cpp' #代码地址

def pre_compile():
    # 对程序进行预编译
    os.system('g++ -o '+filepath_exe+' '+filepath_code)
    pass

def del_files():
    os.system('rm '+filepath_exe)
    pass

def run():
    from algorithm.shortestpath.generator import N_min, N_max, gen_edges, gen_data, gen_problem

    N = random.randint(N_min,N_max)
    edges, S, T = gen_edges(N)
    data = gen_data(N, S, T, edges)
    problem = gen_problem(S, T)

    # 根据随机生成的结果来生成图片
    from dots.dots import generate_dot, generate_png
    filepath_dot = "./data/dijkstra.dot"
    with open(filepath_dot,"w") as file_dot:
        file_dot.write(generate_dot("dijkstra",edges))
    generate_png("./data/dijkstra.dot", filepath_image)
    os.system('rm ./data/dijkstra.dot')

    # 生成数据，运算，给出答案
    with open(filepath_in,"w") as file_in:
        file_in.write(data)
    os.system(filepath_exe +' < '+filepath_in+' > '+filepath_ans)

    # 写题面
    with open(filepath_problem, "w") as file_problem:
        file_problem.write(problem)

    # 转换成html
    os.system('pandoc --standalone --template  ./data/template.html '+ filepath_problem + ' -o ' + filepath_problem_html)

    return filepath_in, filepath_ans, filepath_problem_html, filepath_image

if __name__ == '__main__':
    pre_compile()
    run()