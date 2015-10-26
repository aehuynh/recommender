class User:
    """Bare minimum User object for collaborative filtering."""

    def __init__(self, user_id, value):
        self._id = user_id
        self._value = value
        self._preferences = {}

    def __repr__(self):
        return self._value

    def get_id(self):
        return self._id

    def get_value(self):
        return self._value

    def get_preferences(self):
        return self._preferences

    def add_preference(self, item_id, weight):
        self._preferences[item_id] = weight

class Item:
    """Bare minimum Item object for collaborative filtering."""

    def __init__(self, item_id, value):
        self._id = item_id
        self._value = value

    def __repr__(self):
        return self._value

    def get_id(self):
        return self._id

    def get_value(self):
        return self._value
