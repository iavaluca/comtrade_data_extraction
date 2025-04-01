import logging
import os

from .whereToStoreIn import whereToStoreIn

class makingLog:
    """
    Get log while running codes and store it locally.
    """
    # Variable of class: the log file where to write will always be the same through the entire execution
    log = whereToStoreIn(os.getcwd()).file
    
    def __init__(self, info):
        """
        Get instances based on the object you want to print.
        """
        self.info = info
    
    def setup():
        """
        Configure log creation.
        """
        # Use logging.DEBUG or logging.INFO
        logging.basicConfig(    
                            level = logging.INFO,
                            handlers = [
                                        logging.FileHandler(
                                                            makingLog.log, 
                                                            mode = 'a'
                                                            ),
                                        logging.StreamHandler()
                                        ],
                            force = True
                            )
        
        logger = logging.getLogger(__name__)
        
        return logger
         
    def __repr__(self):
        """
        Log message for developers.
        """
        return f"""
                {self.info}
                """