__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pandas as pd
import numpy as np

DF = pd.DataFrame


def complete_scale(df: DF, answer_column: str, quantity_column: str, scale_items: tuple, missing_quantity: int) -> DF:
    """Complete df with missing items set to missing_quantity.

    :param df: DataFrame containing scale items.
    :type df: ``pandas.DataFrame``
    :param answer_column: Column with answers on dataframe.
    :type answer_column: ``str``
    :param quantity_column: Column with answer quantities on dataframe.
    :type quantity_column: ``str``
    :param scale_items: Tuple containing all scale items.
    :type scale_items: ``tuple`` from ``str``
    :param missing_quantity: Value to be set for the quantity of the missing values.
    :type missing_quantity: ``int``
    :return: Complete DataFrame with all scale items.
    :rtype: ``pandas.DataFrame``
    """
    if scale_items:
        missing_items = np.setdiff1d(scale_items, df[answer_column].values)
        df = df.append([
            {answer_column: item, quantity_column: missing_quantity}
            for item in missing_items
        ])
    return df
