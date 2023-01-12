from collections import defaultdict
from goody import type_as_str
from pickle import FALSE

class Bag:

    def __contains__ (self, arg): # 'in' operator
        return self._dict.get(arg) != None
    
    def count(self,arg): # get arg # of instances or 0 if not exists
        if arg in self:  # calls __contains__ ()
            return self._dict[arg]
        return 0
        
    def add(self, new_str): # add item
        self._dict[new_str] = self.count(new_str) + 1
    
    def __init__ (self, input_list = []): # ctor
        self._dict = defaultdict(int) # dictionary of integers 
        for key in input_list:
            self.add(key)
    
    def __len__ (self):     # items count - len()
        len = 0
        for key in self._dict.keys():
            len += self._dict[key]
        return len

    def unique(self): # number of unique item types
        return len(self._dict.keys())
        
    def __str__ (self): # returns string w/ the class content #called with str()    
        l = list()
        for key in self._dict.keys():
            s = str(key + '[' + str(self._dict[key]) + ']')
            l.append(s)
            
        content_str = ', '.join(map(str, l))      
        return 'Bag(' + content_str + ')'
                                           
    
    def __eq__(self, bag2): #compares 2 bags
        if not isinstance(bag2, Bag): # correct type or false
            return False
        
        if self.unique() != bag2.unique():  # equal # of unique items
            return False
                
        # check for same items (unique items of union bag remains the same )
        union_bag = self + bag2
        if union_bag.unique() != self.unique():
            return False     
        
        for key in self._dict.keys(): # compare each of the keys
            if self.count(key) != bag2.count(key):
                return False
            
        return True
    
    
    def __ne__ (self, bag2):
        return not self == bag2
             
    def __iter__(self): # iterator returns a list of items
        l = list()
        for key in self._dict.keys(): # construction of items list
            l += [key] * self.count(key)
        return iter(l)
    
 
    def __add__ (self, bag2): # union of two Bag, called using + operator
        new_bag = Bag()
        if not isinstance(bag2, Bag):
            raise TypeError ("__add__:type Bag is required")
        
        for arg in self: # addition of first bag
            new_bag.add(arg)
        
        for arg2 in bag2: # addition of second bag
            new_bag.add(arg2)          
        
        return new_bag
   
    def remove(self, arg): # removes an argument, exception if not in the bag
        item_count = self.count(arg)
        if item_count > 1: # more than 1 instance
            self._dict[arg] = self.count(arg) - 1
            
        elif item_count == 1: # last item
            del self._dict[arg] 

        else: # argument is not exists
            raise ValueError(arg + "item cannot be removed")
    
    def __repr__ (self):
        l = list()
        for x in self: # calls iterator
            l += .append(x)
        return 'Bag(' + str(l) + ')'


if __name__ == '__main__':
#    test_bag = Bag(['d','a','b','d','c','b','d'])
    test_bag = Bag([])
#    test_bag.repr()
    print (str(test_bag))
#    quit()    #driver tests
    import driver
    driver.default_file_name = 'bsc21S22.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
