from itertools import product
import logging
import os
import pandas as pd


def aggregate(data: pd.DataFrame, sectors: dict, num: str, denom: str):
    """
    @data: pd.DataFrame
    @sectors: dict
    @num: str
    @denom: str
    
    Aggregate data by sector and country. 
    """
    
    # Initialise dataframe
    stats = pd.DataFrame(
                          columns = sectors.keys(),
                          index = data['reporterDesc'].unique()
                        )
    
    tempNum = pd.DataFrame(
                          columns = sectors.keys(),
                          index = data['reporterDesc'].unique()
                        )
    tempDenom = pd.DataFrame(
                          columns = sectors.keys(),
                          index = data['reporterDesc'].unique()
                        )
    
    # Group by country and sector code
    data = (
            data
            .groupby(by = ['reporterDesc'], dropna = False)
            )
       
    # Divide targetted partner / total for every group
    for g in data.groups:
        df = data.get_group(g)
        for key in sectors:
            nums = (
                                df.loc[
                                       (df['partnerDesc'] == num)
                                       & (df['cmdCode'].isin(sectors[key]))
                                       ]
                                .agg({'primaryValue': 'sum'})
                                )
            denoms = (
                                df.loc[
                                       (df['partnerDesc'] == denom)
                                       & (df['cmdCode'].isin(sectors[key]))
                                       ]
                                .agg({'primaryValue': 'sum'})
                                )
            tempNum.at[g,key] = nums
            tempDenom.at[g,key] = denoms
            stats.at[g, key] = nums.div(denoms.values, axis = 'index').mul(100).item()

    return tempNum, tempDenom, stats
                