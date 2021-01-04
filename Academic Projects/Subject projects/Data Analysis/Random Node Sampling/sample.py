import random, pprint

adj_list={1:[2,4,3,8,9],
          2:[3,1,4,5,6,9,7],
          3:[4,2,1,7,5,9],
          4:[3,1,2,5,6,7,8,9],
          5:[4,6,2,9,7,3],
          6:[5,4,2,7,9],
          7:[3,4,6,8,9,5,2],
          8:[5,7,1,3,4,9],
          9:[1,2,3,4,5,6,7,8]}

n=1000
j=10
m=3

while j<=n:
    tmplist=random.sample(range(1,len(adj_list)+1),m)
    adj_list[j] = [tmplist[0]]
    for i in range(1,m):
        adj_list[j].append(tmplist[i])
    for i in range(0,m):
        adj_list[tmplist[i]].append(j)
    j=j+1



edgelist=[]

for i in range(1,len(adj_list)+1):
    for j in range(0,len(adj_list[i])):
        if i > adj_list[i][j]:
            edgelist.append([i,adj_list[i][j]])

print("\nEdge List:")
print(edgelist,"\n\nNumber of Edges:")
print(len(edgelist))

aaa=random.sample(adj_list.keys(),200)
print("\nRandom Nodes selected:")
print(aaa)

temp=[]
for i in range(len(aaa)):
    for j in range(len(aaa)):
        if [aaa[i],aaa[j]] in edgelist:
            temp.append([aaa[i],aaa[j]])
        elif [aaa[j],aaa[i]] in edgelist:
            temp.append(([aaa[j],aaa[i]]))

print("\nEdges formed from random node sample")
print(temp)


import xlsxwriter
wbk=xlsxwriter.Workbook('E:/Bals/Study plan/Lectures_Tutorials/Sem 2/DA II/.xlsx')
wks=wbk.add_worksheet('Sheet 1')

for i in range(0,len(temp)):
    wks.write(i,0,temp[i][0])
    wks.write(i,1,temp[i][1])
wbk.close()