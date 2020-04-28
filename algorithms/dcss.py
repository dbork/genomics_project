import numpy as np

from rank_k_svd import rank_k_svd

# Function implementing the DCSS algorithm.
#
# data: A numpy array of data, with rows representing cells and columns
# 	representing genes.
# k: The rank of the matrix approximation.
# eps: The error tolerance.
# ls_algo: Whether to use an exact or approximate leverage score computation
#	algorithm.
def dcss(data, k, eps, ls_algo, debug=False):
    # exact leverage score computation via SVD
    if ls_algo == 'exact':
        data_k_trunc = rank_k_svd(data, k, debug)

        # Moore-Penrose pseudoinverse
        AkAkT = np.matmul(data_k_trunc, data_k_trunc.T)
        pseudoinv = np.linalg.pinv(AkAkT)
        if debug:
            print 'Moore-Penrose:'
            print pseudoinv
            print np.matmul(np.matmul(AkAkT, pseudoinv), AkAkT)
            print AkAkT

        # leverage scores
        leverages = np.diag(np.matmul(np.matmul(data.T, pseudoinv), data))
        if debug:
            print np.matmul(np.matmul(data.T, pseudoinv), data)
            print leverages
		
        # validate by checking that the sum of the leverage scores ~= k
        assert np.isclose(np.sum(leverages), k)

        # construct the set of sampled rows
        rowset = set({})
        ls_sum = 0
        index = 0
        sorted_row_indices = sorted(
            range(np.shape(data)[1]),
            key=lambda x: leverages[x],
            reverse=True
        )
        if debug:
            print 'Sorting row indices...'
            print sorted_row_indices

        while ls_sum <= k - eps or len(rowset) < k:
            rowset.add(sorted_row_indices[index])
            ls_sum += leverages[sorted_row_indices[index]]
            thresh = leverages[sorted_row_indices[index]]
            index += 1
        if debug:
            print rowset
            print thresh

        # construct DCSS sampling matrix
        S = np.zeros([np.shape(data)[1], len(rowset)])
        for i in range(len(sorted_row_indices)):
            if sorted_row_indices[i] in rowset:
                S[sorted_row_indices[i], i] = 1
        if debug:
            print 'Constructing sampling matrix...'
            print S
            print 'DCSS sample:'
            print np.matmul(data, S)
        # return both the rowset and threshold in addition to the sampled
        # matrix so the identities of the chosen columns can be reconstructed
        return np.matmul(data, S), rowset, thresh

if __name__ == '__main__':
    # Test using the Pachter toy example
    toy_data = np.array([[40., 20., 10.], [20., 10., 15.]])
    dcss(toy_data, 2, 0.3, 'exact', debug=True)

