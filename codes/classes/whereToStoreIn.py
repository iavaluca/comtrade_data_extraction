import os

from .whatTimeIsIt import whatTimeIsIt

class whereToStoreIn:
    """
    Define file where to save log produced from running the codes.
    """
    def __init__(self, path):
        self.path = path
        self.file = None
            
    @property
    def file(self):
        """
        File where to save.
        """
        # This turns the file() method into a getter for the attribute exceptions        
        if self._file is None:
            raise AttributeError(f'self._file is {self._file}!')
        return self._file
    
    @file.setter
    def file(self, file):
        """
        Define here, in the settler of file,  the file where you want to save.
        """        

        print("Creating logs directory...")
        
        # Creating folder where to store the logs
        try:
            os.mkdir(f'{self.path}/logs')
        except FileExistsError:
            print("Directory already exists.")
            pass
        
        print(
            f"""
             Current directory is: "{self.path}".
             We will be writing logs into the following folder: "{self.path}\logs".
            """
        )
        
        # Creating file
        file = os.path.join(self.path, "logs", f'{str(whatTimeIsIt())}.txt') 
        
        self._file = file

    @file.deleter
    def file(self):
        del self._file   
    
    def __repr__(self):
        return self.file    