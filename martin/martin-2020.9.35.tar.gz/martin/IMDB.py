from imdb import IMDb
from imdb.Movie import Movie


class IMDB:
	def __init__(self):
		self._imdb = IMDb()

	def search(self, title, year=None):
		"""
		:type title: str
		:type year: int
		:rtype: Movie
		"""
		movies = self._imdb.search_movie(title=title)

		if len(movies) == 0:
			print(f'{title} ({year}) not found!')
			return False

		if year is not None:
			for movie in movies:
				if movie.data['year'] == year:
					return self._imdb.get_movie(movie.movieID)

		return self._imdb.get_movie(movies[0].movieID)
