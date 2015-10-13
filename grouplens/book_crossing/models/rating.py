class BookRating(object):
    def __init__(self, user_id, book_isbn, rating):
        self._user_id = user_id
        self._book_isbn = book_isbn
        self._rating = rating

    def get_user_id(self):
        return self._user_id

    def get_book_isbn(self):
        return self._book_isbn

    def get_rating(self):
        return self._rating
