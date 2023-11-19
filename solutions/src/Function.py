class Function:
    def __init__(self,function,threshold:float,weight:int):
        self.function = function
        self.threshold = threshold
        self.weight = weight
    
    def vote(self,left,right):
        if self.threshold == 0:
            if self.function(left,right):
                return self.weight
            else:
                return -self.weight
        else:
            if self.function(left,right,self.threshold):
                return self.weight
            else:
                return -self.weight