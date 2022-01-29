#NIKOS KARIOTIS

import sys
import ast
import math

current_index = 0
level = 0
node_array = []
k = 0
node_ids = []

class PriorityQueue(object): #priority queue implementation
    def __init__(self): #initialize queue 
        self.queue = []
    
    def empty(self): # for checking if the queue is empty 
        return len(self.queue) == 0
  
    def put(self, data): #add a new element in the queue
        self.queue.append(data)
  

    def pop(self): #delete the smallest element from the queue 
        try:
            minimum = self.queue[0][1]
            index = 0
            for i in range(len(self.queue)):
                if (self.queue[i][1] < minimum):
                    minimum = self.queue[i][1]
                    index = i
            item = self.queue[index]
            del self.queue[index]
            return item
        except IndexError:
            print()
            exit()

class Node():
    def __init__(self, nonleaf ,node_id ,elements,level):
        self.nonleaf = nonleaf
        self.node_id = node_id
        self.elements = elements
        self.level = level

    
        
def reconstruct_Rtree(tree,q_points): #same as part 2
    global current_index
    global level
    global node_array
    global result
    global node_ids
    if(current_index < len(tree)):
        nonleaf = tree[current_index][0]

        if(nonleaf == 1):
            nodeID_arr = []
             
            for i in range(len(node_array)):
                node_id = node_array[i].node_id
                nodeID_arr.append(node_id)
                
            nodes_in_same_level = 0
        
            for i in range(current_index,len(tree)):
                elements = tree[i][2][0][0]
                
                if(elements in nodeID_arr):
                    node = Node(tree[i][0],tree[i][1],tree[i][2],level)
                    node_array.append(node)
                    nodes_in_same_level += 1
            level += 1
            
            current_index = current_index + nodes_in_same_level
            reconstruct_Rtree(tree,q_points)
        
        else:
            while(nonleaf == 0):
                node = Node(tree[current_index][0],tree[current_index][1],tree[current_index][2],level)
                node_array.append(node)
                current_index += 1
                nonleaf = tree[current_index][0]
                
            level += 1
            reconstruct_Rtree(tree,q_points)
        
    else:
        for i in range(len(node_array)):
            node_ids.append(node_array[i].node_id)
        
        root = node_array[-1].node_id
        for i in range(len(q_points)): #now it finds  neighbors of a point 
            result = BF_NN_search(q_points[i],root)
            print(str(i) + ":" + " " +str(result)[1:-1])
            
        return 


def BF_NN_search(point,nodeID):
    neighbors = []
    q = PriorityQueue(); #initialize an empty queue every time
    node = None
    counter = 0
    for j in range(len(node_array)):
        if(nodeID == node_array[j].node_id): #finds the node by id 
            node = node_array[j]
            
    for i in range(len(node.elements)):
        distance = calculateDistance(point,node.elements[i][1]) # for each child node ,calculates its distance from the point
        node_id = node.elements[i][0] 
        q.put([node_id,distance]) # insert pair of node_id and distance into the priority queue

    while(counter < k): # we need to find k neighbors not only one
        n = getNext(point,q)
        neighbors.append(n[0])
        counter +=1
        
    return neighbors
    
def getNext(point,q):
    global node_ids
    
    node = None
    while(not q.empty()):
        n = q.pop() #deletes the element with the smallest distance from the queue
        
        if(n[0] not in node_ids): #if node appears in the elements of a leaf node
            return n

        else: 
            for i in range(len(node_array)):
                if(n[0] == node_array[i].node_id):
                    node = node_array[i] #find the node by its name
                
            if(node.nonleaf == 1): 
                for j in range(len(node.elements)):
                    #print(node.elements[j][1])
                    distance = calculateDistance(point,node.elements[j][1])
                    node_id = node.elements[j][0]
                    q.put([node_id,distance])

            if(node.nonleaf == 0):
                #print(node.elements[j][1])
                for j in range(len(node.elements)):
                    distance = calculateDistance(point,node.elements[j][1])
                    node_id = node.elements[j][0]
                    q.put([node_id,distance])
    
        
        
def calculateDistance(point,mbr_arr):#calculates distance of between a point and a MBR
    dx = 0.0
    dy = 0.0
    
    if(point[0] < mbr_arr[0]):
        dx = mbr_arr[0] - point[0]
    if(point[0] > mbr_arr[1]):
        dx = point[0] - mbr_arr[1]
    if(point[1] < mbr_arr[2]):
        dy = mbr_arr[2] - point[1]
    if(point[1] > mbr_arr[3]):
        dy = point[1] - mbr_arr[3]
    distance = math.sqrt(dx*dx + dy*dy)
    
    return distance


    
def read_NNqueries(file):
    q_points = []
    line = file.readline() 
    while(line != ""): #check for EOF
        temp = line.split() #split using space as separator
        x = float(temp[0]) #convert string to float
        y = float(temp[1])
        q_points.append([x,y]) #append the point in the form of array into an array
        line = file.readline() #read next line of the file
         
    return q_points #returns a 2d array that contains all points 


def main(argv):
    tree = []
    global k
    file1 = open(argv[1] , "r") #Rtree.txt
    file2 = open(argv[2] , "r") #NNqueries.txt
    k = int(argv[3]) #number of closest neighbors wanted
    for l in file1:
        temp = ast.literal_eval(l)
        tree.append(temp) 
        
    q_points = read_NNqueries(file2) #read q points from file and returns an array with them 
    reconstruct_Rtree(tree,q_points) #reconstructs Rtree and finds k closest neighbors(nodes from the tree) for each q point
    file1.close()
    file2.close()



if __name__ == "__main__":
    main(sys.argv)
