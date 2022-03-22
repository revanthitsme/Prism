import numpy as np

n = 10
m = 3
adj = np.zeros((n,n))
count = np.zeros((n)) 


for i in range(m):
    adj[0][i+1] = 1
    adj[i+1][0] = 1
    count[0] = count[0]+1
    count[i+1] = count[i+1]+1

w = [1,0.4,0.9,0.7,0.5,0.6,0.2,0.4,0.3,0.1]

for i in range(1,n):
    s = np.sum(w*count)
    t = [[val/s,ind] for ind, val in enumerate(w*count)]
    t.sort(reverse = True)
    c =0
    for j in t:
        if i!= j[1] and adj[i][j[1]]==0:
            adj[i][j[1]] = 1
            adj[j[1]][i] = 1
            count[i] = count[i]+1
            count[j[1]] = count[j[1]]+1
            
        c = c +1
        if c>=m:
            break


print(adj)
print(count) 
