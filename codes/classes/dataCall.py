import logging
import os
import pandas as pd
from pathlib import Path

class dataCall:
    """
    Call data from storage.
    """
    
    # Variable of class: path where to get data stored locally
    # TODO: this can be expanded to SQL databases, etc.
    path = Path(os.getcwd(),
                'data'
                )
    
    def __init__(self, countries, flows):
        """
        @countries: list 
        @flows: list
        
        Initialise class instance.
        """
        self.countries = countries
        self.flows = flows
        self.data = None
        
    @property
    def data(self):
        """
        Data to get.
        """
        # This turns the data() method into a getter for the attribute exceptions        
        if self._data is None:
            raise AttributeError(f'self._data is {self._data}!')
        return self._data
    
    @data.setter
    def data(self, data):
        """
        Define here, in the settler of data, the data to get.
        """      
        
        # Get list of countries with stored data
        # TODO: this relies on exact name match, checks to implement
        countries = [country for country in dataCall.path.iterdir() if country.is_dir() and country.name in self.countries]
        # Get data
        for country in countries:
            # TODO: implement a check if flow exists
            flows = list(map(lambda flow: country / 'Parquet' / flow / 'C', self.flows))
            # Loop over flows
            for flow in flows:
                files = flow.glob('*.parquet.gzip')
                for file in files:
                    df = pd.read_parquet(file)
                    # TODO: make it structural
                    filtered_df = df[df['cmdCode'].apply(lambda code: len(code) <= 2 or code == 'TOTAL')]
                    print(filtered_df)
                    # Save df
                    filtered_df.to_parquet(Path('N:/shared\MED\Monitoring\internalMonitoring\Sep 2024\data\Comtrade',
                                                flow.name,
                                                file.name
                                                ),
                                           compression = 'gzip'
                                           )
        # Get data
        # if self.country in countries:
        #     # List all flows available for the specified country
        #     flows = [flow for flow in os.scandir(os.path.join(dataCall.path, self.country, 'Parquet')) if flow.is_dir()]
        #     logging.info(f'{self.country} flows available: {[flow.name for flow in flows]}. Importing {self.flow}.')
            
        #     data = [pd.read_parquet(f.path) for f in files]
                                                                                                  
        self._data = data

    @data.deleter
    def data(self):
        del self._data
        
    def __repr__(self):
        """
        Log message for developers.
        """
        return f"""
                Country: {self.country}; flow: {self.flow}.
                """
        