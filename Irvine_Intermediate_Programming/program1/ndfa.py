import goody


def read_ndfa(file : open) -> {str:{str:{str}}}:    
    ndfa = dict()
    for line in file:
        line_text = line.strip().lower().split(";")
        status = line_text.pop(0)
        state_dict = dict()
        while(line_text): # transitions not empty
            key = line_text.pop(0)
            val = line_text.pop(0)
            # print("k,v", key, val)
            if key in state_dict.keys():
                state_dict[key].add(val)
            else:
                state_dict[key]=  {val}  
        #     print (state_dict[key])
        # print(state_dict.items())
        # print (dict(sorted(state_dict.items())))
        # print()
                              
        ndfa[status] = state_dict.copy()
                        
    # return dict(sorted(ndfa.items()))
    return ndfa


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    ndfa_str = ""
    for k in sorted(ndfa.keys()):
        transitions = []
        for inp in sorted(ndfa[k].keys()):
            transitions.append((inp, sorted(ndfa[k][inp])))
        new_line = "  "+ k + " transitions: " + str(transitions) + "\n"
        ndfa_str += new_line  
    return ndfa_str

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    ndfa_run = []
    # checking is state exist
    if state in ndfa.keys():
        ndfa_run.append(state)
    else:
        return ndfa_run.append(None)
    
    possible_states = [state]
    for inp in inputs:
        new_states = []
        input_valid = False                
        for state in sorted(possible_states):         
            if str(inp) in ndfa[state]:  
                # input valid
                new_states += ndfa[state][inp]
                input_valid = True                
        
        if not input_valid:
            ndfa_run.append((inp, set()))
            break            
        else:
            ndfa_run.append((inp, set(new_states)) )
            possible_states = new_states
            
    return ndfa_run
        


def interpret(result : [None]) -> str:
    out_str = "Start state = " + str(result[0]) +"\n"
    for touple in result[1:]:
        stop_state = touple[1]        
        
        if stop_state:
            new_states_str = sorted(list(touple[1]))
        else:
            new_states_str = []
        
        out_str += f'  Input = {touple[0]}; new possible states = {new_states_str}\n'
            
        if not stop_state:
            break
                
    out_str += "Stop state(s) = " + str(new_states_str) + "\n"
    return out_str




if __name__ == '__main__':
    # Write script here
#    f = safe_open('Specify the file name representing the Finite Automaton:','r','Illegal file name',default='faparity.txt')
    f = open("ndfaendin01.txt", "r")
    ndfa = read_ndfa(f)
    print(ndfa)
    print(ndfa_as_str(ndfa))
    ndfa_run = process(ndfa, "start", ['1','0','1','1','0','1','x'])
    print(ndfa_run)
    print(interpret(ndfa_run))
    import sys
    # sys.exit() 
    # # For running batch self-tests
    # print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
