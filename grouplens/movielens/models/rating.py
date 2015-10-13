class MovieRating(object):
    def __init__(self, user_id, movie_id, rating):
        self._user_id = user_id
        self._movie_id = movie_id
        self._rating = rating

    def get_user_id(self):
        return self._user_id

    def get_movie_id(self):
        return self._movie_id

    def get_rating(self):
        return self._rating
