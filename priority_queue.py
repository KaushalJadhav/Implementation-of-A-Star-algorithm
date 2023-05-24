import heapq

# class for handling priority queues 
class PriorityQueue :
    '''
    creates a Priority Queue Class
    '''

    def __init__(self):
        '''
        Creates a queue
        '''
        self.Queue=[]

    def isempty(self):
        '''
        Checks if given Queue is empty.
        \nReturns True if Empty
        '''
        return not self.Queue:
    
    def push(self,index):
        '''
        Puts given element onto the queue
        \nUses heapq.heappush for faster aproach.
        '''
        heapq.heappush(self.Queue,index)

    def pop(self):
        '''
        Returns the smallest-in-priority element using heapq.heappop
        \n\nComparison based on __lt__ and __gt__ of node class
        '''
        return heapq.heappop(self.Queue)