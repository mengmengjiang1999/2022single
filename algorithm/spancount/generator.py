import random

'''
输入：

从标准输入读取数据。

M + 1 行。

第一行：N，M，S，T，点的个数，边的个数，开始结点，结束结点。有向图

接下来M行，每行三个整数u，v，w，表示起始点，终点，边权重。

输入数据保证w>0。'''


N_max=5
N_min=4
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
    for i in range(1,N+1,1):
        for j in range(1,N+1):
            if i!=j:
                rnd = random.random()
                if rnd < DENSITY:
                    edges.append((i, j, "<<i>e</i><sub>%d</sub>>" % (len(edges) + 1)))
    e_exc = random.randint(1, len(edges))
    e_inc = random.randint(1, len(edges))
    return edges, e_exc, e_inc

def gen_data(N, e_exc, e_inc, edges):
    M = len(edges)
    data = "%d %d %d %d\n" % (N, M, e_exc, e_inc)
    for edge in edges:
        data += "%d %d\n" % (edge[0], edge[1])
    return data

def gen_problem(e_exc, e_inc):
    problem = '''
### 支撑树计数

对于下图给出的一个边上不带权的有向连通图 $G$，计算该图中：

1. 支撑树的数目。
2. 不含边 $e_%d$ 的支撑树的数目。
3. 必含边 $e_%d$ 的支撑树的数目。

三个答案之间用一个空格隔开。
    ''' % (e_exc, e_inc)
    return problem
