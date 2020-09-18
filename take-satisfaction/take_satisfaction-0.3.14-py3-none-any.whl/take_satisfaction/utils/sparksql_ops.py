__author__ = 'Gabriel Salgado and Milo Utsch'
__version__ = '0.1.3'
__all__ = [
    'DF',
    'SDF',
    'CONTEXT',
    'query_df',
    'spark_to_pandas',
    'get_query_file'
]

import typing as tp
import warnings as wn

import pandas as pd

with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps

DF = pd.DataFrame
SDF = ps.sql.DataFrame
CONTEXT = ps.sql.HiveContext


def get_query_file(params: tp.Dict[str, tp.Any], query_name: str) -> str:
    """Retrieves the location of the file containing the relevant query.
    
    :param params: Dict containing project specific configuration.
    :type params: ``Dict`` from ``any``
    :param query_name: Key word to choose the query to be retrieved from file.
    :type query_name: ``str``
    :return: File name containing the relevant query.
    :rtype: ``str``
    """
    return params[query_name]


def query_df(sql_context: CONTEXT, query: str) -> SDF:
    """Do a query on HIVE spark.
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param query: Query as formatter string.
    :type query: ``str``
    :return: Pyspark dataframe with query.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.sql(query)


def spark_to_pandas(df: SDF) -> DF:
    """Query spark dataframe getting pandas dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Pandas dataframe with the data.
    :rtype: ``pandas.DataFrame``
    """
    return df.toPandas()
