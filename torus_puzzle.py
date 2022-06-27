'''
Created on Feb 8, 2020

@author: Vu M Pham
@course: CS540

'''
import copy
from queue import PriorityQueue
'''given a state of the puzzle, represented as a single list of 
 integers with a 0 in the empty space, print to the console all of the possible successor states
'''
def print_succ(state):
    #initialize variable
    goal = [1,2,3,4,5,6,7,8,0]
    
    #call helper method to generate successor list
    succList = create_succList(state)
    
    #for loops to print out successors and their h
    for i in succList:
        #call finder method to get h
        h = h_finder(i,goal)
        print(i,"h="+ str(h))
        
''' find the heuristic value of the passed in state
'''
def h_finder(state,goal):
    #h counter
    h = 0 
    #find heuristic based on the displacement of each indices to the desired goal
    for i in range(9):
        if state[i] != goal[i] and state[i] != 0: #0 does not count
            h += 1
    return h
        
'''helper method that generate the successors of the passed in state
'''
def create_succList(state):
    #initalize the variables
    add1 = []
    add2 = []
    succList = []
    tmp = copy.deepcopy(state)

    for i in range(len(tmp)):
        #condition to find the empty index (0)
        if tmp[i] == 0:
            #this successor is the switching between 0 and the index directly above (or below)
            sub = tmp[i]
            tmp[i] = tmp[i-3]
            tmp[i-3] = sub
            succList.append(tmp)
            
            #this successor is the switching between 0 and the index directly below (or above)
            tmp = copy.deepcopy(state)
            sub = tmp[i]
            tmp[i] = tmp[i-6]
            tmp[i-6] = sub
            succList.append(tmp)
            
            #reset tmp
            tmp = copy.deepcopy(state)
            
            #these successors are the switchings between 0 and the index in the same row
            ''' Original author: geeksforgeeks
                Source: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/ (Links to an external site.)
                The following line was written accordingly
            '''
            splitTmp = [tmp[i*3:(i+1)*3] for i in range((len(tmp)+3-1)//3)] #separate the row
           
            #this successor is the switchings between 0 and the index to the left (or right) 
            splitClone = copy.deepcopy(splitTmp)
            for j in splitTmp: #loop through each row
                for k in range(3): 
                    #condition to find the empty index (0)
                    if j[k] == 0:
                        #switch the indices
                        sub = j[k]
                        j[k]= j[k-1]
                        j[k-1] = sub
                        break
                #put the state back together to create the successor
                add1 = add1 + j
            succList.append(add1)
            
            #this successor is the switchings between 0 and the index to the right (or left)
            #same process as above
            for j in splitClone:
                for k in range(3):
                    if j[k] == 0:
                        sub = j[k]
                        j[k]= j[k-2]
                        j[k-2] = sub
                        break
                add2 = add2 + j
            succList.append(add2)
            tmp = copy.deepcopy(state)                         
            break
    return sorted(succList)

''' given a state of the puzzle, perform the A* search algorithm 
    and print the path from the current state to the goal state
'''
def solve(state):
    #initialize the variables
    endLoop = False
    goal = [1,2,3,4,5,6,7,8,0]
    open = PriorityQueue()
    holder =PriorityQueue()
    closed = []
    final = []
    dict = {'state': '','h': '','g': '' ,'parent': '' ,'f': ''}
    #add the first state to the open queue
    open.enqueue({'state': state,'h': h_finder(state,goal),'g': 0 ,'parent': None ,'f': h_finder(state,goal)})
    #loop find and print the states
    while endLoop != True:
        #pop the item with lowest f 
        tmp = open.pop()
        
        #condition to print and end loop
        if tmp['state'] == goal:
            final.append(tmp)
            tmp1 = copy.deepcopy(tmp)
            while tmp1['parent'] != None:
                for i in closed:
                    if i == tmp1['parent']:
                        final.append(i)
                        tmp1 = i
            for i in range(len(final)):
                print(final[len(final)-1-i]['state'], " h="+str(final[len(final)-1-i]['h'])," moves="+str(final[len(final)-1-i]['g']))
            endLoop = True
            break
        
        #create successors
        succList = create_succList(tmp['state'])
        #add successor to the open queue
        for i in succList:
            dict['state'] = i
            dict['h'] = h_finder(i, goal)
            dict['g'] = tmp['g'] +1
            dict['parent'] = tmp
            dict['f'] = dict['g'] + dict['h']
            open.enqueue(dict.copy())
            #skip successor if item in closed queue has the same state but lower f
            #otherwise enqueue the successor 
            for j in closed:
                if j['state'] == i:
                    if j['f'] < dict['f']:
                        #pop the previously added successor if matched condition   
                        open.queue.pop(len(open.queue)-1)
                    else:
                        open.enqueue(dict.copy())
        #add popped item from open queue to closed queue                
        closed.append(tmp)     
    print(open.max_len)
    
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the init  ial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        
        in_open = False
        # TODO: set in_open to True if the state is in the queue already
        # TODO: handle that case correctly
        
        #loop to the queue to check condition for in_open
        for i in range(len(self.queue)):
            if state_dict['state'] == self.queue.__getitem__(i)['state']:
                in_open = True 
                #skip successor if if item in the queue has the same state but lower f
                #update the queue if a successor has the same state but lower g than an item from the open queue
                if state_dict['f'] < self.queue.__getitem__(i)['f']: 
                    self.queue.__getitem__(i)['g'] = state_dict['g']
                    self.queue.__getitem__(i)['f'] = self.queue.__getitem__(i)['g'] + self.queue.__getitem__(i)['h']
                    self.queue.__getitem__(i)['parent'] = state_dict['parent']
                break
        if not in_open:
            self.queue.append(state_dict)          
        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)
            
    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state


