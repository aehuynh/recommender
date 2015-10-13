from math import sqrt
from collections import defaultdict

class Similarity(object):

    def __init__(self, min_shared=5):
        self._min_shared = min_shared
        pass

    def score(self, users, items, prefs=None):
        raise NotImplementedError

    def shared_items(self, pref1, pref2,):
        return {item : 0 for item in pref1.keys() if item in pref2.keys()}

    def score_matrix(self, matrix):
        similarities = defaultdict(lambda: defaultdict(float))
        count = 0
        for row_id1, pref1 in matrix.items():
            for row_id2, pref2 in matrix.items():
                if row_id1 != row_id2 and (row_id2 not in similarities[row_id1] or row_id1 not in similarities[row_id2]):
                    score = self.score(pref1, pref2)
                    similarities[row_id1][row_id2] = score
                    similarities[row_id2][row_id1] = score

        return similarities

class CosineSimilarity(Similarity):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, pref1, pref2, matrix):
        avg_val = {row_id: sum(matrix[row_id])/ len(matrix[row_id]) for row_id in range(1, len(matrix)) if len(matrix[row_id]) > 0}

        numer =  0
        diff_squared1 = 0
        diff_squared2 = 0

        for user, pref in prefs.item():
            if item1 in  pref and item2 in pref:
                item_diff1 = pref[item1] - avg_prefs[user][item1]
                item_diff2 = pref[item2] - avg_prefs[user][item2]

                numer += abs(item_diff1 * item_diff2)

                item_diff_squared1 += item_diff1 ** 2
                item_diff_squared2 += item_diff2 ** 2

        denom = sqrt(item_diff_squared1 * item_diff_squared2)

        if denom == 0:
            return 0

        return numer / denom

class PearsonSimilarity(Similarity):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, pref1, pref2):
        shared_items = self.shared_items(pref1, pref2)

        n = len(shared_items)
        if n < self._min_shared:
            return 0

        sum_of_products = sum(pref1[item] * pref2[item] for item in shared_items)

        sum1 = sum(pref1[item] for item in shared_items)
        sum2 = sum(pref2[item] for item in shared_items)

        sum_of_squared1 = sum(pref1[item]**2 for item in shared_items)
        sum_of_squared2 = sum(pref2[item]**2 for item in shared_items)

        numer = sum_of_products - (sum1 * sum2 / n)
        denom = sqrt(sum_of_squared1 - sum1**2 / n) * sqrt(sum_of_squared2 - sum2**2 / n)

        if denom == 0:
            return 0

        return numer / denom

class EuclideanSimilarity(Similarity):

    def __init__( *args, **kwargs):
        super().__init__(*args, **kwargs)

    def score(self, pref1, pref2):
        shared_items = self.shared_items(pref1, pref2)

        if len(shared_items) < self._min_shared:
            return 0

        euclid_dist_sum = sum((pref1[item] - pref2[item])**2 for item in shared_items.keys())

        return 1 / (1 + sqrt(euclid_dist_sum))


