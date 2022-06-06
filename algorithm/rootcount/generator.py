import random
import os

from matplotlib.pyplot import close

'''
输入：

从标准输入读取数据。

M + 1 行。

第一行：N，M，S，T，点的个数，边的个数，开始结点，结束结点。有向图

接下来M行，每行三个整数u，v，w，表示起始点，终点，边权重。

输入数据保证w>0。'''

N_max=8
N_min=5
W_min=1
W_max=10

DENSITY = 0.5

# 注意：出题时编号从0开始
# N: 结点
# 返回值：list[(int,int,int)], int, int
# 返回值表示边列表、起始点、终点
def gen_edges(N):
    # 随机生成边序列
    edges = []
    for i in range(1,N+1,1):
        for j in range(1,N+1,1):
            if i!=j:
                rnd = random.random()
                if rnd < DENSITY:
                    w = random.randint(W_min, W_max)
                    edges.append((i,j,w))
    S = 1
    T = N
    return edges, S, T

def gen_data(N, S, T, edges):
    data = ''
    M = len(edges)
    data = data + str(N)+' '+str(M)+'\n'
    M = len(edges)
    for edge in edges:
        data = data + str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n'
    return data

def gen_problem(S,T):
    problem = '''
对于下图给出的一个边上不带权的有向连通图G，计算该图所有的根树的数目。

    '''
    return problem
