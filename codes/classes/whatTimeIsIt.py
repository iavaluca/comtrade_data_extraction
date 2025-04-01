import datetime as dt

class whatTimeIsIt:
    """
    Get current time; passed into the log maker class. 
    """
    def __init__(self):
        self.time = None
    
    # Define a property object to incorporate the whole set of relevant information of conversion special cases
    # Usage of decorators is syntactic sugar        
    @property
    def time(self):
        """
        Special cases to handle.
        """
        # This turns the time() method into a getter for the attribute exceptions        
        if self._time is None:
            raise AttributeError(f'self._time is {self._time}!')
        return self._time
    
    @time.setter
    def time(self, value):
        """
        Define here, in the settler of time,  the current time in the format you want.
        """        
        value = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self._time = value

    @time.deleter
    def time(self):
        del self._time   
    
    def __repr__(self):
        return f'{self.time}'

