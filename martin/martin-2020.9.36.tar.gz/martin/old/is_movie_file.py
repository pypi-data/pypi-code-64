from disk import Path
MOVIE_FILE_EXTENSIONS = [
	'avi', 'mp4', 'mkv', 'wmv', 'mov', 'flv', 'm4p', 'm4v', 'ogg', 'webm',
	'mpeg', 'mpg', 'mp2', 'mpe', 'mpv', 'qt', 'swf', 'avchd'
]


def is_movie_file(path):
	"""
	:type path: Path
	:rtype: bool
	"""

	if path.is_directory():
		return False

	elif not path.exists():
		return False

	elif path.extension.lower() in MOVIE_FILE_EXTENSIONS and path.get_size_gb() >= 1:
		return True

	else:
		return False


def has_movie_file(directory):
	"""
	:type directory: Path
	:rtype: bool
	"""

	for path in directory.files:
		if is_movie_file(path):
			return True

	for path in directory.directories:
		if has_movie_file(path):
			return True

	return False


def get_num_movie_files(path):
	"""
	:type path: Path
	:rtype: bool
	"""
	if path.is_file():
		if is_movie_file(path):
			return 1
		else:
			return 0

	else:
		return sum([get_num_movie_files(subpath) for subpath in path.list()])


def is_movie_directory(path):
	"""
	:type path: Path
	:rtype: bool
	"""
	if path.is_file():
		return False

	elif not path.exists():
		return False

	else:
		for subpath in path.directories:
			if has_movie_file(subpath):
				return False

		return sum([1 for file in path.files if is_movie_file(file)]) == 1

