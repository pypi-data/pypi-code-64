from disk import Path
from imdb.Movie import Movie

from .is_movie_file import is_movie_file
from .is_movie_file import is_movie_directory
from .get_title_year_and_resolution import get_title_year_and_resolution
from martin.IMDB import IMDB


def get_all_files(path):
	"""
	:type path: Path
	:rtype: list[Path]
	"""
	if path.is_file():
		return [path]

	else:
		return [f for p in path.list() for f in get_all_files(p)]


class MovieDirectory(Path):
	def __init__(self, path=None, string=None, movie_file=None):
		path = path or string
		super().__init__(string=path)
		if not is_movie_directory(self):
			raise TypeError(f'{self.path} is not a movie directory!')

		if movie_file is None:
			movie_file = [file for file in self.files if is_movie_file(file)][0]
		self._movie_file = movie_file

	@property
	def movie_file(self):
		"""
		:rtype: MovieFile
		"""
		return self._movie_file

	@property
	def contents(self):
		"""
		:rtype: list[Path]
		"""
		return [self.movie_file] + [
			x for x in self.list() if x.path != self.movie_file.path
		]

	@property
	def title(self):
		return self.movie_file.title

	@property
	def year(self):
		return self.movie_file.year

	@property
	def genres(self):
		return self.movie_file.genres


class MovieFile(Path):
	def __init__(self, path=None, string=None, imdb=None):
		path = path or string
		super().__init__(string=path)
		if not is_movie_file(self):
			raise TypeError(f'{self.path} is not a movie file!')

		if is_movie_directory(self.parent_directory):
			self._directory = MovieDirectory(
				path=self.parent_directory, movie_file=self
			)

		else:
			self._directory = None

		self._directory_name_original = None
		self.fix_directory()
		self._original_names_file = None
		self._original_names = None
		self._imdb = imdb or IMDB()
		self._movie = None
		self._title = None
		self._year = None

	def __repr__(self):
		if self.directory is None:
			return self.description
		else:
			return f'{self.directory.__repr__()}\n\t{self.description}'

	@property
	def directory(self):
		"""
		:rtype: MovieDirectory or NoneType
		"""
		return self._directory

	@property
	def accompanying_files_and_directories(self):
		"""
		:rtype: list[Path]
		"""
		if self.directory is None:
			return []

		else:
			return [x for x in self.directory.list() if x.path != self.path]

	def fix_directory(self):
		if self.directory is None:
			self._directory_name_original = False
			print(f'fixing {self.path}')
			self.move(new_directory=self.parent_directory + self.name.replace('.', ' '))
			self._directory = MovieDirectory(
				path=self.parent_directory, movie_file=self
			)
		else:
			self._directory_name_original = True

	def reset_original_names(self):
		self._original_names = None
		self.original_names_file.delete()

	def create_original_names_file(self):
		self.reset_original_names()
		self.original_names_file.save(self.original_names)

	@property
	def original_names_file(self):
		"""
		:rtype: Path
		"""
		if self._original_names_file is None:
			self._original_names_file = self.directory + 'original_names.pickle'
		return self._original_names_file

	@property
	def original_names(self):
		"""
		:rtype: dict[str, str]
		"""
		if self._original_names is None:
			if self.original_names_file.exists():
				self._original_names = self.original_names_file.load()

			elif self._directory_name_original:
				self._original_names = {
					'file': self.name_and_extension,
					'directory': self.directory.name_and_extension
				}

			else:
				self._original_names = {
					'file': self.name_and_extension,
					'directory': None
				}

		return self._original_names

	@property
	def original_title_year_resolution(self):
		"""
		:rtype: dict[str, str or int]
		"""
		original_names = self.original_names

		if original_names['directory'] is not None:
			name_year_resolution = {
				**get_title_year_and_resolution(name=original_names['file']),
				**get_title_year_and_resolution(name=original_names['directory'])
			}

		else:
			name_year_resolution = get_title_year_and_resolution(name=original_names['file'])

		return name_year_resolution

	@property
	def original_title(self):
		return self.original_title_year_resolution['title']

	@property
	def original_year(self):
		return self.original_title_year_resolution['year']

	@property
	def original_resolution(self):
		return self.original_title_year_resolution['resolution']

	@property
	def description(self):
		return f'{self.title} ({self.year}) [{", ".join(self.genres)}]'

	@property
	def imdb(self):
		"""
		:rtype: IMDB
		"""
		return self._imdb

	@property
	def movie(self):
		"""
		:rtype: Movie or False
		"""
		if self._movie is None:
			self._movie = self.imdb.search(
				title=self.original_title, year=self.original_year
			)
		return self._movie

	@property
	def movie_data_file(self):
		if self.directory is None:
			raise RuntimeError('directory does not exist!')
		movie_data_file = self.directory + 'movie_data.pickle'
		if not movie_data_file.exists():
			if self.movie:
				movie_data_file.save({
					'title': self.movie['title'],
					'year': self.movie['year'],
					'genres': self.movie.get('genres')
				})
			else:
				movie_data_file.save(False)
		return movie_data_file

	@property
	def movie_data(self):
		return self.movie_data_file.load()

	@property
	def title(self):
		"""
		:rtype: str
		"""
		if self.movie_data:
			return self.movie_data['title']

		else:
			return self.original_title

	@property
	def year(self):
		"""
		:rtype: int
		"""
		if self.movie_data:
			return self.movie_data['year']

		else:
			return self.original_year

	@property
	def genres(self):
		"""
		:rtype: list[str]
		"""
		if self.movie_data:
			genres = self.movie_data['genres']
			if genres is None:
				return []

			else:
				return list(genres)

		else:
			return []
