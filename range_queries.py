#NIKOS KARIOTIS

import sys
import ast

current_index = 0
level = 0
node_array = []
result = []

class Node(): 
    def __init__(self, nonleaf ,node_id ,elements,level):
        self.nonleaf = nonleaf
        self.node_id = node_id
        self.elements = elements
        self.level = level

    
        
def reconstruct_Rtree(tree,queries):
    global current_index
    global level
    global node_array
    global result
    if(current_index < len(tree)): #condition so that recursion when this global variable reaches the end of the tree array will stop
        nonleaf = tree[current_index][0]

        if(nonleaf == 1): #construction for nonleaf nodes
            nodeID_arr = []
             
            for i in range(len(node_array)): # creates an array with all node_ids from nodes we have created so far
                node_id = node_array[i].node_id 
                nodeID_arr.append(node_id)
                
            nodes_in_same_level = 0
        
            for i in range(current_index,len(tree)):
                elements = tree[i][2][0][0] #from index we ve reached till the end of the tree array check the first node_id that this node-like element has child
                if(elements in nodeID_arr): #if first child node(using its node_id) is within the lower level then build the parent node in the upper level
                    node = Node(tree[i][0],tree[i][1],tree[i][2],level)
                    node_array.append(node)
                    nodes_in_same_level += 1 #in the end,total number of nodes in this particular level
            level += 1  
            
            current_index = current_index + nodes_in_same_level #in the next call of the function we have to read the remaining elements of the 2d array
            reconstruct_Rtree(tree,queries)
        
        else:
            while(nonleaf == 0): # while the first item of each element is zero
                node = Node(tree[current_index][0],tree[current_index][1],tree[current_index][2],level) #create a new leaf Node
                node_array.append(node) #and append it to an array
                current_index += 1 #increase the current index
                nonleaf = tree[current_index][0] #check if the next element of the array will refers to a leaf node  
                
            level += 1 #when we finished with the leaf Nodes ,level must be increased
            
            reconstruct_Rtree(tree,queries) #recursive call of the function
        
    else:
        root = node_array[-1].node_id #node_id of the root
        for i in range(len(queries)): #for each rectangle
            range_querie(root,queries[i]) #find nodes from the tree that they intersect with the rectangle
            print(str(i) + " " + "(" + str(len(result)) + ")" + ": " + str(result)[1:-1])
            result = []
        return 
   

   
def read_Rqueries(file):
    w_rectangles = []
    line = file.readline() #reads the first line of the Rqueries.txt
    while(line != ""): #while not EOF
        temp = line.split() #split the line using space as separator 
        x_low = float(temp[0]) # first string of each line refers to the minimum x value of each rectangle,convert string to float so we can compare the coords later 
        y_low = float(temp[1])
        x_high = float(temp[2])
        y_high = float(temp[3])
        w_rectangles.append([x_low,y_low,x_high,y_high]) #append each line of Rqueries in the form of floats in an array
        line = file.readline() #read the next line

    return w_rectangles #returns a 2d array with its element be an array of floats representing each rectangle

def range_querie(nodeID,querie):
    global node_array
    global result
    node = None
    
    for j in range(len(node_array)): #find the node of the tree using its node_id
        if(nodeID == node_array[j].node_id):
            node = node_array[j] 
            
    if(node.nonleaf == 1): #if node we found is nonleaf
        for i in range(len(node.elements)):
            mbr = node.elements[i][1] # take the mbr of its child node
            node_id = node.elements[i][0] #take the node_id of child node
            boolean = rectangle_overlap(mbr,querie) #check if rectangle and mbr of the child node intersect
            if(boolean == True): #if they do 
                range_querie(node_id,querie) #continue traversing the tree using as root the child node 
    if(node.nonleaf == 0): #if node we found is leaf
        for i in range(len(node.elements)):
            mbr = node.elements[i][1]
            node_id = node.elements[i][0]
            boolean = rectangle_overlap(mbr,querie)
            if(boolean == True): #if child node intersects with the rectangle 
                result.append(node_id) #return its id 
        return
    
def rectangle_overlap(mbr,querie):
    if((mbr[0] >= querie[2]) or (mbr[1] <= querie[0]) or (mbr[3] <= querie[1]) or (mbr[2] >= querie[3])):
        return False
    else:
        return True
    
def main(argv):
    tree = []
    file1 = open(argv[1] , "r") #first command line argument refers to Rtree.txt
    file2 = open(argv[2] , "r") #second command line argument refers to NNqueries.txt
    for l in file1:
        temp = ast.literal_eval(l) #splits a line that is string into substrings 
        tree.append(temp)          
        
    queries = read_Rqueries(file2) #converts the original file into a 2d array 
    reconstruct_Rtree(tree,queries) #builds node objects that represent a tree structure
        
    file1.close()
    file2.close()



if __name__ == "__main__":
    main(sys.argv)
