import numpy as np

from sklearn.manifold import MDS

# Just a wrapper function for the sklearn implementation
def mds(data, k):
    return MDS(n_components=k).fit_transform(data)

if __name__ == '__main__':
    # Test using the Pachter toy example
    toy_data = np.array([[40., 20., 10.], [20., 10., 15.]])
    print mds(toy_data, 2)
