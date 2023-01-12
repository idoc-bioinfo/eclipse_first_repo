import goody
from goody import irange
import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:    
    corpus = dict()
    words_iter = word_at_a_time(file)
    fifo = []# # fifo size os +1
    for word in words_iter:
        fifo.append(word)
        if len(fifo) > os:
            # add to dictionary
            key = tuple(fifo[0:os])
            val = fifo[os]
            if not key in corpus.keys():
                corpus[key] = [val]
            elif not val in corpus[key]:
                    corpus[key].append(val)
            # remove last fifo item
            fifo.pop(0)
    return corpus.copy() 

def corpus_as_str(corpus : {(str):[str]}) -> str:
    out_str = ""
    sizes_for_stats = []
    for k in sorted(corpus.keys()):
        out_str += f'  {k} can be followed by any of {corpus[k]}\n'
        sizes_for_stats.append(len(corpus[k]))
    out_str += f'min/max list lengths = {min(sizes_for_stats)}/{max(sizes_for_stats)}\n'
    return out_str

def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    current_words = start
    text_list = list(start)
    for i in range(count):
        if not tuple(current_words) in corpus.keys():
            text_list.append(None)
            break
        optional_words = corpus[tuple(current_words)]
         # random key
        next_word = choice(optional_words)                 
        text_list.append(next_word)
        current_words.append(next_word)
        current_words.pop(0)         
    return text_list

        
if __name__ == '__main__':
    # Write script here
#    # f = safe_open('Specify the file name representing the Finite Automaton:','r','Illegal file name',default='faparity.txt')
    # f = open("wginput1.txt", "r")       
    # corpus = read_corpus(2,f)
    # print(corpus)
    # print(corpus_as_str(corpus))    
    # print(produce_text(corpus, ['a','d'],10))
    # import sys
    # sys.exit()
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
    driver.default_show_traceback = True
    driver.default_show_exception = True
    driver.default_show_exception_message = True
    driver.driver()
