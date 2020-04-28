import numpy as np

# Computes the rank-k SVD truncation of an input numpy array of data.
def rank_k_svd(data, k, debug=False):
	U, S, V = np.linalg.svd(data, full_matrices=False)
	if debug:
		print 'SVD:'
		print U
		print np.diag(S)
		print V
		print np.matmul(np.matmul(U, np.diag(S)), V)
	
	# rank-k SVD truncation
	Uk = U[:, :k]
	Sk = S[:k]
	Vk = V[:k, :]
	data_k_trunc = np.matmul(np.matmul(Uk, np.diag(Sk)), Vk)
	if debug:
		print 'rank-k SVD truncation:'
		print Uk
		print np.diag(Sk)
		print Vk
		print data_k_trunc

	return data_k_trunc
