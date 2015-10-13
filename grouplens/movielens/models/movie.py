class Movie(object):
    def __init__(self, movie_id, title):
        self._id = movie_id
        self._title = title

    def __repr__(self):
        return self._title

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title
