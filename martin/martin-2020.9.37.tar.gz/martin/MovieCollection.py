from disk import HardFolder
from disk import Path

from .IMDB import IMDB

_IMDB = IMDB()


class MovieCollection:
	def __init__(self, path, imdb=None):
		"""
		:type path: str or Path
		"""

		# path
		self._path = Path(path)
		if not self.path.exists():
			self.path.make_directory()
		elif self.path.is_file():
			raise TypeError(f'{path.path} is a file!')
		self._imdb = imdb or _IMDB

		# information
		self._data_folder = HardFolder(path=self.path + 'data')
		self.data['directories'] = []
		self.data['movie_files'] = []
		self.data['genres'] = []
		self.data['logs'] = []

	def __getstate__(self):
		return self._path

	def __setstate__(self, state):
		self._path = state
		self._imdb = IMDB()
		self._data_folder = HardFolder(path=self.path + 'data')

	@property
	def path(self):
		"""
		:rtype: Path
		"""
		return self._path

	@property
	def data(self):
		"""
		:rtype: HardFolder
		"""
		return self._data_folder

	@property
	def directories(self):
		"""
		:rtype: list[Path]
		"""
		return self.data['directories']

	def add_directory(self, path):
		path = Path(path)
		if not path.exists():
			raise NotADirectoryError(f'{path.path} does not exist!')
		elif path.is_file():
			raise NotADirectoryError(f'{path.path} is a file!')

		directories = self.directories
		if not path in directories:
			directories.append(path)
		self.data['directories'] = directories










