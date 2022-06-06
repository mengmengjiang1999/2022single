#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAXN = 10;
const int MAXM = 20;

int N, M, e_exc, e_inc;
int edges[MAXN][2], edges_exclude[MAXN][2], edges_include[MAXN][2];

int det(int n, double a[][MAXN])
{
    double ans = 1;
    for (int i = 0; i < n; i++)
    {
        if (a[i][i] == 0) ans *= -1;
        for (int j = i; j < n; j++)
            if (a[j][i] != 0)
            {
	            for (int k = 0; k < n; k++) swap(a[i][k], a[j][k]);
                break;
            }
        if (a[i][i] == 0) return 0;
        for (int j = i + 1; j < n; j++)
            if (a[j][i] != 0)
            {
                double x = a[j][i] / a[i][i];
                for (int k = i; k < n; k++) a[j][k] -= a[i][k] * x;
            }
    }
    for (int i = 0; i < n; i++) ans *= a[i][i];
    return (int)ans;
}

int span_count(int n, int m, int edges[][2])
{
    double a[MAXN][MAXN];
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1; j++)
        {
            int s = 0;
            for (int k = 0; k < m; k ++)
            {
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
    
    int ans_all = span_count(N, M, edges);

    for (int i = 0, t = 0; i < M; i++)
        if (i != e_exc)
        {
            edges_exclude[t][0] = edges[i][0];
            edges_exclude[t][1] = edges[i][1];
            t++;
        }
    int ans_exc = span_count(N, M - 1, edges_exclude);

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
    int ans_inc = span_count(N - 1, M - 1, edges_include);
    
    printf("%d\n%d\n%d\n", ans_all, ans_exc, ans_inc);
}
