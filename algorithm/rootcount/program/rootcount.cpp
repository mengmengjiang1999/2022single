#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
using namespace std;

const int MAXN = 10;
const int MAXM = 20;

int N, M, R, e_exc, e_inc;
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

long long root_count(int n, int m, int r, int edges[][2])
{
    int t = 0;
    long long a[MAXN][MAXN];
    int p[MAXN];
    for (int i = 0; i < n; i++)
        if (i != r) p[t++] = i;

    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1; j++)
        {
            int s = 0;
            for (int k = 0; k < m; k ++)
            {
                int x = 0, y = 0;
                if (p[i] == edges[k][1]) x = -1;
                if (p[j] == edges[k][0]) y = 1;
                else if (p[j] == edges[k][1]) y = -1;
                s += x * y;
            }
            a[i][j] = s;
        }
    return det(n - 1, a);
}

int main()
{
    scanf("%d%d%d%d%d", &N, &M, &R, &e_exc, &e_inc);
    R--, e_exc--, e_inc--;
    for (int i = 0; i < M; i++)
    {
        scanf("%d%d", &edges[i][0], &edges[i][1]);
        edges[i][0]--, edges[i][1]--;
    }
    
    long long ans_all = root_count(N, M, R, edges);

    for (int i = 0, t = 0; i < M; i++)
        if (i != e_exc)
        {
            edges_exclude[t][0] = edges[i][0];
            edges_exclude[t][1] = edges[i][1];
            t++;
        }
    long long ans_exc = root_count(N, M - 1, R, edges_exclude);

    long long ans_inc = 0;
    // The root of an outward arborescence has no incoming edge.
    if (edges[e_inc][1] != R)
    {
        int m = 0;
        for (int i = 0; i < M; i++)
            if (i == e_inc || edges[i][1] != edges[e_inc][1])
            {
                edges_include[m][0] = edges[i][0];
                edges_include[m][1] = edges[i][1];
                m++;
            }
        ans_inc = root_count(N, m, R, edges_include);
    }
    
    printf("%lld %lld %lld\n", ans_all, ans_exc, ans_inc);
}
