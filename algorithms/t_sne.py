import numpy as np

from sklearn.manifold import TSNE

# Just a wrapper function for the sklearn implementation
def t_sne(data, k):
    return TSNE(n_components=k).fit_transform(data)

if __name__ == '__main__':
    # Test using the Pachter toy example
    toy_data = np.array([[40., 20., 10.], [20., 10., 15.]])
    print t_sne(toy_data, 2)
