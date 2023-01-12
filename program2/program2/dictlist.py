from goody import type_as_str  # Useful for some exceptions

class DictList:
    def __init__(self,*args): # one or more dictionaries as input        
        l = list()
        assert args, "no input (type dict)"
        for element in args:
            assert isinstance(element,dict), str(element) + "is not a dictionary"          
            assert element, "empty dict inserted"
            l.append(element)
        self.dl = l

    
    def __len__(self):      # # of keys
        keys = list()
        for d in self.dl:        # passing over the dict
            keys += d.keys()
        return len(set(keys))
            
    
    def __bool__(self): # True if contains more than single dict
        return len(self.dl) > 1
    
    def __repr__(self): # for the debugger ?
        return "DictList" + str(tuple(self.dl))
    
    def __contains__(self, key): # overloads in
        for d in self.dl: # passing over the dictionary list
            if key in d.keys(): # checking the keys of each dictionary
                return True
        return False
    
    def __getitem__(self, key): # overloads x = dl[key]
        for idx in reversed(range(len(self.dl))):
            if key in self.dl[idx].keys():
                return self.dl[idx].get(key)
        # key not found
        raise KeyError(str(key) + "is not in the dictionary")
        
            
    def __setitem__(self, key, val): # overloads dl[key] = val
        if key in self:  
            for idx in reversed(range(len(self.dl))):
                if key in self.dl[idx].keys():
                    self.dl[idx][key] = val
                    return
        else: # new key
            new_dict = {key:val}
            self.dl.append(new_dict)
            return
        
        
    def __delitem__(self, key):
        if key in self:  
            for idx in reversed(range(len(self.dl))):
                if key in self.dl[idx].keys():
                    del self.dl[idx][key]
                    return
        
        raise KeyError(key + "is not in the dictionary")
    
    
    def __call__(self, key): # list of keys position
        l = list()
        for idx in range(len(self.dl)):
            if key in self.dl[idx].keys():
                l.append((idx, self.dl[idx][key]))  
        return l
                       
        
    def __iter__(self):
        iterated_keys = set()
        for idx in reversed(range(len(self.dl))):
            for key in self.dl[idx].keys():
                if key not in iterated_keys:     
                    iterated_keys.add(key)  
                    yield key
       
    def items(self): # returns list of (key, value)
        l = list()       
        for key in self:
            l.append((key, self[key]))                
        return l 
        
    def collapse(self):
        collopsed_dict = dict()
        for key in self:   #iterator
            val = self[key]
            collopsed_dict[key]= val
        return collopsed_dict   
    
       
    def __eq__(self, dl2): # == operator
        if not (isinstance(dl2, DictList) \
            or isinstance(dl2, dict)):
            raise TypeError ("type DictList or dict is required")
    
        if len(self) != len(dl2): # same number of items
            return False
        
        for item in self.items():
            if not item in dl2.items(): # non overlapping item
                return False

        return True
       
    
    def __lt__(self, dl2): # < operator
        if not (isinstance(dl2, DictList) \
            or isinstance(dl2, dict)):
            raise TypeError ("type DictList or dict is required")
        
        if len(self) >= len(dl2): # same number of items
            return False
        
        for item in self.items():
            if not item in dl2.items(): # not a subset
                return False
        return True

    
    def __gt__(self, dl2): ## > operator
        if not (isinstance(dl2, DictList) \
            or isinstance(dl2, dict)):
            raise TypeError ("type DictList or dict is required")
        
        if len(self) <= len(dl2): # dl2 not included in self
            return False
        
        for item in dl2.items():
            if not item in self.items(): # not a subset
                return False
        return True
        
    

    
    def __add__(self, dl2): ## + operator
        if not (isinstance(dl2, DictList) \
            or isinstance(dl2, dict)):
            raise TypeError ("type DictList or dict is required")
                
        new_input_list = list()       
        for d in self.dl:
                new_input_list.append(d.copy())
                 
        if isinstance(dl2, dict):
            new_input_list.append(dl2.copy())
        else:               # dl2 is DictList            
            for d in dl2.dl:
                new_input_list.append(d.copy())

        return DictList(*new_input_list)

    def __radd__(self, dl2):
        if not (isinstance(dl2, DictList) \
            or isinstance(dl2, dict)):
            raise TypeError ("type DictList or dict is required")
        
        new_input_list = [dl2.copy()]
        for d in self.dl:
                new_input_list.append(d.copy())
        
        return DictList(*new_input_list) 
        
        return self + dl2
          
        
        
    # def ___setattr__(self, key, val): # exeption throwed - no attr 
    #     assert True, "Attributes setting not allowed for DictList"
        
            
if __name__ == '__main__':
    #Simple tests before running driver
    #Put your own test code here to test DictList before doing bsc tests

    d = DictList(dict(a=1,b=2), dict(b=12,c=13))
    print('len(d): ', len(d))
    print('bool(d):', bool(d))
    print('repr(d):', repr(d))
    print(', '.join("'"+x+"'" + ' in d = '+str(x in d) for x in 'abcx'))
    print("d['a']:", d['a'])
    print("d['b']:", d['b'])
    print("d('b'):", d('b'))
    print('iter results:', ', '.join(i for i in d))
    print('item iter results:', ', '.join(str(i) for i in d.items()))
    print('d.collapse():', d.collapse())
    print('d==d:', d==d)
    print('d+d:', d+d)
    print('(d+d).collapse():', (d+d).collapse())
    print ('items type:', type(d.items()))
    print()
    import driver
    driver.default_file_name = 'bsc22S22.txt'
    driver.default_show_exception= True
    driver.default_show_exception_message= True
    driver.default_show_traceback= True
    driver.driver()
