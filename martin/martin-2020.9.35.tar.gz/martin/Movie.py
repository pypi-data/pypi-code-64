from .IMDB import IMDB

_IMDB = IMDB()


class Movie:
	def __init__(self, title=None, year=None, imdb=None):
		"""
		:type movie: _Movie
		"""
		self._imdb = imdb or _IMDB
		self._title = None
		self._year = None
		self._genres = None

		self._movie = self._imdb.search(title=title, year=year)

	def __eq__(self, other):
		if not isinstance(other, Movie):
			raise TypeError(f'cannot compare a Movie with a {type(other)}')
		return self.year == other.year and self.title == other.title

	def __ge__(self, other):
		if not isinstance(other, Movie):
			raise TypeError(f'cannot compare a Movie with a {type(other)}')
		return (self.year, self.title) >= (other.year, other.title)

	def __le__(self, other):
		if not isinstance(other, Movie):
			raise TypeError(f'cannot compare a Movie with a {type(other)}')
		return (self.year, self.title) <= (other.year, other.title)

	def __ne__(self, other):
		return not self == other

	def __gt__(self, other):
		return not self <= other

	def __lt__(self, other):
		return not self >= other

	@property
	def title(self):
		"""
		:rtype: str
		"""
		if self._title is None:
			self._title = str(self._movie['title'])
		return self._title

	@property
	def year(self):
		"""
		:rtype: int
		"""
		if self._year is None:
			self._year = int(self._movie['year'])
		return self._year

	@property
	def genres(self):
		"""
		:rtype: list[str]
		"""
		if self._genres is None:
			genres = self._movie.get('genres')
			if genres is None:
				self._genres = []
			else:
				self._genres = list(genres)
		return self._genres

	def genre_is(self, genre):
		"""
		:type genre: str
		:rtype: bool
		"""
		return genre.lower() in [x.lower() for x in self.genres]

	def genre_in(self, genres):
		"""
		:type genres: list[str]
		:rtype: bool
		"""
		return any([self.genre_is(genre=genre) for genre in genres])

