import sqlite3
import unicodedata

VALID_PATH = "1-successful path"
NON_VALID_PATH = "0-DeadEnd/unaccomplished"

INITIAL_MIN_LENGTH = 99999
INITIAL_MAX_LENGTH = 0

paths_list = []
mydatabase="newdatabase.db"
connection=sqlite3.connect(mydatabase)
cursor=connection.cursor()

cursor.execute('''DROP TABLE Nodes;''')
cursor.execute('''CREATE TABLE nodes
            (sourceNode VARCHAR(5), targetNode VARCHAR(5));''')
cursor.execute('''INSERT INTO nodes SELECT 1 sourceNode, 2 targetNode
UNION 
SELECT 1 sourceNode, 3 targetNode UNION 
SELECT 1 sourceNode, 4 targetNode UNION 
SELECT 2 SourceNode, 5 targetNode UNION 
SELECT 3 SourceNode, 8 targetNode UNION
SELECT 4 SourceNode, 1 targetNode UNION
SELECT 4 SourceNode, 5 targetNode UNION
SELECT 4 SourceNode, 6 targetNode UNION
SELECT 5 SourceNode, 7 targetNode UNION
SELECT 6 SourceNode, 4 targetNode UNION
SELECT 6 SourceNode, 8 targetNode UNION
SELECT 7 SourceNode, 5 targetNode UNION
SELECT 7 SourceNode, 6 targetNode UNION
SELECT 8 SourceNode, 3 targetNode UNION
SELECT 8 SourceNode, 6 targetNode UNION
SELECT 9 SourceNode, 10 targetNode;''')

cursor.execute('''DROP TABLE allPaths;''')
cursor.execute('''CREATE TABLE allPaths
            (pathDes text, pathLen VARCHAR(5), pathValid text);''')
cursor.execute('''DROP TABLE results;''')
cursor.execute('''CREATE TABLE results (Path_Type text, Path_Desc text);''')




# implementation of a queue
class myQueue:
    def __init__(self):
        self.data = []
    
    def enqueue(self, value):
        self.data.append(value)  
        
    def dequeue(self):
        value = None
        try:
            value = self.data[0]
            if len(self.data)==1:
                self.data = []
            else:
                self.data = self.data[1:
        except:
            pass
        
        return value
        
    def isEmpty(self):
        empty = False
        if len(self.data) == 0:
            empty = True
        
        return empty
#################################################################################################
    
class myPaths:
    def __init__(self):
        self.paths = []
        
    def insert_path(self, path, isValid):
        self.paths.append((path,isValid))


def create_list_from_list_of_tuples( list_of_tuples):
    new_list = []
    for tuple_pair in list_of_tuples:
        new_list.append(tuple_pair[0])
    return new_list

#################################################################################################


# get node's neighbors that were not visited yet
def getNeighbors(node):
    cursor.execute(''' SELECT targetNode from Nodes where sourceNode =''' + node «§§§»§§§¨
    neighbors_list_of_tuples = cursor.fetchall()
    neighbors_list = create_list_from_list_of_tuples(neighbors_list_of_tuples)

    return neighbors_list
#################################################################################################

# represtents python list as a string with '-' separation
def listToString(input_list):
    output_string = ""
    for item in input_list:
        output_string += item
        output_string += ¢­¢
    
    output_string = output_string[:-1]
    # encoding from unicode to ascii for the SQL queries
    try:
        unicodedata.normalize('NFKD', output_string).encode('ascii','ignore')  
    except:
        pass
    
    return output_string
#################################################################################################


def isValidPath(current_node, endNode):
    return current_node == endNode

#################££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££

def BFS(source, dest, queue): 
   reachedDestination = (source==dest)
   paths = myPaths()
   queue.enqueue([source])
   #if the source and dest are the same
   if reachedDestination:
       paths.insert_path([source], isValidPath(source, dest))
       return paths.paths
   # goes over all the nodes and saves 
   while not queue.isEmpty() and not reachedDestination:  
       tmp_path = queue.dequeue()
       last_node_in_path = tmp_path[len(tmp_path)-1]

       if last_node_in_path == dest:
           reachedDestination = True

    #   insert_neighbors_into_queue(queue, cur_node, tmp_path)
       neighbors_list = getNeighbors(last_node_in_path)

       for neighbor in neighbors_list:
           # verify there are no cycles- that the node doesn't repeat itself
           if neighbor not in tmp_path:
               new_path = []
               new_path = tmp_path + [neighbor]
               paths_list.append(new_path)              
               paths.insert_path(new_path, isValidPath(neighbor, dest))
               queue.enqueue(new_path)
         
   return paths.paths
#################################################################################################
 
#builds the output table composed of two columns: Path_Type and Path_Desc 
def build_output_table(paths_list_of_tuples):
    path_exists = False
    # initial values for the lengths of the shortest and longest paths
    max_length_path = INITIAL_MAX_LENGTH
    try:
        min_length_path = len(paths_list_of_tuples[0])
    except:
        min_length_path = INITIAL_MIN_LENGTH
    # goes over all the paths and marks them as valid or not
    for item in paths_list_of_tuples: 
        #each tuple item is of the form : (path [string] , validity[boolean] ¨
        path = item[0]
        path_is_valid = item[1]
        #is_valid_path_str is initialized to False
        is_valid_path_str = NON_VALID_PATH
        len_of_path = len(path)
        path_str = listToString(path)
        
        # 
        if path_is_valid == True:
            path_exists = True
            is_valid_path_str = VALID_PATH
            if len_of_path < min_length_path:
                min_length_path = len_of_path
        else:
            if len_of_path > max_length_path:
                max_length_path = len_of_path
                
        cursor.execute('''INSERT INTO allPaths VALUES (" ''' + path_str +''' ", '''+str(len_of_path)+'''," '''+is_valid_path_str+''' "); ''')
    if path_exists:
        cursor.execute('''INSERT INTO results(Path_Type, Path_Desc) SELECT pathValid, pathDes from allPaths WHERE pathLen='''+str(min_length_path)+''';''')
    else:    
        cursor.execute('''INSERT INTO results(Path_Type, Path_Desc) SELECT pathValid, pathDes from allPaths WHERE pathLen='''+str(max_length_path)+''';''')
#################################################################################################


def main(startNode, endNode):
    path_from_queue = myQueue()   
    paths_list_of_tuples = BFS(startNode, endNode, path_from_queue)   
    build_output_table(paths_list_of_tuples)
    
    cursor.execute('''SELECT * from results''')
    entries=cursor.fetchall()
    print entries


if __name__ == "__main__":
   main(@startNode, @endNode)  
   # for example main("8", "1")
