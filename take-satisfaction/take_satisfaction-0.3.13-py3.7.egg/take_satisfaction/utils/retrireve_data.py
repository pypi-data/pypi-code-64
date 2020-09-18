__author__ = 'Milo Utsch'
__version__ = '0.1.0'
__all__ = [
    'retrieve_data'
]

import typing as tp
import warnings as wn

with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps

from take_satisfaction.utils import get_query_file
from take_satisfaction.utils import load_query
from take_satisfaction.utils import format_text
from take_satisfaction.utils import query_df

SDF = ps.sql.DataFrame
CONTEXT = ps.sql.HiveContext


def retrieve_data(sql_context: CONTEXT, params: tp.Dict[str, tp.Any],
                  query_type: str, query_parameters: tp.Dict[str, tp.Any],
                  answer_column: str, quantities_column: str) -> SDF:
    """Loads and calls the suitable query with passed parameters.
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param params: Dict containing project specific configuration.
    :type params: ``Dict`` from ``any``
    :param query_type: Type of the query to be used. Can be either 'db_simple_query' or 'db_actions_query'.
    :type query_type: ``str``
    :param query_parameters: Dictionary containing parameters to be formatted into the survey query.
    :type query_parameters: ``dict`` from ``str`` to ``any``
    :param answer_column: Answer items column name.
    :type answer_column: ``str``
    :param quantities_column: Quantity of answers column name.
    :type quantities_column: ``str``
    :return: Pyspark dataframe with query.
    :rtype: ``pyspark.sql.DataFrame``
    """
    query_name = get_query_file(params, query_type)
    
    query_parameters['answer'] = answer_column
    query_parameters['quantities'] = quantities_column
    
    query = format_text(load_query(query_name),
                        query_parameters)
    
    return query_df(sql_context=sql_context, query=query)
