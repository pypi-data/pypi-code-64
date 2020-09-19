from disk import Path
from .is_movie_file import is_movie_file
from .MovieFile import get_all_files
from .MovieFile import MovieFile
from .MovieFile import MovieDirectory
from martin.IMDB import IMDB


class CollectionDirectory(Path):
	def __init__(self, path=None, string=None, imdb=None):
		path = path or string
		super().__init__(string=path, show_size=False)

		self._movie_files = None
		self._imdb = imdb or IMDB()

	@property
	def movie_files(self):
		"""
		:rtype: list[MovieFile]
		"""
		if self._movie_files is None:
			self._movie_files = [
				MovieFile(file, imdb=self.imdb) for file in get_all_files(self)
				if is_movie_file(file)
			]

		return self._movie_files

	@property
	def movie_directories(self):
		"""
		:rtype: list[MovieDirectory]
		"""
		return [movie_file.directory for movie_file in self.movie_files]

	def reset(self):
		self._movie_files = None

	def reset_original_names_files(self):
		for movie_file in self.movie_files:
			movie_file.reset_original_names()

	@property
	def imdb(self):
		"""
		:rtype: IMDB
		"""
		return self._imdb
