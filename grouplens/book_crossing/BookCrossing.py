from models.book import Book
from models.rating import BookRating
from models.user import User

from grouplens.GroupLens import GroupLens

from recommender.models import User as RecommenderUser, Item as RecommenderItem

import os
import csv

class BookCrossing(GroupLens):
    def __init__(self):
        self._books = {}
        self._ratings = []
        self._users = {}

    def load_from_dir(self,
                      dir_name,
                      books_file_name="BX-Books.csv",
                      ratings_file_name="BX-Book-Ratings.csv",
                      users_file_name="BX-Users.csv"):
        self.load_books(os.path.join(dir_name, books_file_name))
        self.load_ratings(os.path.join(dir_name, ratings_file_name))
        self.load_users(os.path.join(dir_name, users_file_name))

    def load_books(self, file_path):
        try:
            with open(file_path, 'r', encoding="iso-8859-1") as csv_file:
                reader = csv.reader(csv_file, delimiter=';', quotechar='"')
                # Skip header,
                next(reader, None)
                for row in reader:
                    book = Book(isbn=row[0], title=row[1], author=row[2], publish_year=row[3], publisher=row[4])
                    self._books[book.get_isbn()] = book
        except Exception as e:
            self._books = {}
            print("Could not load books.", e)

    def load_ratings(self, file_path):
        try:
            with open(file_path, 'r', encoding="ISO-8859-1") as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                # Skip header
                next(reader, None)
                for row in reader:
                    rating = BookRating(user_id=int(row[0]), book_isbn=row[1], rating=float(row[2]))
                    self._ratings.append(rating)
        except Exception as e:
            self._ratings = []
            print("Could not load ratings.", e)

    def load_users(self, file_path):
        try:
            with open(file_path, 'rt', encoding="ISO-8859-1") as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                # Skip header
                next(reader, None)
                for row in reader:
                    user = User(user_id=int(row[0]), location=row[1], age=row[2])
                    self._users[user.get_id()] = user
        except Exception as e:
            self._users = {}
            print("Could not load users. ", e)

    def get_recommender_items(self):
        return [RecommenderItem(book.get_isbn(), repr(book)) for book in self._books.values()]

    def get_recommender_users(self):
        recommender_users = {user.get_id(): RecommenderUser(user.get_id(), repr(user)) for user in self._users.values()}

        for rating in self._ratings:
            if rating.get_rating() != "0":
                recommender_users[rating.get_user_id()].add_preference(rating.get_book_isbn(), rating.get_rating())

        return list(recommender_users.values())
