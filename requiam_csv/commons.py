import numpy as np
from pandas import DataFrame


def no_org_code_index(df: DataFrame) -> np.ndarray:
    """
    Purpose:
      Identify entries without an Org Code.  This is based on whether
      the value is set to NaN

    :param df: pandas dataframe
    :return no_org_code: numpy array containing elements
    """

    no_org_code = np.where(df['Org Code'].isna() &
                           df['Overall Themes'].isna())[0]

    return no_org_code
