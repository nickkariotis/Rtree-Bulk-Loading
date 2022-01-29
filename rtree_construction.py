#NIKOS KARIOTIS

import math
import sys

_DIVISORS = [180.0 / 2 ** n for n in range(32)]

file3 = open("Rtree.txt" , "w") 
level = 0
tree = []
nonleaf = 0
node_id = 0
root = 0

coords = []

def find_coords(file): 
    points = []
    boolean = True
    l = file.readline() #read a line of offsets.txt
    tmp = l.replace("\n","").split(",")
    num = tmp[0]
    start = tmp[1]
    end = tmp[2]
    while(boolean): # a while loop which breaks when we reach EOF 
        values =object_create(int(start),int(end)) #returns an array that contains all the coords that are grouped by offset of each line in offsets.txt
        #for each line we read from offsets.txt we push a new element in the end of the array,this element is an array with two values
        #first value represents the unique id of a rectangle,second value is the array that returned above and represents the coords that form the object
        points.append([int(num),values]) 
        l = file.readline() #read the next line of offsets.txt
        if(l != ""): 
            tmp = l.replace("\n","").split(",") #replace the "\n" in the end of the line with empty string,split the line using comma as separator
            num = tmp[0] #split creates an array of 3 strings,first string refers to id
            start = tmp[1] #second string refers to start offset
            end = tmp[2] #third string refers to end offset
        else:
            boolean = False #indicates EOF
        
    return points 

        
def object_create(start,end): #fuction that iterrates through coords array and returns a sub_array depending on the parameters(startOffset,endOffset) given by
                                     #a single line of offsets.txt
        obj = []                     
        for i in range(start,end):   #from startOffset to endOffset 
            row = coords[i].replace("\n","") #take a xy pair from coords_array
            pair = row.split(",") #split it 
            for j in pair: 
                obj.append(float(j)) #convert x,y string to float and push both of them in an array
                
        return obj


def calculate_MBR(points):
    mbr_arr = []
    mbrs = []
    for row in points:
        key = row[0] #id is the first element of each points[i]
        min_x = 1000000
        min_y = 1000000
        max_x = -1000000
        max_y = -1000000
        values = row[1] #set of coords is the second element of each points[i]
        length = len(values)
        for i in range(length): #from zero to length(set_of_coords)-1 
            if(i % 2 == 0): #because each set_of_coords array has the form of x,y,x,y... modulo works as a hashing function 
                if(values[i] < min_x): #simple min and max algorithms to find min,max x
                    min_x = values[i]
                if(values[i] > max_x):
                    max_x = values[i]
            else:
                if(values[i] < min_y): #same as above,this time calculates min,max y
                    min_y = values[i]
                if(values[i] > max_y):
                    max_y = values[i]   
        mbrs = [min_x,max_x,min_y,max_y] #mbr for each rectangle
        mbr_arr.append([key,mbrs]) #append id and mbr of each rectangle to an array 
        
    return mbr_arr
 


def interleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        print('Usage: interleave_latlng(float, float)')
        raise ValueError("Supplied arguments must be of type float!")

    if (lng > 180):
        x = (lng % 180) + 180.0
    elif (lng < -180):
        x = (-((-lng) % 180)) + 180.0
    else:
        x = lng + 180.0
    if (lat > 90):
        y = (lat % 90) + 90.0
    elif (lat < -90):
        y = (-((-lat) % 90)) + 90.0
    else:
        y = lat + 90.0

    morton_code = ""
    for dx in _DIVISORS:
        digit = 0
        if (y >= dx):
            digit |= 2
            y -= dx
        if (x >= dx):
            digit |= 1
            x -= dx
        morton_code += str(digit)

    return morton_code    


def calculate_z(mbr): #function that finds z-order for each rectangle using its mbr
    z = ""
    for row in mbr: #iterates through mbr_2d_array
        values = row[1] #take the set_of_coords of each element
        x_centre = (values[0] + values[1])/2 #find the average of min_x and max_x
        y_centre = (values[2] + values[3])/2 #same for y
        z = interleave_latlng(y_centre,x_centre) #call of the function that we were told to use for calculating z
        row.append(z) #[id,mbr,z] is the new form of each element of mbr_2d_array
        
    return mbr

def mergeSort(myList):
   
    if(len(myList) <= 1):
        return myList
    else:
        mid = (len(myList))//2 #middle of the array
        myList1 = mergeSort(myList[mid:]) #recursive call of merge-sort
        myList2 = mergeSort(myList[:mid])
        
        return merge(myList1,myList2)

    
def merge(left,right):
    output = []
    i = 0
    j = 0
    while((i < len(left)) and (j < len(right))):
        if(left[i][2] <= right[j][2]):
            output.append(left[i])
            i += 1
        elif(left[i][2] > right[j][2]):
            output.append(right[j])
            j += 1
    while(i < len(left)):#remaining items 
        output.append(left[i])
        i += 1
    while(j < len(right)):#same
        output.append(right[j])
        j += 1

        
    return output


def sort_mbr(unsorted_mbr):
    sorted_mbr = mergeSort(unsorted_mbr) #sorts the array by z-values
    for row in sorted_mbr:
        del row[-1]   #removes z-value from each element of the 2d array
        
    return sorted_mbr


def calculate_node_MBR(array): #calculate the total MBR of a Node object 
    mbrs = []
    min_x = 1000000
    min_y = 1000000
    max_x = -1000000
    max_y = -1000000
    
    for values in array:
        if(values[0] < min_x):
            min_x = values[0]
        if(values[1] > max_x):
            max_x = values[1]
        if(values[2] < min_y):
            min_y = values[2]
        if(values[3] > max_y):
            max_y = values[3]   
        
    mbr_res = [min_x,max_x,min_y,max_y]
       
    return mbr_res

def find_lvl0_mbrs(array): #calculate the mbr of a single leaf node
    mbrs_only = []
    for row in array:
        mbrs_only.append(row[1]) #array is in the form of [id,MBR] so the mbrs_only contains MBRs without the node_ids

    result = calculate_node_MBR(mbrs_only) # call the fuction that calculates the mbr of the node

    return result


class Node(): #defines a node object
    
    def __init__(self ,node_id , level ,elements):
        self.node_id = node_id 
        self.level = level
        self.elements = elements
        
def construct_Rtree(mbrs , max_cap , min_cap):
    global nonleaf
    global node_id
    global root
    global level
    global tree
    child_nodes = []
    start = 0
    end = max_cap
    number_of_nodes = math.ceil(len(mbrs)/max_cap) #calculate number of nodes per level
    if(number_of_nodes == 1): #we reached the root 
        root += 1

    if(nonleaf == 1): #here nonleaf Nodes are created

        if(root == 1): #end of recursion happens here
            
            node = Node(node_id,level,[]) #one Node is needed to represent the root Node
            for i in range(len(mbrs)): 
                node.elements.append([mbrs[i][0],mbrs[i][1]]) #append to the elements of root Node the ids and Mbrs from the lower level
            tree.append([nonleaf,node])
            print(str(number_of_nodes) + " node at level " + str(level)) #print 1 Node at level we reached to 
            
            for i in range(len(tree)):
                nonleaf = tree[i][0] 
                node_id = tree[i][1].node_id
                elems = tree[i][1].elements
                file3.write("[" + str(nonleaf)+ "," + str(node_id)+ "," + str(elems) + "]" + "\n") #write to the output file each element of tree_array
            return
       
        else: #non-root level
           
            for i in range(number_of_nodes): #it is the same procedure that we follow for the leaf-nodes
                mbr_list = []
                node = Node(node_id,level,[])
                for j in range(start,end):
                    mbr_list.append(mbrs[j][1])
                    node.elements.append([mbrs[j][0],mbrs[j][1]])
                node_id += 1
                start = end
                end += 20
                if((end > len(mbrs)) and (start < len(mbrs))):
                    split = len(mbrs) - min_cap
                    new_start = (20 - split) 
                    del node.elements[-new_start:]
                    del mbr_list[-new_start:]
                    start = split
                    end = len(mbrs)
                mbr = calculate_node_MBR(mbr_list)
                child_nodes.append([node.node_id,mbr])
                tree.append([nonleaf,node])         
            print(str(len(child_nodes)) + " nodes at level " + str(level))
            level += 1
            construct_Rtree(child_nodes , max_cap , min_cap) #recursive call to build the upper levels
           
    if(nonleaf == 0): #fuction begins from here(level 0) where the nodes are leafs
        for i in range(number_of_nodes): #loop for number_of_nodes times
            mbr_list = []
            node = Node(node_id,level,[]) #creates a new object Node
            for j in range(start,end): #from 0 to 20,from 20 to 40(fill a single node with 20 elements)
                node.elements.append(mbrs[j]) #for each Node append to the field that represents its data,elements in the form of [id,MBR] 
                mbr_list.append(mbrs[j])      #it will be used to find the MBR of all the elements we pass in a single node
            node_id += 1 #increase node_id by 1 so that every Node has a unique id
            start = end #refresh bounds so that the next Node will take the next 20 elements
            end += max_cap
            if((end > len(mbrs)) and (start < len(mbrs))): #if the upper bound surpassed the length of the mbr_length we have to split the elements so that the last one has at least 8 elements
                    split = len(mbrs) - min_cap #find how many elements must have the next to last Node
                    new_start = (max_cap - split) + 1 #find how many elements i have to remove form the next to last Node
                    del node.elements[-new_start:-1] #delete
                    del mbr_list[-new_start:-1]      #delete
                    start = split #refresh bounds for the last Node
                    end = len(mbrs)
            mbr = find_lvl0_mbrs(mbr_list) #it returns the mbr of a leaf Node(calculates  mbr from all the MBRs that the Node contain
            tree.append([nonleaf,node])    #append to an array which will be the final representation of the tree elements([nonleaf,node])from the lower level
            child_nodes.append([node.node_id,mbr]) #nodes that will need to fit into the above level(contains elements in the form of [node_id,total_node_MBR])
        nonleaf = 1 #from now on all the nodes will be nonleaf
        print(str(len(child_nodes)) + " nodes at level " + str(level)) #it prints to the console the number of nodes from level 0
        level += 1 #level increased
        construct_Rtree(child_nodes , max_cap , min_cap) #recursive call of the function to build the upper levels
        
   
def main(argv): 
    file1 = open(argv[1] , "r") #first command line argument refers to coords.txt 
    file2 = open(argv[2] , "r") #second command line argument refers to offsets.txt
    
   
    for l in file1: #fill an array with the contents of coords.txt
        coords.append(l)
    
    points = find_coords(file2) #returns a 2d array that contains [id,set_of_coords] elements
    mbrs = calculate_MBR(points) #returns a 2d array that contains [id,mbr] elements(mbr = [min_x,max_x,min_y,max_y])
    mbrs_unsorted = calculate_z(mbrs) #returns a 2d array that contains [id,mbr,z] elements
    mbrs_sorted = sort_mbr(mbrs_unsorted) #sorts the above array by z-values(merge-sort algorithm is used,other sort algorithms took too long),when sorting process
                                          #is done,z is deleted from the 2d array
    max_cap = 20 #max capacity of a node
    min_cap = 8  #min capacity of a node
    construct_Rtree(mbrs_sorted,max_cap,min_cap) #returns a 2d array that contains [nonleaf,node-id,[[id1,MBR1]..[idn,MBRn]]] elements 
    file1.close()
    file2.close()
    file3.close()
    
if __name__ == "__main__":
    main(sys.argv)    
   
