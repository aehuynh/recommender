from abc import ABCMeta, abstractmethod
from collections import defaultdict

from recommender.similarity import PearsonSimilarity


class Recommender(metaclass=ABCMeta):
    """Interface for all collaborative filtering recommenders.
    """

    @abstractmethod
    def load(self, users, items):
        """Processes users and items for recommendations and similarity.
        """
        raise NotImplementedError

    @abstractmethod
    def similar_users(self, user_id):
        """Returns similar users to user with user_id.
        """
        raise NotImplementedError

    @abstractmethod
    def similar_items(self, item_id):
        """Returns similar items to item with item_id.
        """
        raise NotImplementedError

    @abstractmethod
    def recommendations(self, user_id):
        """Returns item recommendations for user.
        """
        raise NotImplementedError


class WeightedSimilarityRecommender(Recommender):
    """A collaborative recommender based on weighted similarity vectors.
    """

    def __init__(self, memorize=False):
        self._memorize = memorize

        self._users = {}
        self._items = {}

        self._preferences = {}
        self._inverted_preferences = {}

        self._item_similarities = {}
        self._user_similarities = {}

    def load(self, users, items):
        """Turn list of Users and Items into dicts of Users and Items with
        their ids as keys and create preference and inverted preference dicts.
        """
        self._users = {user.get_id() : user for user in users}
        self._items = {item.get_id() : item for item in items}

        self._preferences = self._user_prefs(self._users)
        self._inverted_preferences = self._inv_prefs(self._users)

        if self._memorize:
            self._user_similarities = self._similarity.score_matrix(self._preferences)
            self._item_similarities = self._similarity.score_matrix(self._inverted_preferences)

    def _user_prefs(self, users):
        return {user_id : user.get_preferences() for user_id, user in users.items()}

    def _inv_prefs(self, users):
        inv_pref = defaultdict(lambda: defaultdict(float))
        for user_id, user in users.items():
            for item_id, weight in user.get_preferences().items():
                inv_pref[item_id][user_id] = weight

        return inv_pref

    def _similar(self, matrix, row_id):
        pref1 = matrix[row_id]
        scores = []
        for row_id2, pref2 in matrix.items():
            if row_id != row_id2:
                 scores.append((self._similarity.score(pref1, pref2), row_id2))

        scores.sort(reverse=True)
        return scores

    def similar_users(self, user_id, n=10):
        if self._memorize:
            scores = [(score, user_id) for user_id, score in self._user_similarities.items()]
            scores.sort(reverse=True)
        else:
            scores = self._similar(self._preferences, user_id)

        results = [(self._users[user_id].get_value(), user_id, score) for (score, user_id) in scores]

        return results[:n]

    def similar_items(self, item_id, n=10):
        if self._memorize:
            scores = [(score, item_id) for item_id, score in self._item_similarities.items()]
            scores.sort(reverse=True)
        else:
            scores = self._similar(self._inverted_preferences, item_id)

        results = [(self._items[item_id].get_value(), item_id, score) for (score, item_id) in scores]

        return results[:n]

    def recommendations(self, user_id):
        raise NotImplementedError


class ItemBasedRecommender(WeightedSimilarityRecommender):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._similarity = PearsonSimilarity()

    def recommendations(self, user_id, n=10):
        """Recommend items based on item similarities.
        """

        weighted_scores = defaultdict(int)
        total_weight = defaultdict(int)

        for item_id, rating in self._preferences[user_id].items():
            similarities = self._similar(self._inverted_preferences, item_id)
            for score, item_id2 in similarities:
                if item_id2 in self._preferences[user_id] or score == 0:
                    continue
                weighted_scores[item_id2] += rating * score
                total_weight[item_id2] +=  abs(score)

        ranked_items = [(score / total_weight[item_id], item_id) for item_id, score in weighted_scores.items()]
        ranked_items.sort(reverse=True)

        ranked_with_values = [(self._items[item_id].get_value(), item_id, score) for score, item_id in ranked_items]

        results = ranked_with_values[:n]

        return results


class UserBasedRecommender(WeightedSimilarityRecommender):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._similarity = PearsonSimilarity()

    def recommendations(self, user_id, n=10):
        """Recommend items based on user similarities.
        """

        weighted_scores = defaultdict(int)
        total_weight = defaultdict(int)

        for score, user_id2 in self._similar(self._preferences, user_id):
            for item_id, rating in self._preferences[user_id2].items():
                if item_id in self._preferences[user_id] or score == 0:
                    continue
                weighted_scores[item_id] += rating * score
                total_weight[item_id] +=  abs(score)

        ranked_items = [(score / total_weight[item_id], item_id) for item_id, score in weighted_scores.items()]
        ranked_items.sort(reverse=True)

        ranked_with_values = [(self._items[item_id].get_value(), item_id, score) for score, item_id in ranked_items]

        results = ranked_with_values[:n]

        return results
