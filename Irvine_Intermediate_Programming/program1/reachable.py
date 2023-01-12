import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    xref = defaultdict(set)
    for line_number,text in enumerate(file,1):
        text = text.strip().lower()
        if len(text) != 0:
            key, value = text.split(';')
            xref[key].add(value)
                # Close the file (it has no more lines to read)
    file.close() 
    return xref


def graph_as_str(graph : {str:{str}}) -> str:
    s = ""
    for word ,lines in sorted(graph.items()):
        s += "  " + word + ' -> [\'' + '\', \''.join(str(x) for x in sorted(lines)) 
        s+= '\']\n'
    return s

        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set = set()
    exploring_list = set(start)
    first_time = True
    while len(exploring_list) != 0:
        if trace:
            print("\nreached_set\t= ", reached_set)
            print("exploring_list\t= ", list(exploring_list))
        
        key = exploring_list.pop()
        
        if key in reached_set:
            continue # already explored    
 
        new_set = graph.get(key,None)
        if first_time and new_set == None: # input node was not found
            return None
        first_time = False
               
        reached_set.add(key) # A reachable node        
        if trace:
            print("moving node", key, "from the exploring list into the reached set")
                          
        if new_set != None:
            exploring_list = exploring_list.union(new_set)
            
        if trace:
            print("after adding all nodes reachable directly from", key, "but not already in reached, exploring = ", sorted(exploring_list))              
          
    return reached_set




if __name__ == '__main__':
    # Write script here
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
