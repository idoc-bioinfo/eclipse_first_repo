import prompt
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

MATCH = 0   # Index 0 of list associate with name is match (str)
PREFS = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    preference = dict()
    for line in open_file:
        line_words = line.strip().lower().split(";")
        preference[line_words.pop(0)]= [None, line_words]
    return preference 


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    out_str = ""
    out_str = "\n".join(f'  {k} -> {d[k]}' for k in sorted(d.keys(), key=key, reverse=reverse))
    return out_str + "\n"        


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    for i in range(len(order)):
        if order[i] == p1:
            return p1
        if order[i] == p2:
            return p2
    return None  # shouldnt happen

def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    matches = set()
    for k in men.keys():
        matches.add((k, men[k][MATCH]))
    return matches

def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:    
    
    
    unmatched_men = set()
    for k in men.keys():
        if men[k][MATCH] == None:
            unmatched_men.add(k)
    
    men_table = men.copy()                    
    if trace:
        print("\nWomen Preferences (unchanging)")
        print(dict_as_str(women))
        
    while unmatched_men:
        if trace:
            print("\nMen Preferences (current)") 
            print(dict_as_str(men_table))
            print("\nunmatched men = ",unmatched_men, "\n")
        
        man_of_interest = unmatched_men.pop() 
        candidate_woman  = men_table[man_of_interest][PREFS].pop(0)
        candidate_current_match = women[candidate_woman][MATCH]
        # Woman unmatched match men and woman
        if not candidate_current_match:
            women[candidate_woman][MATCH] = man_of_interest
            men_table[man_of_interest][MATCH] = candidate_woman
            if trace:
                print(f'{man_of_interest} proposes to {candidate_woman}, who is currently unmatched, accepting proposal\n')
            continue
                
        candidate_w_preference = who_prefer(women[candidate_woman][PREFS], man_of_interest, candidate_current_match)
        # woman matched but preferes man_of_interest -> replace matching
        if candidate_w_preference == man_of_interest:
            # unmatch current
            unmatched_men.add(candidate_current_match)
            men_table[candidate_current_match][MATCH] = None 
            # match new
            women[candidate_woman][MATCH] = man_of_interest
            men_table[man_of_interest][MATCH] = candidate_woman 
            if trace:
                print(f'{man_of_interest} proposes to {candidate_woman}, who is currently matched, accepting the proposal (likes new match better)\n')
                continue
        else: # woman matched and prefer current match -> add man to the unmatched men
            if trace:
                print(f'{man_of_interest} proposes to {candidate_woman}, who is currently matched, rejecting the proposal (likes current match better)\n')
            unmatched_men.add(man_of_interest)
        
    if trace:
        print("Tracing terminated, the final matches:", extract_matches(men))
    return extract_matches(men) 
          
    
if __name__ == '__main__':
    # Write script here
    f = open("men0.txt", "r") 
    men = read_match_preferences(f)
    print(dict_as_str(men))
    f.close()
    print()
    f = open("women0.txt", "r") 
    women = read_match_preferences(f)
    print(dict_as_str(women))
    f.close()
    
    make_match(men, women, True)
    

    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
