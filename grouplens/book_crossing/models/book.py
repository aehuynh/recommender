class Book(object):
    def __init__(self, isbn, title, author, publish_year, publisher):
        self._isbn = isbn
        self._title = title
        self._author = author
        self._publish_year = publish_year
        self._publisher = publisher

    def __repr__(self):
        return self._title + " by " + self._author

    def get_isbn(self):
        return self._isbn
