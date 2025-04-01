from linearmodels.panel.model import PanelOLS
from math import isclose
import numpy as np
import os
import pandas as pd

from codes.classes.dataCall import dataCall

def preparePanel(data: pd.DataFrame, countries: list):
    """
    @data: pd.DataFrame
    @countries: list
    
    Prepare retrieved data for estimation. 
    Data are cleaned; shrunk based on the countries at hand; aggregated; completed with prices information.
    """
    
    # Query data for relevant countries
    data.query('partnerDesc in @countries', inplace = True)
    
    # Aggregate in quarterly frequency
    data['date'] = pd.to_datetime(data['refPeriodId'], format = "%Y%m%d")
    
    groups = (
              data
              .groupby(
                       by = [
                             'reporterISO',
                             'partnerISO',
                             'flowDesc',
                             'cmdCode',
                             'cmdDesc',
                             data['date'].dt.to_period('Q')
                             ]
                       )
              .aggregate(
                         {
                          'primaryValue': 'sum',
                          'netWgt': 'sum'
                          }
                         )
              )
    
    # Get unit log price changes if volume is available
    # Note: exclusion of zeros with pd methods doesn't work probably due to float-related issues
    groups['logPrice'] = np.where(
                                  groups['netWgt'] != 0,
                                  np.log(groups['primaryValue'].div(groups['netWgt'])),
                                  np.nan
                                  )
    # Get q-o-q differences
    groups['logPriceDiff'] = groups.groupby(by = [
                                                  'reporterISO',
                                                  'partnerISO',
                                                  'flowDesc',
                                                  'cmdCode'
                                                  ]
                                            ).diff(periods = 1)['logPrice']
    return groups   
    
    
def regressModel(data: pd.DataFrame, countries: list):
    """
    @data: pd.DataFrame
    @countries: list
    
    Estimate a panel OLS model.
    """
    
    dfs = []
    
    # Drop rows without data on prices or prices diff (dependent variable)
    data.dropna(axis = 'index', how = 'any', subset = ['logPrice', 'logPriceDiff'], inplace = True)
    
    # Define exports
    exports = data.groupby('reporterISO')
    # Define imports based on exporter-reported data
    imports = data.groupby('partnerISO')

    for g in exports.groups:
        exp = exports.get_group(g)
        exp.index.set_names({'reporterISO': 'Exporter', 'partnerISO': 'Importer'}, inplace = True)
        imp = imports.get_group(g)
        imp.index.set_names({'reporterISO': 'Importer', 'partnerISO': 'Exporter'}, inplace = True)
        # IT DROPS ROWS WHERE EXP OR IMP NOT AVAILABLE.
        df = exp.merge(imp, 
                       on = ['Exporter', 'Importer', 'cmdCode', 'cmdDesc', 'date'], 
                       how='inner',
                       suffixes = ('_exports', '_imports')
                       )
        # Convert date to timestamp for regression
        df.index = df.index.set_levels(df.index.get_level_values('date').to_timestamp(), level = 'date', verify_integrity = False)
        dfs.append(df)
        
    # Drop not relevant levels
    df = df.droplevel([
                       'Exporter',
                       'Importer',
                       'cmdDesc'
                       ])
    
    PanelOLS(dependent = df['logPriceDiff_exports'],
              exog = df[['primaryValue_exports', 'primaryValue_imports']],
              entity_effects = True,
              time_effects = True)
    
    return data

def main(countries: list, flow: str):
    """
    @countries: list
    @flow: str
    
    Run a panel OLS model regression based on the inputted data.
    """
    # Initialise object
    data = []
    
    for country in countries:
        data.append(preparePanel(
                                 data = dataCall(country = country, flow = flow).data,
                                 countries = countries
                                 )
                    )
    
    estimates = regressModel(data = pd.concat(data), countries = countries)
         
    return estimates