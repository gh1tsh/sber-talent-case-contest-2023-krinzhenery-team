import numpy as np

# Алгоритм кластеризации К-средних
class KMeans:
    def __init__(self, n_clusters=2, max_iters=100):
        self.n_clusters = n_clusters
        self.max_iters = max_iters
        self.labels_ = []

    def fit(self, array):
        array = np.array(array)
        # Выбираем центры кластеров случайным образом
        # self.centroids = array[np.random.choice(range(len(array)),size=self.n_clusters,replace=False)]
        self.centroids = array[np.linspace(0,len(array),n_clusters)]

        for _ in range(self.max_iters):
            clusters = [[] for _ in range(self.n_clusters)]
            self.labels_ = []
            for point in array:
                distances = [np.linalg.norm(point - centroid) for centroid in self.centroids]
                cluster_index = np.argmin(distances)
                clusters[cluster_index].append(point)
                self.labels_.append(cluster_index)
            new_centroids = [np.mean(cluster, axis=0) for cluster in clusters]
            if np.array_equal(new_centroids, self.centroids):
                break
            else:
                self.centroids = new_centroids
        return self
