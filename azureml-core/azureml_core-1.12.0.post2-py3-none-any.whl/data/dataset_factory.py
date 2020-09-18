# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains functionality to create datasets for Azure Machine Learning."""

import re
import sys
import warnings
from azureml.data.abstract_datastore import AbstractDatastore
from azureml.data.constants import _PUBLIC_API
from azureml.data.datapath import DataPath
from azureml.data.data_reference import DataReference
from azureml.data.dataset_type_definitions import PromoteHeadersBehavior
from azureml.data.dataset_error_handling import _validate_has_data
from azureml.data._dataprep_helper import dataprep
from azureml.data._loggerfactory import _LoggerFactory, track
from azureml.exceptions import UserErrorException


_logger = None


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


class TabularDatasetFactory:
    """Contains methods to create a tabular dataset for Azure Machine Learning.

    A :class:`azureml.data.TabularDataset` is created using the ``from_*`` methods in this class, for example,
    the method :func:`azureml.data.dataset_factory.TabularDatasetFactory.from_delimited_files`.

    For more information on working with tabular datasets, see the notebook
    https://aka.ms/tabulardataset-samplenotebook.
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def from_parquet_files(path, validate=True, include_path=False, set_column_types=None, partition_format=None):
        """Create a TabularDataset to represent tabular data in Parquet files.

        .. remarks::

            **from_parquet_files** creates an object of :class:`azureml.data.TabularDataset` class,
            which defines the operations to load data from Parquet files into tabular representation.

            For the data to be accessible by Azure Machine Learning, the Parquet files specified by `path`
            must be located in :class:`azureml.core.Datastore` or behind public web urls.

            Column data types are read from data types saved in the Parquet files. Providing `set_column_types`
            will override the data type for the specified columns in the returned TabularDataset.

            .. code-block:: python

                from azureml.core import Dataset, Datastore
                from azureml.data.datapath import DataPath

                # create tabular dataset from Parquet files in datastore
                datastore = Datastore.get(workspace, 'workspaceblobstore')
                datastore_path = [
                    DataPath(datastore, 'weather/2018/11.parquet'),
                    DataPath(datastore, 'weather/2018/12.parquet'),
                    DataPath(datastore, 'weather/2019/*.parquet')
                ]
                tabular = Dataset.Tabular.from_parquet_files(path=datastore_path)

                # create tabular dataset from Parquet files behind public web urls.
                web_path = [
                    'https://url/datafile1.parquet',
                    'https://url/datafile2.parquet'
                ]
                tabular = Dataset.Tabular.from_parquet_files(path=web_path)

                # use `set_column_types` to set column data types
                from azureml.data import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_long(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool()
                }
                tabular = Dataset.Tabular.from_parquet_files(path=web_path, set_column_types=data_types)

        :param path: The path to the source files, which can be single value or list of http url string,
            :class:`azureml.data.datapath.DataPath` object, or tuple of :class:`azureml.core.Datastore`
            and relative path.
        :type path: str, builtin.list[str],
            azureml.data.datapath.DataPath, builtin.list[azureml.data.datapath.DataPath],
            (azureml.core.Datastore, str), or builtin.list[(azureml.core.Datastore, str)]
        :param validate: Boolean to validate if data can be loaded from the returned dataset. Defaults to True.
            Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :param include_path: Boolean to keep path information as column in the dataset. Defaults to False.
            This is useful when reading multiple files, and want to know which file a particular record
            originated from, or to keep useful information in file path.
        :type include_path: bool
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.dataset_factory.DataType`.
        :type set_column_types: dict[(str, azureml.data.dataset_factory.DataType)]
        :param partition_format: Specify the partition format of path. Defaults to None.
            The partition information of each path will be extracted into columns based on the specified format.
            Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
            datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
            hour, minute and second for the datetime type. The format should start from the position of first
            partition key until the end of file path.
            For example, given the path '../Accounts/2019/01/01/data.parquet' where the partition is by
            department name and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.parquet'
            creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
            with the value '2019-01-01'.
        :type partition_format: str
        :return: Returns a :class:`azureml.data.TabularDataset` object.
        :rtype: azureml.data.TabularDataset
        """
        path = _validate_and_normalize_path(path)
        return TabularDatasetFactory._from_parquet_files(path,
                                                         validate,
                                                         include_path,
                                                         set_column_types,
                                                         partition_format)

    @staticmethod
    def _from_parquet_files(path, validate=True, include_path=False, set_column_types=None, partition_format=None):
        # Without path validation to enable testing with local files.
        from azureml.data import TabularDataset

        dataflow = dataprep().read_parquet_file(path,
                                                include_path=True,
                                                verify_exists=False)
        dataflow = _transform_and_validate(
            dataflow, partition_format, include_path,
            validate or _is_inference_required(set_column_types))
        dataflow = _set_column_types(dataflow, set_column_types)
        return TabularDataset._create(dataflow)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def from_delimited_files(path, validate=True, include_path=False, infer_column_types=True, set_column_types=None,
                             separator=',', header=True, partition_format=None, support_multi_line=False,
                             empty_as_string=False):
        r"""Create a TabularDataset to represent tabular data in delimited files (e.g. CSV and TSV).

        .. remarks::

            **from_delimited_files** creates an object of :class:`azureml.data.TabularDataset` class,
            which defines the operations to load data from delimited files into tabular representation.

            For the data to be accessible by Azure Machine Learning, the delimited files specified by `path`
            must be located in :class:`azureml.core.Datastore` or behind public web urls.

            Column data types are by default inferred from data in the delimited files. Providing `set_column_types`
            will override the data type for the specified columns in the returned TabularDataset.

            .. code-block:: python

                from azureml.core import Dataset, Datastore
                from azureml.data.datapath import DataPath

                # create tabular dataset from delimited files in datastore
                datastore = Datastore.get(workspace, 'workspaceblobstore')
                datastore_path = [
                    DataPath(datastore, 'weather/2018/11.csv'),
                    DataPath(datastore, 'weather/2018/12.csv'),
                    DataPath(datastore, 'weather/2019/*.csv')
                ]
                tabular = Dataset.Tabular.from_delimited_files(path=datastore_path)

                # create tabular dataset from delimited files behind public web urls.
                web_path = [
                    'https://url/datafile1.tsv',
                    'https://url/datafile2.tsv'
                ]
                tabular = Dataset.Tabular.from_delimited_files(path=web_path, separator='\t')

                # use `set_column_types` to set column data types
                from azureml.data import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_long(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool()
                }
                tabular = Dataset.Tabular.from_delimited_files(path=web_path, set_column_types=data_types)

        :param path: The path to the source files, which can be single value or list of http url string,
            :class:`azureml.data.datapath.DataPath` object, or tuple of :class:`azureml.core.Datastore`
            and relative path.
        :type path: str, builtin.list[str],
            azureml.data.datapath.DataPath, builtin.list[azureml.data.datapath.DataPath],
            (azureml.core.Datastore, str), or builtin.list[(azureml.core.Datastore, str)]
        :param validate: Boolean to validate if data can be loaded from the returned dataset. Defaults to True.
            Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :param include_path: Boolean to keep path information as column in the dataset. Defaults to False.
            This is useful when reading multiple files, and want to know which file a particular record
            originated from, or to keep useful information in file path.
        :type include_path: bool
        :param infer_column_types: Boolean to infer column data types. Defaults to True.
            Type inference requires that the data source is accessible from current compute.
        :type infer_column_types: bool
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.dataset_factory.DataType`.
        :type set_column_types: dict[(str, azureml.data.dataset_factory.DataType)]
        :param separator: The separator used to split columns.
        :type separator: str
        :param header: Controls how column headers are promoted when reading from files. Defaults to True for all
            files having the same header. Files will read as having no header When header=False. More options can
            be specified using enum value of :class:`azureml.data.dataset_type_definitions.PromoteHeadersBehavior`.
        :type header: bool or azureml.data.dataset_type_definitions.PromoteHeadersBehavior
        :param partition_format: Specify the partition format of path. Defaults to None.
            The partition information of each path will be extracted into columns based on the specified format.
            Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
            datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
            hour, minute and second for the datetime type. The format should start from the position of first
            partition key until the end of file path.
            For example, given the path '../Accounts/2019/01/01/data.csv' where the partition is by
            department name and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.csv'
            creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
            with the value '2019-01-01'.
        :type partition_format: str
        :param support_multi_line: By default (support_multi_line=False), all line breaks, including those in quoted
            field values, will be interpreted as a record break. Reading data this way is faster and more optimized
            for parallel execution on multiple CPU cores. However, it may result in silently producing more records
            with misaligned field values. This should be set to True when the delimited files are known to contain
            quoted line breaks.

            .. remarks::

                Given this csv file as example, the data will be read differently based on support_multi_line.

                    A,B,C
                    A1,B1,C1
                    A2,"B
                    2",C2

                .. code-block:: python

                    from azureml.core import Dataset, Datastore
                    from azureml.data.datapath import DataPath

                    # default behavior: support_multi_line=False
                    dataset = Dataset.Tabular.from_delimited_files(path=datastore_path)
                    print(dataset.to_pandas_dataframe())
                    #      A   B     C
                    #  0  A1  B1    C1
                    #  1  A2   B  None
                    #  2  2"  C2  None

                    # to handle quoted line breaks
                    dataset = Dataset.Tabular.from_delimited_files(path=datastore_path,
                                                                   support_multi_line=True)
                    print(dataset.to_pandas_dataframe())
                    #      A       B   C
                    #  0  A1      B1  C1
                    #  1  A2  B\r\n2  C2

        :type support_multi_line: bool
        :param empty_as_string: Specify if empty field values should be loaded as empty strings.
            The default (False) will read empty field values as nulls. Passing this as True will
            read empty field values as empty strings. If the values are converted to numeric or
            datetime then this has no effect, as empty values will be converted to nulls.
        :type empty_as_string: bool, optional
        :return: Returns a :class:`azureml.data.TabularDataset` object.
        :rtype: azureml.data.TabularDataset
        """
        from azureml.data import TabularDataset

        if header is True or header is 'ALL_FILES_HAVE_SAME_HEADERS':
            header = PromoteHeadersBehavior.ALL_FILES_HAVE_SAME_HEADERS
        elif header is False or header is 'NO_HEADERS':
            header = PromoteHeadersBehavior.NO_HEADERS
        elif header is 'ONLY_FIRST_FILE_HAS_HEADERS':
            header = PromoteHeadersBehavior.ONLY_FIRST_FILE_HAS_HEADERS
        elif header is 'COMBINE_ALL_FILES_HEADERS':
            header = PromoteHeadersBehavior.COMBINE_ALL_FILES_HEADERS
        elif isinstance(header, str):
            raise UserErrorException('Unsupported header provided. The allowed values are '
                                     'NO_HEADERS'
                                     'ONLY_FIRST_FILE_HAS_HEADERS'
                                     'COMBINE_ALL_FILES_HEADERS'
                                     'ALL_FILES_HAVE_SAME_HEADERS')

        import inspect
        if empty_as_string:
            try:
                inspect.signature(dataprep().read_csv).parameters['empty_as_string']
            except KeyError:
                raise UserErrorException('Unable to create azureml dataset from delimited files with '
                                         'empty_as_string set. azureml.dataprep needs to be upgraded '
                                         'to a version that supports empty_as_string.')
            dataflow = dataprep().read_csv(_validate_and_normalize_path(path),
                                           verify_exists=False,
                                           include_path=True,
                                           infer_column_types=False,
                                           separator=separator,
                                           header=header,
                                           quoting=support_multi_line,
                                           empty_as_string=empty_as_string)
        else:
            dataflow = dataprep().read_csv(_validate_and_normalize_path(path),
                                           verify_exists=False,
                                           include_path=True,
                                           infer_column_types=False,
                                           separator=separator,
                                           header=header,
                                           quoting=support_multi_line)

        dataflow = _transform_and_validate(
            dataflow, partition_format, include_path,
            validate or infer_column_types or _is_inference_required(set_column_types))
        if infer_column_types:
            column_types_builder = dataflow.builders.set_column_types()
            column_types_builder.learn()
            if len(column_types_builder.ambiguous_date_columns) > 0:
                warnings.warn(('Ambiguous datetime formats inferred for columns {} are resolved as "month-day". '
                              'Desired format can be specified by `set_column_types`.')
                              .format(column_types_builder.ambiguous_date_columns))
                column_types_builder.ambiguous_date_conversions_keep_month_day()
            dataflow = column_types_builder.to_dataflow()

        dataflow = _set_column_types(dataflow, set_column_types)
        return TabularDataset._create(dataflow)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def from_json_lines_files(path,
                              validate=True,
                              include_path=False,
                              set_column_types=None,
                              partition_format=None,
                              invalid_lines='error'):
        """Create a TabularDataset to represent tabular data in JSON Lines files (http://jsonlines.org/).

        .. remarks::

            **from_json_lines_files** creates an object of :class:`azureml.data.TabularDataset` class,
            which defines the operations to load data from JSON Lines files into tabular representation.

            For the data to be accessible by Azure Machine Learning, the JSON Lines files specified by `path`
            must be located in :class:`azureml.core.Datastore` or behind public web urls.

            Column data types are read from data types saved in the JSON Lines files. Providing `set_column_types`
            will override the data type for the specified columns in the returned TabularDataset.

            .. code-block:: python

                from azureml.core import Dataset, Datastore
                from azureml.data.datapath import DataPath

                # create tabular dataset from JSON Lines files in datastore
                datastore = Datastore.get(workspace, 'workspaceblobstore')
                datastore_path = [
                    DataPath(datastore, 'weather/2018/11.jsonl'),
                    DataPath(datastore, 'weather/2018/12.jsonl'),
                    DataPath(datastore, 'weather/2019/*.jsonl')
                ]
                tabular = Dataset.Tabular.from_json_lines_files(path=datastore_path)

                # create tabular dataset from JSON Lines files behind public web urls.
                web_path = [
                    'https://url/datafile1.jsonl',
                    'https://url/datafile2.jsonl'
                ]
                tabular = Dataset.Tabular.from_json_lines_files(path=web_path)

                # use `set_column_types` to set column data types
                from azureml.data import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_long(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool()
                }
                tabular = Dataset.Tabular.from_json_lines_files(path=web_path, set_column_types=data_types)

        :param path: The path to the source files, which can be single value or list of http url string,
            :class:`azureml.data.datapath.DataPath` object, or tuple of :class:`azureml.core.Datastore`
            and relative path.
        :type path: str, builtin.list[str],
            azureml.data.datapath.DataPath, builtin.list[azureml.data.datapath.DataPath],
            (azureml.core.Datastore, str), or builtin.list[(azureml.core.Datastore, str)]
        :param validate: Boolean to validate if data can be loaded from the returned dataset. Defaults to True.
            Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :param include_path: Boolean to keep path information as column in the dataset. Defaults to False.
            This is useful when reading multiple files, and want to know which file a particular record
            originated from, or to keep useful information in file path.
        :type include_path: bool
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.DataType`
        :type set_column_types: dict[(str, azureml.data.DataType)]
        :param partition_format: Specify the partition format of path. Defaults to None.
            The partition information of each path will be extracted into columns based on the specified format.
            Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
            datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
            hour, minute and second for the datetime type. The format should start from the position of first
            partition key until the end of file path.
            For example, given the path '../Accounts/2019/01/01/data.jsonl' where the partition is by
            department name and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.jsonl'
            creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
            with the value '2019-01-01'.
        :type partition_format: str
        :param invalid_lines: How to handle lines that are invalid JSON. Supported values are 'error' and 'drop'.
        :type invalid_lines: str
        :return: Returns a :class:`azureml.data.TabularDataset` object.
        :rtype: azureml.data.TabularDataset
        """
        from azureml.data import TabularDataset

        def invalid_lines_to_dprep_enum():
            if invalid_lines == 'error':
                return dataprep().InvalidLineHandling.ERROR
            elif invalid_lines == 'drop':
                return dataprep().InvalidLineHandling.DROP
            else:
                raise UserErrorException('Expected \'error\' or \'drop\' as value for invalid_lines, found {}'
                                         .format(str(invalid_lines)))

        if invalid_lines != 'error':
            try:
                import inspect
                inspect.signature(dataprep().read_json_lines).parameters['invalid_lines']
            except KeyError:
                raise UserErrorException('Unable to create azureml dataset from JSON lines files with '
                                         'invalid_lines set to values other than \'error\'. azureml.dataprep needs '
                                         'to be upgraded to a version >= 1.5.0')

            dataflow = dataprep().read_json_lines(_validate_and_normalize_path(path),
                                                  include_path=True,
                                                  verify_exists=False,
                                                  invalid_lines=invalid_lines_to_dprep_enum())
        else:
            dataflow = dataprep().read_json_lines(_validate_and_normalize_path(path),
                                                  include_path=True,
                                                  verify_exists=False)

        dataflow = _transform_and_validate(
            dataflow, partition_format, include_path,
            validate or _is_inference_required(set_column_types))
        dataflow = _set_column_types(dataflow, set_column_types)
        return TabularDataset._create(dataflow)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': 'TabularDataset'}, activity_type=_PUBLIC_API)
    def from_sql_query(query, validate=True, set_column_types=None, query_timeout=30):
        """Create a TabularDataset to represent tabular data in SQL databases.

        .. remarks::

            **from_sql_query** creates an object of :class:`azureml.data.TabularDataset` class,
            which defines the operations to load data from SQL databases into tabular representation.
            Currently, we only support MSSQLDataSource.

            For the data to be accessible by Azure Machine Learning, the SQL database specified by ``query``
            must be located in :class:`azureml.core.Datastore` and the datastore type must be of a SQL kind.

            Column data types are read from data types in SQL query result. Providing ``set_column_types``
            will override the data type for the specified columns in the returned TabularDataset.

            .. code-block:: python

                from azureml.core import Dataset, Datastore
                from azureml.data.datapath import DataPath

                # create tabular dataset from a SQL database in datastore
                datastore = Datastore.get(workspace, 'mssql')
                query = DataPath(datastore, 'SELECT * FROM my_table')
                tabular = Dataset.Tabular.from_sql_query(query, query_timeout=10)
                df = tabular.to_pandas_dataframe()

                # use `set_column_types` to set column data types
                from azureml.data import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_long(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool()
                }
                tabular = Dataset.Tabular.from_sql_query(query, set_column_types=data_types)

        :param query: A SQL-kind datastore and a query.
        :type query: azureml.data.datapath.DataPath or (azureml.core.Datastore, str)
        :param validate: Boolean to validate if data can be loaded from the returned dataset. Defaults to True.
            Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :param set_column_types: A dictionary to set column data type, where key is column name and value is
            :class:`azureml.data.DataType`.
        :type set_column_types: dict[(str, azureml.data.DataType)]
        :param query_timeout: Sets the wait time (in seconds) before terminating the attempt to execute a command
            and generating an error. The default is 30 seconds.
        :type: int
        :return: Returns a :class:`azureml.data.TabularDataset` object.
        :rtype: azureml.data.TabularDataset
        """
        from azureml.data import TabularDataset
        try:
            dataflow = dataprep().read_sql(*_get_store_and_query(query), query_timeout=query_timeout)
        except TypeError as error:
            import logging
            error_msg = 'The version of azureml-dataprep currently installed is too low and does not support ' \
                        'this operation. Minimum required version is 1.2.1rc0. Please update it by ' \
                        'running: \n "{}" -m pip install --pre azureml-dataprep[fuse,pandas] ' \
                        '--upgrade'.format(sys.executable)
            logging.getLogger().error(error_msg)
            raise UserErrorException(error_msg, inner_exception=error)

        if validate or _is_inference_required(set_column_types):
            _validate_has_data(dataflow, ('Cannot load any data from the datastore using the SQL query "{}". '
                                          'Please make sure the datastore and query is correct.').format(query))
        dataflow = _set_column_types(dataflow, set_column_types)
        return TabularDataset._create(dataflow)


class FileDatasetFactory:
    """Contains methods to create a file dataset for Azure Machine Learning.

    A :class:`azureml.data.FileDataset` is created from the
    :func:`azureml.data.dataset_factory.FileDatasetFactory.from_files` method defined in this class.

    For more information on working with file datasets, see the notebook
    https://aka.ms/filedataset-samplenotebook.
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': 'FileDataset'}, activity_type=_PUBLIC_API)
    def from_files(path, validate=True):
        """Create a FileDataset to represent file streams.

        .. remarks::

            **from_files** creates an object of :class:`azureml.data.FileDataset` class,
            which defines the operations to load file streams from the provided path.

            For the data to be accessible by Azure Machine Learning, the files specified by ``path``
            must be located in a :class:`azureml.core.Datastore` or be accessible with public web URLs.

            .. code-block:: python

                from azureml.core import Dataset, Datastore
                from azureml.data.datapath import DataPath

                # create file dataset from files in datastore
                datastore = Datastore.get(workspace, 'workspaceblobstore')
                datastore_path = [
                    DataPath(datastore, 'animals/dog/1.jpg'),
                    DataPath(datastore, 'animals/dog/2.jpg'),
                    DataPath(datastore, 'animals/dog/*.jpg')
                ]
                file_dataset = Dataset.File.from_files(path=datastore_path)

                # create file dataset from files behind public web urls.
                web_path = [
                    'https://url/image1.jpg',
                    'https://url/image1.jpg'
                ]
                file_dataset = Dataset.File.from_files(path=web_path)

        :param path: The path to the source files, which can be single value or list of http url string,
            :class:`azureml.data.datapath.DataPath` object, or tuple of :class:`azureml.core.Datastore`
            and relative path.
        :type path: str, builtin.list[str],
            azureml.data.datapath.DataPath, builtin.list[azureml.data.datapath.DataPath],
            (azureml.core.Datastore, str), or builtin.list[(azureml.core.Datastore, str)]
        :param validate: Indicates whether to validate if data can be loaded from the returned dataset.
            Defaults to True. Validation requires that the data source is accessible from the current compute.
        :type validate: bool
        :return: A :class:`azureml.data.FileDataset` object.
        :rtype: azureml.data.FileDataset
        """
        from azureml.data import FileDataset

        dataflow = dataprep().api.dataflow.Dataflow._path_to_get_files_block(_validate_and_normalize_path(path))
        if validate:
            _validate_has_data(dataflow, 'Cannot load any data from the specified path. '
                                         'Make sure the path is accessible and contains data.')
        return FileDataset._create(dataflow)


class DataType:
    """Configures column data types for a dataset created in Azure Machine Learning.

    DataType methods are used in the :class:`azureml.data.dataset_factory.TabularDatasetFactory` class
    ``from_*`` methods, which are used to create new TabularDataset objects.
    """

    @staticmethod
    def to_string():
        """Configure conversion to string."""
        dt = DataType()
        dt._set_type_conversion(dataprep().TypeConverter(dataprep().FieldType.STRING))
        return dt

    @staticmethod
    def to_long():
        """Configure conversion to 64-bit integer."""
        dt = DataType()
        dt._set_type_conversion(dataprep().TypeConverter(dataprep().FieldType.INTEGER))
        return dt

    @staticmethod
    def to_float(decimal_mark='.'):
        """Configure conversion to 64-bit float.

        :param decimal_mark: Dot "." or  comma "," for different regions' standard symbol for the decimal place.
            Uses a dot decimal marker by default. For example, the number 1234.56 should use "." as the `decimal mark`
            and the number 1234,56 should use "," as the decimal mark.
        """
        dt = DataType()
        dt._set_type_conversion(dataprep().FloatConverter(decimal_mark))
        return dt

    @staticmethod
    def to_bool():
        """Configure conversion to bool."""
        dt = DataType()
        dt._set_type_conversion(dataprep().TypeConverter(dataprep().FieldType.BOOLEAN))
        return dt

    @staticmethod
    def to_datetime(formats=None):
        """Configure conversion to datetime.

        :param formats: Formats to try for datetime conversion. For example `%d-%m-%Y` for data in "day-month-year",
            and `%Y-%m-%dT%H:%M:%S.%f` for "combined date an time representation" according to ISO 8601.

            * %Y: Year with 4 digits

            * %y: Year with 2 digits

            * %m: Month in digits

            * %b: Month represented by its abbreviated name in 3 letters, like Aug

            * %B: Month represented by its full name, like August

            * %d: Day in digits

            * %H: Hour as represented in 24-hour clock time

            * %I: Hour as represented in 12-hour clock time

            * %M: Minute in 2 digits

            * %S: Second in 2 digits

            * %f: Microsecond
            * %p: AM/PM designator

            * %z: Timezone, for example: -0700

            Format specifiers will be inferred if not specified.
            Inference requires that the data source is accessible from current compute.
        :type formats: str or builtin.list[str]
        """
        dt = DataType()
        if formats is not None:
            if not isinstance(formats, list):
                formats = [formats]
            if len(formats) == 0:
                formats = None
        dt._set_type_conversion(dataprep().DateTimeConverter(formats))
        return dt

    def _set_type_conversion(self, type_conversion):
        self._type_conversion = type_conversion


_set_column_types_type_error = UserErrorException(
    '`set_column_types` must be a dictionary where key is column name and value is :class: azureml.data.DataType')


def _is_inference_required(set_column_types):
    if set_column_types is None:
        return False
    try:
        for data_type in set_column_types.values():
            if isinstance(data_type._type_conversion, dataprep().DateTimeConverter) \
               and data_type._type_conversion.formats is None:
                return True
    except Exception:
        raise _set_column_types_type_error
    return False


def _set_column_types(dataflow, set_column_types):
    if set_column_types is None:
        return dataflow
    type_conversions = {}
    try:
        for column in set_column_types.keys():
            conversion = set_column_types[column]._type_conversion
            if not isinstance(column, str) or not isinstance(conversion, dataprep().TypeConverter):
                raise Exception()  # proper error message will be raised below
            type_conversions[column] = conversion
    except Exception:
        raise _set_column_types_type_error

    if len(type_conversions) == 0:
        return dataflow
    try:
        return dataflow.set_column_types(type_conversions)
    except Exception:
        raise UserErrorException('Cannot infer conversion format for datetime. Please provide the desired formats.')


def _validate_and_normalize_path(path):
    invalid_path_error = UserErrorException(
        'Invalid argument type for `path`. It can be single value or a list of: '
        'string starting with "http://" or "https://", '
        '`azureml.data.datapath.DataPath` object, '
        'or tuple of `azureml.core.Datastore` object and string for relative path in the datastore.')

    if path is None:
        raise invalid_path_error
    if not isinstance(path, list):
        path = [path]
    if len(path) == 0:
        raise invalid_path_error

    http_pattern = re.compile(r'^https?://', re.IGNORECASE)
    if all([isinstance(p, str) for p in path]):
        if any([not http_pattern.match(p) for p in path]):
            raise invalid_path_error
        return path

    normalized = []
    for p in path:
        if isinstance(p, DataPath):
            normalized.append(p)
        elif isinstance(p, DataReference):
            normalized.append(DataPath(p.datastore, p.path_on_datastore))
        elif _is_valid_path_tuple(p):
            normalized.append(DataPath(*p))
        else:
            raise invalid_path_error
    return normalized


def _get_store_and_query(query):
    if _is_valid_path_tuple(query):
        return query
    if isinstance(query, DataPath):
        return query._datastore, query.path_on_datastore
    if isinstance(query, DataReference):
        return query.datastore, query.path_on_datastore
    raise UserErrorException('Invalid argument value or type. Please refer to the documentation for accepted types.')


def _is_valid_path_tuple(path_tuple):
    if isinstance(path_tuple, tuple):
        if len(path_tuple) == 2 and isinstance(path_tuple[0], AbstractDatastore) and isinstance(path_tuple[1], str):
            return True
        raise UserErrorException(
            'Invalid tuple for path. Please make sure the tuple consists of a datastore and a path/SQL query')
    return False


def _transform_and_validate(dataflow, partition_format, include_path, validate):
    if partition_format:
        dataflow = dataflow._add_columns_from_partition_format('Path', partition_format, False)
    if not include_path:
        dataflow = dataflow.drop_columns('Path')
    if validate:
        _validate_has_data(dataflow, 'Cannot load any data from the specified path. '
                                     'Make sure the path is accessible and contains data.')
    return dataflow
