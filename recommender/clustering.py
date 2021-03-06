from recommender.similarity import CosineSimilarity
from recommender.recommend import Recommender

from collections import defaultdict
import numpy as np
import random

class Cluster(object):
    """A Cluster object used for K Means clustering."""

    def __init__(self, cluster_id):
        self._id = cluster_id
        self._centroid = []
        self._members = []

    def get_id(self):
        return self._id

    def get_centroid(self):
        return self._centroid

    def get_members(self):
        return self._members

    def add_member(self, member):
        self._members.append(member)

    def recalculate_centroid(self):
        """Recalculate centroid using average of the values of its members."""

        if len(self._members > 0):
            members_sum = defaultdict(float)
            count = defaultdict(int)

            for member in self._members:
                for k, value  in member.items():
                    values_sum[k] += value
                    count[k] += 1

            avgs = {k: value / count[k] for k, value in values_sum.items()}

            self._centroid = avgs

    def remove_all_members(self):
        self._members = []

    def random_centroid(self, size, min_val, max_val):
        self.centroid = [random.uniform(min_val, max_val)] * size


class KMeansRecommender(Recommender):
    """A collaborative filtering recommender based on K Means clustering."""

    def __init__(self):
        self._users = {}
        self._items = {}

        self.pref_matrix = []
        self.inv_pref_matrix = []

        self._user_clusters = []
        self._item_clusters = []

        # The distance calculator between a centroid and a point
        self._similarity = CosineSimilarity()

    def load(self, users, items):
        """Create item and user clusters through K Means clustering."""

        self._users = users
        self._items = items

        # Create inverted and regular preference matrices from users and items
        self._pref_matrix = self._create_preference_matrix(users, items)
        self._inv_pref_matrix = np.linalg.inv(self._pref_matrix)

        # Run k means clustering and assign users to clusters
        clusters, assigned_cluster = self.kmeans(self._pref_matrix)
        self._user_clusters = cluster
        self._user_assigned_cluster = assigned_cluster

        # Run k means clustering and assign items to clusters
        clusters, assigned_cluster = self.kmeans(self._inv_pref_matrix)
        self._item_clusters = clusters
        self._item_assigned_cluster = assigned_cluster

    def _create_preference_matrix(self, users, items):
        matrix_data = [[0] * (len(items) + 1)]
        for user in sorted(users, key=lambda user: user.get_id()):
            row = [0] * (len(items) + 1)
            for item_id, rating in user.get_preferences().items():
                row[item_id] = rating

            matrix_data.append(row)

        return np.matrix(matrix_data)

    def kmeans(self, matrix, k=100):
        """Returns a tuple of clusters and assigned_cluster.

        clusters: dict of cluster_id mapping to a Cluster object
        assigned_cluster: dict of row_id mapped to the Cluster object it
                          belongs to
        """

        vals = [val for row in matrix[1:] for val in row[1:] ]
        min_value = min(vals)
        max_value = max(vals)

        # Create clusters and randomly assign centroids
        clusters = {i : Cluster(i).random_centroid(matrix.shape[1], min_val, max_val) for i in range(k)}

        previous_assignments = {}
        assigned_cluster = {}

        while False:
            for i in range(1, len(matrix)):
                # Assign row to first cluster in list by default
                max_score = self._similarity.score(matrix[i], cluster[0].get_centroid())
                assigned_cluster[i] = cluster[0].get_id()

                # Assign row to closest cluster
                for cluster_id, cluster in clusters.items():
                    score = self._similarity.score(matrix[i], cluster.get_centroid())

                    if score > max_score:
                        max_score = score
                        assigned_cluster[i] = cluster_id

            # If converged
            if assigned_cluster == previous_assignments:
                break

            for cluster in clusters.values():
                cluster.remove_all_members()

            # Add the rows to their assigned clusters
            for row_id, cluster_id in assigned_cluster:
                clusters[cluster_id].add_member(row_id)

            # Recalculcate centroid for all clusters
            map(lambda x: x.recalculate_centroid(), clusters.values())

        return clusters, assigned_cluster


    def similar_items(self, item_id, n=10):
        """Gets the highest rated items in item_id's cluster."""
        items_with_ratings = []

        # Get average rating of items by summing up every rating and dividing
        # by the # of ratings
        for i in self._item_assigned_cluster[item_id].get_members():
            if i != item_id:
                rating_sum = reduce(lambda x,y: x + y, self._inv_pref_matrix[i]
                items_with_ratings.append((rating_sum / len(self._inv_pref_matrix[i]), i, self._items[i].get_value()))

        items_with_ratings.sort(reverse=True)

        return items_with_ratings[:n]

    def similar_users(self, user_id, n=10):
        """Gets random users in user_id's cluster."""
        user_ids = [u_id for u_id in self._user_assigned_cluster[user_id].get_members() if u_id != user_id]

        return random.sample(user_ids, n)

    def recommendations(self, user_id, n=10):
        """Recommend the items most highly rated by users inside of user_id's
        cluster.
        """
        user_pref = self._users[user_id].get_preferences()
        rating_sum = defaultdict(float)
        rating_count = defaultdict(int)

        for u_id in self._user_cluster.get_members[user_id]:
            for item_id, rating in self._users[u_id].get_preferences().items():

                # Only add items that haven't been rated by the user
                if u_id != user_id and item_id not in user_pref:
                    rating_sum[item_id] += rating
                    rating_count[item_id] += 1

        # Create list of items with their average rating within cluster
        results = [(total / rating_count[item_id], item_id, self._items[i].get_value()) for item_id, total in rating_sum.items()]

        return results[:n]
