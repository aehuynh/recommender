from abc import ABCMeta, abstractmethod

class GroupLens(metaclass=ABCMeta):
    """Interface for all GroupLens datasets.
    """
    @abstractmethod
    def load_from_dir(self, dir_name):
        raise NotImplementedError

    @abstractmethod
    def get_recommender_items(self):
        raise NotImplementedError

    @abstractmethod
    def get_recommender_users(self):
        raise NotImplementedError
