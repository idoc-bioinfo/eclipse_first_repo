import goody
from goody import safe_open
from ndfa import interpret

def read_fa(file : open) -> {str:{str:str}}:
    fa = dict()
    for line in file:
        line_text = line.strip().lower().split(";")
        status = line_text.pop(0)
        state_dict = dict()
        while(line_text): # transitions not empty
            key = line_text.pop(0)
            val = line_text.pop(0)
            state_dict[key]=val
        fa[status] = state_dict.copy()
    return fa
                    
def fa_as_str(fa : {str:{str:str}}) -> str:
#    fa_str = "\nSpecified details of this Finite Automaton\n"
    fa_str = ""
    for k in sorted(fa.keys()):
        transitions = []
        for inp in sorted(fa[k].keys()):
            transitions.append((inp, fa[k][inp]))
        new_line = "  "+ k + " transitions: " + str(transitions) + "\n"
        fa_str += new_line  
    return fa_str
    

def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    fa_run = []
    if state in fa.keys():
        fa_run.append(state)
    else:
        return fa_run.append(None)
    
    current_state = state
    for inp in inputs:
        if str(inp) in fa[current_state]:
            new_state = fa[current_state][str(inp)]
        else: 
            new_state = None                    
        fa_run.append((inp, new_state))
        if new_state == None:
            break
        current_state = new_state
    return fa_run
        
        


def interpret(fa_result : [None]) -> str:
    out_str = "Start state = " + str(fa_result[0]) +"\n"
    stop_state = None 
    for touple in fa_result[1:]:
        stop_state = touple[1]
        if stop_state == None:
             out_str += f'  Input = {touple[0]}; illegal input: simulation terminated\n'
             stop_state = touple[1]
             break
        out_str += f'  Input = {touple[0]}; new state = {touple[1]}\n'
    out_str += "Stop state = " + str(stop_state) + "\n"
    return out_str

if __name__ == '__main__':
    # Write script here
    # f = safe_open('Specify the file name representing the Finite Automaton:','r','Illegal file name',default='faparity.txt')
    # f = open("faparity.txt", "r")
    # fa = read_fa(f)
    # print(fa_as_str(fa))
    # fa_run = process(fa, "even", ['1','0','1','1','0','1','x'])
    # # print(fa_run)
    # print(interpret(fa_run))
    # import sys
    # sys.exit()
              
    # For running batch self-tests
    # print()
    import driver
    driver.default_file_name = "bsc3.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
