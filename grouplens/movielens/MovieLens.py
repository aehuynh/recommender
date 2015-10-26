from models.rating import MovieRating
from models.movie import Movie

from grouplens.GroupLens import GroupLens

from recommender.models import User as RecommenderUser, Item as RecommenderItem

import os
import csv

class MovieLens(GroupLens):
    """Model for MovieLens dataset that parses the data into a form useable by
    the recommender.
    """

    def __init__(self):
        self._movies = {}
        self._ratings = []

    def load_from_dir(self,
                      dir_name,
                      movies_file_name="movies.csv",
                      ratings_file_name="ratings.csv"):
        self.load_movies(os.path.join(dir_name, movies_file_name))
        self.load_ratings(os.path.join(dir_name, ratings_file_name))

    def load_movies(self, file_path):
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                # Skip header,
                next(reader, None)
                for row in reader:
                    movie = Movie(movie_id=int(row[0]), title=row[1])
                    self._movies[movie.get_id()] = movie
        except Exception as e:
            self._movies= {}
            print("Could not load movies.", e)

    def load_ratings(self, file_path):
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                # Skip header
                next(reader, None)
                for row in reader:
                    rating = MovieRating(user_id=int(row[0]), movie_id=int(row[1]), rating=float(row[2]))
                    self._ratings.append(rating)
        except Exception as e:
            self._ratings = []
            print("Could not load ratings.", e)


    def get_recommender_items(self):
        """Converts self._movies into recommender.models.Item objects."""

        return [RecommenderItem(movie.get_id(), repr(movie)) for movie in self._movies.values()]

    def get_recommender_users(self):
        """Converts self._ratings into recommender.models.User objects."""

        user_ids = set(rating.get_user_id() for rating in self._ratings)
        recommender_users = {user_id: RecommenderUser(user_id, user_id) for user_id in user_ids}

        for rating in self._ratings:
            recommender_users[rating.get_user_id()].add_preference(rating.get_movie_id(), rating.get_rating())

        return list(recommender_users.values())
