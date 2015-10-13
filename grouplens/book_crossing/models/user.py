class User(object):
    def __init__(self, user_id, location, age):
        self._id = user_id
        self._location = location
        self._age = age

    def __repr__(self):
        return self._id

    def get_id(self):
        return self._id
