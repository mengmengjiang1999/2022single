#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAXN = 25;

int N, a[MAXN][MAXN], min_dist, p[MAXN];
bool visited[MAXN];

void dfs(int t, int current, int dist)
{
    if (dist >= min_dist) return;
    if (t >= N - 1)
    {
        min_dist = min(min_dist, dist + a[current][0]);
        // printf("0 ");
        // for (int i = 0; i < t; i++)
        //     printf("%d ", p[i]);
        // printf(":  %d\n", dist+a[current][0]);
        return;
    }
    for (int i = 1; i < N; i++)
        if (!visited[i])
        {
            visited[i] = true;
            p[t] = i;
            dfs(t + 1, i, dist + a[current][i]);
            visited[i] = false;
        }
}

int main()
{
    scanf("%d", &N);
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) scanf("%d", &a[i][j]);

    min_dist = 0x7fffffff;
    for (int i = 1; i < N; i++)
    {
        memset(visited, 0, sizeof(visited));
        p[0] = i;
        visited[i] = true;
        dfs(1, i, a[0][i]);
    }
    printf("%d\n", min_dist);
}
