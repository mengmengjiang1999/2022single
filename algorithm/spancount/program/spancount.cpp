#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAXN = 10;
const int MAXM = 20;

int N, M, e_exc, e_inc;
int edges[MAXM][2], edges_exclude[MAXM][2], edges_include[MAXM][2];

long long det(int n, long long a[][MAXN])
{
    if (n == 0) return 1;
    long long sign = 1, previous_pivot = 1;
    for (int i = 0; i < n - 1; i++)
    {
        int pivot = i;
        while (pivot < n && a[pivot][i] == 0) pivot++;
        if (pivot == n) return 0;
        if (pivot != i)
        {
            for (int j = 0; j < n; j++) swap(a[i][j], a[pivot][j]);
            sign = -sign;
        }
        for (int row = i + 1; row < n; row++)
            for (int col = i + 1; col < n; col++)
                a[row][col] = (a[row][col] * a[i][i] -
                               a[row][i] * a[i][col]) / previous_pivot;
        previous_pivot = a[i][i];
    }
    return sign * a[n - 1][n - 1];
}

long long span_count(int n, int m, int edges[][2])
{
    long long a[MAXN][MAXN];
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1; j++)
        {
            int s = 0;
            for (int k = 0; k < m; k ++)
            {
                // Contracting the required edge can turn parallel edges into
                // self-loops. Self-loops never belong to a spanning tree.
                if (edges[k][0] == edges[k][1]) continue;
                int x = 0, y = 0;
                if (i == edges[k][0]) x = 1;
                else if (i == edges[k][1]) x = -1;
                if (j == edges[k][0]) y = 1;
                else if (j == edges[k][1]) y = -1;
                s += x * y;
            }
            a[i][j] = s;
        }
    return det(n - 1, a);
}

int main()
{
    scanf("%d%d%d%d", &N, &M, &e_exc, &e_inc);
    e_exc--, e_inc--;
    for (int i = 0; i < M; i++)
    {
        scanf("%d%d", &edges[i][0], &edges[i][1]);
        edges[i][0]--, edges[i][1]--;
    }
    
    long long ans_all = span_count(N, M, edges);

    for (int i = 0, t = 0; i < M; i++)
        if (i != e_exc)
        {
            edges_exclude[t][0] = edges[i][0];
            edges_exclude[t][1] = edges[i][1];
            t++;
        }
    long long ans_exc = span_count(N, M - 1, edges_exclude);

    int map[MAXN];
    memset(map, -1, sizeof(map));
    map[edges[e_inc][0]] = map[edges[e_inc][1]] = 0;
    for (int i = 0, t = 1; i < N; i++)
        if (map[i] < 0) map[i] = t++;
    for (int i = 0, t = 0; i < M; i++)
        if (i != e_inc)
        {
            edges_include[t][0] = map[edges[i][0]];
            edges_include[t][1] = map[edges[i][1]];
            t++;
        }
    long long ans_inc = span_count(N - 1, M - 1, edges_include);
    
    printf("%lld %lld %lld\n", ans_all, ans_exc, ans_inc);
}
