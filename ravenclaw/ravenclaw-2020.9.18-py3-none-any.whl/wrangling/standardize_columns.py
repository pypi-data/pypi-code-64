from slytherin import remove_non_alphanumeric
from pandas import DataFrame

import re

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')
def convert_camel_to_snake(string):
	s1 = _first_cap_re.sub(r'\1_\2', string)
	result = _all_cap_re.sub(r'\1_\2', s1).lower()
	result = re.sub(pattern='_+', repl="_", string=result)
	#print(manipulation, result)
	return result


def remove_non_alphanumeric_lower_and_join(x, camel_to_snake=True, replace_with = '_', join_by = '__', ignore_errors = False):
	"""
	:type x: list[str] or tuple or str
	:type camel_to_snake: bool
	:type replace_with: str
	:type join_by: str
	:type ignore_errors: bool
	:rtype: str
	"""
	if type(x) == tuple:
		x = list(x)

	# remove empty strings and remove non alphanumeric
	if type(x) == list:
		#x = [remove_non_alphanumeric(s, replace_with = replace_with) for s in x if s != '']
		x = [str(s).strip() for s in x if s != '']
		x = join_by.join(x)


	try:
		x = remove_non_alphanumeric(s=x, replace_with=' ')
		x = x.strip()
		x = remove_non_alphanumeric(s=x, replace_with=replace_with)
		if camel_to_snake:
			x = convert_camel_to_snake(x)
		x = x.lower()
	except Exception as e:
		if ignore_errors:
			print('Error was ignored for: "', x, '" ', e, sep='')
		else:
			raise e

	return x


def standardize_columns(data, inplace = False, camel_to_snake=True):
	"""
	:type data: DataFrame
	:type inplace: bool
	:type camel_to_snake: bool
	:rtype: DataFrame
	"""
	if inplace:
		new_data = data
	else:
		new_data = data.copy()

	new_data.columns = list(map(
		lambda x: remove_non_alphanumeric_lower_and_join(x = x, camel_to_snake=camel_to_snake),
		list(new_data.columns)
	))

	return new_data

