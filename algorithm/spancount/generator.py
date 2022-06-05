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
# N: 结点数
# 返回值：list[(int,int,int)], int, int
# 返回值表示边列表、起始点、终点
def gen_edges(N):
    # 随机生成边序列
    # edges := list[(int,int,int)]
    edges = []
    for i in range(N):
        for j in range(N):
            if i!=j:
                rnd = random.random()
                if rnd < DENSITY:
                    w = random.randint(W_min, W_max)
                    edges.append((i,j,w))
    S = 0
    T = N-1
    return edges, S, T

def gen_data(N, S, T, edges):
    data = ''
    M = len(edges)
    data = data + str(N)+' '+str(M)+'\n'
    M = len(edges)
    for edge in edges:
        data = data + str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n'
    return data
    # with open(filepath_in, "w") as f:
    #     M = len(edges)
    #     # f.write(str(N)+' '+str(M)+' '+str(S)+' '+str(T)+'\n')
    #     for edge in edges:
    #         data = data + str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n'
            # f.write(str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n')

def gen_problem(S,T):
    problem = '''
### dijkstra算法求最短路

请使用dijkstra算法求最短路径 \n

下图中，编号为 '''+str(S)+''' 的结点是起点，编号为 '''+str(T)+''' 是终点。请计算从起点到终点的最短路。\n

答案为一个正整数，如果从起点到终点不存在一条路径，请提交2147483647。

<!-- ![dijkstra.png](/Users/chenzm/Projects/2022/2022single/images/dijkstra.png)  -->
    '''
    return problem
