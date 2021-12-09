#deleting the old input file
import os
import time
import math
import heapq
#start_time = time.time()
try:
	os.remove("output.txt")
	print("Output File Removed!")
except:
	print("No existing output file")

#reading the file
#print("Reading input file")
with open('input39.txt') as f:
    lines = f.read()
lines = lines.split('\n')

#getting the inputs
algorithm = lines[0]
size = [int(i) for i in lines[1].split(' ')]
start = lines[2]
end = lines[3]
n = int(lines[4]) #number of nodes in the graph

#move agent by the code
def move(pos,i):
	global size
	if i==1:
		pos[0] = pos[0]+1
	elif i==2:
		pos[0] = pos[0]-1
	elif i==3:
		pos[1] = pos[1]+1
	elif i==4:
		pos[1] = pos[1]-1
	elif i==5:
		pos[2] = pos[2]+1
	elif i==6:
		pos[2] = pos[2]-1
	elif i==7:
		pos[0] = pos[0]+1
		pos[1] = pos[1]+1
	elif i==8:
		pos[0] = pos[0]+1
		pos[1] = pos[1]-1
	elif i==9:
		pos[0] = pos[0]-1
		pos[1] = pos[1]+1
	elif i==10:
		pos[0] = pos[0]-1
		pos[1] = pos[1]-1
	elif i==11:
		pos[0] = pos[0]+1
		pos[2] = pos[2]+1
	elif i==12:
		pos[0] = pos[0]+1
		pos[2] = pos[2]-1
	elif i==13:
		pos[0] = pos[0]-1
		pos[2] = pos[2]+1
	elif i==14:
		pos[0] = pos[0]-1
		pos[2] = pos[2]-1
	elif i==15:
		pos[1] = pos[1]+1
		pos[2] = pos[2]+1
	elif i==16:
		pos[1] = pos[1]+1
		pos[2] = pos[2]-1
	elif i==17:
		pos[1] = pos[1]-1
		pos[2] = pos[2]+1
	elif i==18:
		pos[1] = pos[1]-1
		pos[2] = pos[2]-1
	if 0<=pos[0]<size[0]:
		if 0<=pos[1]<size[1]:
			if 0<=pos[2]<size[2]:
				return pos
	return None

#to make the position of the agent hashable - array is not hashable with dictionary
def arrayToString(arr):
	arr = [str(i) for i in arr]
	return ' '.join(arr)
def stringToArray(str):
	arr = [int(i) for i in str.split(' ')]
	return arr



#build the graph 
def buildGraph(lines):
	#print("building Graph")
	adjList = {}
	global n
	for i in range(5,5+n):
		temp = [int(j) for j in lines[i].split(' ')]
		pos = [temp[0], temp[1], temp[2]]
		node = arrayToString(pos)
		temp = temp[3:]
		#print(temp)
		for j in temp:
			#CHECK OMG
			cur = []
			cur[:] = list(pos) 
			newpos = move(cur,j)
			#print(newpos, pos)
			if newpos:
				newposNode = arrayToString(newpos)
			if newpos:
				try:
					adjList[node].append(newposNode)
				except:
					adjList[node] = [newposNode]
	#print(adjList)
	return adjList

graph=buildGraph(lines)
#(graph)
def dist(a,b):
	a = stringToArray(a)
	b = stringToArray(b)
	return math.floor(math.sqrt((10*(a[0]-b[0]))**2+(10*(a[1]-b[1]))**2+(10*(a[2]-b[2]))**2))

parent = {}
def shortestPath_BFS(start, end, graph):
	global parent
	frontier = []
	heapq.heappush(frontier,(0,start,0))
	priority = 0
	parent[start]  = (None,0)
	explored_pos = set()
	explored_pos.add(start)	
	while True:
		#print(parent)
		#print(frontier)
		if frontier == []:
			return "FAIL"
		curPriority, curNode,curTotalCost = heapq.heappop(frontier)
		if curNode == end:
			return curTotalCost
		#print(graph[curNode])
		for i in graph.get(curNode, []):
			#print("here")
			if i not in explored_pos:
				#print("here")
				explored_pos.add(i)
				priority+=1
				parent[i] = (curNode,1)
				heapq.heappush(frontier,(priority,i,curTotalCost+1)) 

def shortestPath_UCS(start,end,graph):
	global parent
	#print("starting")
	frontier = []
	#node:(parent,totalcost)
	parent = {start:(None,0)}
	#totalcost,node
	heapq.heappush(frontier,(0,start))
	explored_pos = set()
	cur_frontier = {start:0}
	#start_time_ucs = time.time()
	while True:
		if frontier == []:
			return "FAIL"
		curTotalCost, curNode = heapq.heappop(frontier)
		cur_frontier.pop(curNode)
		if curNode == end:
			return curTotalCost

		explored_pos.add(curNode)

		for i in graph.get(curNode, []):
			#print(i)
			#start_time_ucs = time.time()
			newCurCost = dist(curNode,i)
			newTotalCost = curTotalCost+newCurCost
			if i not in explored_pos and i not in cur_frontier:
				heapq.heappush(frontier,(newTotalCost,i))
				parent[i] = (curNode,newCurCost)
				cur_frontier[i]=newTotalCost
			elif i in cur_frontier:
				#print(cur_frontier)
				if cur_frontier[i] > newTotalCost:
					cur_frontier[i]=newTotalCost
					parent[i] = (curNode,newCurCost)
					for temp in range(len(frontier)):
						if frontier[temp][1]==i:
							frontier[temp] = (newTotalCost,i)
					heapq.heapify(frontier)


def shortestPath_A(start,end,graph):
	global parent
	#print("starting")
	frontier = []
	#node:(parent,totalcost)
	parent = {start:(None,0)}
	#totalcost,node
	heapq.heappush(frontier,(dist(start,end),0,start))
	explored_pos = set()
	#start_time_ucs = time.time()
	while True:
		if frontier == []:
			return "FAIL"
		curHeuristic, curTotalCost, curNode = heapq.heappop(frontier)
		if curNode == end:
			return curTotalCost
		for i in graph.get(curNode, []):
			#print(i)
			#start_time_ucs = time.time()
			if i not in explored_pos:
				explored_pos.add(curNode)
				newCurCost = dist(curNode,i)
				newHeuristic = dist(i,end) #euclidean distance
				newEstimate = newCurCost+newHeuristic+ curTotalCost
				parent[i] = (curNode, newCurCost)
				heapq.heappush(frontier, (newEstimate, curTotalCost+newCurCost, i))


if algorithm=="BFS":
	#print(parent)
	sumCost = shortestPath_BFS(start,end,graph)
elif algorithm=="UCS":
	#start_time_ucs = time.time()
	sumCost = shortestPath_UCS(start,end,graph)
	#print("--- %s seconds ---" % (time.time() - start_time_ucs))
elif algorithm=="A*":
	sumCost = shortestPath_A(start,end,graph)

f = open("output.txt", "w")
if sumCost!="FAIL":
	cur = end 
	path = []
	cost = []
	while cur!=None:
		cur_parent,cur_cost = parent[cur]
		path.append(cur)
		cur = cur_parent
		cost.append(cur_cost)
	path = path[::-1]
	cost = cost[::-1]
	f.write(str(sumCost))
	f.write('\n')
	f.write(str(len(path)))
	f.write('\n')
	#print('COST',cost)
	for i in range(len(cost)):
		f.write(path[i])
		f.write(' ')
		f.write(str(cost[i]))
		f.write('\n')
else:
	f.write(sumCost)
f.close()
#print("--- %s seconds ---" % (time.time() - start_time))
