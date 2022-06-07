#include <iostream>
#include <string.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
using namespace std;

struct listNode{
    listNode* prev;
    listNode* next;
    int v;
    int len;
    listNode():prev(NULL),next(NULL),v(-1){}
};
class list{
public:
    listNode* header,*trailer;
    int _size;
    list():_size(0){
        header=new listNode;trailer=new listNode;
        header->next=trailer;
        trailer->prev=header;
    }
    void insert(int v,int len){
        //由于输入数据还比较好，这里没有必要检查是否有重边，从本题的情况来看即使有重边也不影响,因此不需要判断
        listNode* p=new listNode;
        p->v=v;
        p->len=len;
        p->next=header->next;header->next=p;
        p->next->prev=p;p->prev=header;
    }
    //题目里面没有删边的操作，因此可以不考虑删边的情况
    //由于时间和空间限制
    // 决定不用封装太好，遍历操作交给外部来执行
};

struct dis{
    int n,len;
};
class heap{
    dis h[500000+1];
    int size;
    void swap(dis& a,dis& b){
        dis t=a;a=b;b=t;
    }
    void siftdown(int i,int n){
        int t= i,flag=0;
        while(i*2<=n&&flag==0){
            if(h[i<<1].len<h[i].len){
                t=i<<1;
            }
            else{
                t=i;
            }
            if((i<<1|1)<=n&&h[i<<1|1].len<h[t].len){
                t=i<<1|1;
            }
            if(i==t){
                flag=1;
            }
            else{
                swap(h[i],h[t]);
                i=t;
            }
        }
    }
    void siftup(int i){
        int flag=0;
        if(i==1)return;
        while(i!=0&&flag==0){
            if(h[i>>1].len>h[i].len){
                swap(h[i],h[i>>1]);
            }
            else{
                flag=1;
            }
            i=i>>1;
        }
    }
public:
    heap():size(0){
        init();
    }
    void init(){
        for(int i=0;i<=500000;i++){
            h[i].len=0;h[i].n=0;
        }
    }
    void push(int n,int x){
        size++;
        h[size].len=x;h[size].n=n;
        siftup(size);
    }
    void shuchu(){
        printf("%d\n",h[1].n);
    }
    void pop(){
        swap(h[1],h[size]);
        size--;
        siftdown(1,size);
    }
    int top(){
        return h[1].n;
    }
    bool empty(){
        return size==0;
    }
};

list edges[500000];
int n,m;//记录边的个数和点的个数
int record[500000];//record 在d算法中记录节点是否已经被发现
//初始化为无穷大，这里实际上是1061109567
//如果没有边，那么认为边权是正无穷
/************************/

heap h;
bool vis[500000];

/***********************/
inline int min(int a,int b){
    return a<b?a:b;
}

char c[500000];
int main(){

    int s,t;
    scanf("%d%d",&n,&m);
    scanf("%d%d",&s,&t);
    s--, t--;
    for(int i=0;i<m;i++){
        int a,b,len;
        scanf("%d%d%d",&a,&b,&len);
        a--, b--;
        edges[a].insert(b,len);
    }
    //图信息输入完毕

    //ready to run d algorithm
    memset(record , 0x3f, sizeof(record));
    memset(vis, false, sizeof(vis));
    record[s]=0;
    h.push(s,record[s]);
    while (!h.empty()){
        int u=h.top();
        h.pop();
        if(vis[u])continue;
        vis[u]=true;
        for(listNode* p=edges[u].header->next;p->next;p=p->next){
            if(p->v > -1){
                if(record[p->v]>record[u]+p->len){
                    record[p->v]=record[u]+p->len;
                    h.push(p->v,record[p->v]);
                }
            }
        }
    }
    // for(int i=0;i<n;i++){
    //     if(record[i]!=1061109567)
    //         printf("%d ",record[i]);
    //     else printf("2147483647 ");
    // }printf("\n");
    if(record[t]!=1061109567)
            printf("%d",record[t]);
        else printf("2147483647");

    return 0;
}
