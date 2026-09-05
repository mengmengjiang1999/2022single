import random
import subprocess
from pathlib import Path

filepath_pre_data = './../data/'
filepath_pre_in = './data/input/'
filepath_pre_answer = './data/answer/'
filepath_pre_problem = './data/problem/'
filepath_pre_html = './data/html/'
filepath_pre_dot = './data/dot/'
filepath_pre_algorithm = './algorithm/'
filepath_pre_image = './images/'

FILEPATH_EXE_SHORTESTPATH = './algorithm/shortestpath/program/main' #可执行文件地址
FILEPATH_CODE_SHORTESTPATH = './algorithm/shortestpath/program/dijkstra.cpp' #代码地址

FILEPATH_EXE_ROOTCOUNT = './algorithm/rootcount/program/main' #可执行文件地址
FILEPATH_CODE_ROOTCOUNT = './algorithm/rootcount/program/rootcount.cpp' #代码地址

FILEPATH_EXE_SPANCOUNT = './algorithm/spancount/program/main' #可执行文件地址
FILEPATH_CODE_SPANCOUNT = './algorithm/spancount/program/spancount.cpp' #代码地址

FILEPATH_EXE_TSP = './algorithm/tsp/program/main' #可执行文件地址
FILEPATH_CODE_TSP = './algorithm/tsp/program/tsp.cpp' #代码地址

FILEPATH_EXE = [FILEPATH_EXE_SHORTESTPATH,FILEPATH_EXE_TSP,FILEPATH_EXE_SPANCOUNT,FILEPATH_EXE_ROOTCOUNT]
FILEPATH_CODE = [FILEPATH_CODE_SHORTESTPATH,FILEPATH_CODE_TSP,FILEPATH_CODE_SPANCOUNT,FILEPATH_CODE_ROOTCOUNT]

def pre_compile():
    # 对程序进行预编译
    for executable, source in zip(FILEPATH_EXE, FILEPATH_CODE):
        subprocess.run(['g++', '-o', executable, source], check=True)

def del_files():
    for executable in FILEPATH_EXE:
        Path(executable).unlink(missing_ok=True)

# 无论数据类型是什么，都要返回边列表的形式
# 接口约定
def gen_edges():
    pass

def gen_input_files(type:int):
    if type==0:
        from algorithm.shortestpath.generator import N_min, N_max, gen_edges, gen_data, gen_problem

        # 生成数据并写入，运算，给出答案
        N = random.randint(N_min,N_max)
        edges, S, T = gen_edges(N)
        data = gen_data(N, S, T, edges)
        problem = gen_problem(S, T)

        return N,edges,data,problem
    elif type==1:
        from algorithm.tsp.generator import N_min, N_max, gen_edges, gen_data, gen_problem

        # 生成数据并写入，运算，给出答案
        N = random.randint(N_min,N_max)
        edges, S, T = gen_edges(N)
        data = gen_data(N, S, T, edges)
        problem = gen_problem(S, T)

        return N,edges,data,problem

    elif type==2:
        from algorithm.spancount.generator import N_min, N_max, gen_edges, gen_data, gen_problem

        # 生成数据并写入，运算，给出答案
        N = random.randint(N_min,N_max)
        edges, e_exc, e_inc = gen_edges(N)
        data = gen_data(N, e_exc, e_inc, edges)
        problem = gen_problem(e_exc, e_inc)

        return N,edges,data,problem

    elif type==3:
        from algorithm.rootcount.generator import N_min, N_max, gen_edges, gen_data, gen_problem

        # 生成数据并写入，运算，给出答案
        N = random.randint(N_min,N_max)
        R = random.randint(1, N)
        edges, e_exc, e_inc = gen_edges(N)
        data = gen_data(N, R, e_exc, e_inc, edges)
        problem = gen_problem(R, e_exc, e_inc)

        return N,edges,data,problem
    else:
        pass

def get_filepath_image(problem_sha):
    return filepath_pre_image + problem_sha + '.png' #图片地址

def run(problem_type:int,problem_sha:str,need_run:bool=False):
    # 对于所有题目的通用流程
    filepath_in = filepath_pre_in +  problem_sha + '.in' #输入数据地址
    filepath_ans = filepath_pre_answer + problem_sha + '.ans' #答案地址
    filepath_problem = filepath_pre_problem + problem_sha + '.md' #题面地址
    filepath_problem_html = filepath_pre_html + problem_sha + '.html' #题面地址
    filepath_image = get_filepath_image(problem_sha)

    print("run函数")

    # 如果不需要运行，那么只要返回路径
    if not need_run:
        return filepath_in, filepath_ans, filepath_problem_html, filepath_image

    print("生成新题目")
    print("题目类型",problem_type)

    for directory in (
        filepath_pre_in,
        filepath_pre_answer,
        filepath_pre_problem,
        filepath_pre_html,
        filepath_pre_dot,
        filepath_pre_image,
    ):
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # 如果需要真的生成新的题目，再生成
    # 这里是生成新数据的地方
    N,edges,data,problem = gen_input_files(problem_type)

    with open(filepath_in,"w") as file_in:
        file_in.write(data)
    # 执行
    with open(filepath_in, 'r') as file_in, open(filepath_ans, 'w') as file_ans:
        subprocess.run(
            [FILEPATH_EXE[problem_type]],
            stdin=file_in,
            stdout=file_ans,
            check=True,
        )

    with open(filepath_ans,"r") as file_ans:
        ans = file_ans.read().strip()
        print("新生成的题目答案是",ans)

    # 根据随机生成的结果来生成图片
    from dots.dots import generate_dot, generate_figure
    filepath_dot = filepath_pre_dot + problem_sha + '.dot'
    with open(filepath_dot,"w") as file_dot:
        file_dot.write(generate_dot("pic",N,edges,problem_type))
    generate_figure(filepath_dot, filepath_image)

    print("filepath-problem",filepath_problem)
    print("filepath-image",filepath_image)
    # os.system('rm '+filepath_dot)

    # 写题面
    with open(filepath_problem, "w") as file_problem:
        file_problem.write(problem)

    # 转换成html
    subprocess.run(
        [
            'pandoc',
            '--standalone',
            '--template',
            './data/template.html',
            filepath_problem,
            '-o',
            filepath_problem_html,
        ],
        check=True,
    )

    return filepath_in, filepath_ans, filepath_problem_html, filepath_image

if __name__ == '__main__':
    pre_compile()
    run(0,"233")
