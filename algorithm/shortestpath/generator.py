import random

'''
输入：

从标准输入读取数据。

M + 1 行。

第一行：N，M，S，T，点的个数，边的个数，开始结点，结束结点。有向图

接下来M行，每行三个整数u，v，w，表示起始点，终点，边权重。

输入数据保证w>0。'''


N_max=6
N_min=5
W_min=1
W_max=20


DENSITY = 0.45


# 注意：出题时编号从0开始
# N: 结点数
# 返回值：list[(int,int,int)], int, int
# 返回值表示边列表、起始点、终点
def gen_edges(N):
    # 随机生成边序列
    # edges := list[(int,int,int)]
    edges = []
    for i in range(1, N+1):
        for j in range(1, N+1):
            if i!=j:
                rnd = random.random()
                if rnd < DENSITY:
                    w = random.randint(W_min, W_max)
                    edges.append((i,j,w))
    S = 1
    T = N
    return edges, S, T

def gen_data(N, S, T, edges):
    M = len(edges)
    data = "%d %d %d %d\n" % (N, M, S, T)
    for edge in edges:
        data += "%d %d %d\n" % (edge[0], edge[1], edge[2])
    return data

    # with open(filepath_in, "w") as f:
    #     M = len(edges)
    #     # f.write(str(N)+' '+str(M)+' '+str(S)+' '+str(T)+'\n')
    #     for edge in edges:
    #         data = data + str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n'
            # f.write(str(edge[0])+' '+str(edge[1])+' '+str(edge[2])+'\n')

def gen_problem(S,T):
    problem = '''
### 求单源最短路

下图中，编号为 %d 的结点是起点，编号为 %d 是终点。请计算从起点到终点的最短路。

答案为一个正整数，如果从起点到终点不存在一条路径，请提交 2147483647。

    ''' % (S, T)
    return problem
