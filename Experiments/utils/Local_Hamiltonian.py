import random
import numpy as np
from scipy.sparse import csr_matrix, kron

# %%
def Local_Hamiltonian(terms,locality,N):
    """
    Generate a k-local Hamiltonain with variable number of terms, for an N-site lattice of spins.
    
    :param terms: Number of (additive) terms to include in the Hamiltonian
    :param locality: Maximum number of Pauli X,Y,Z strings in each term
    :param N: Number of sites
    """
    H_symbolic = []# initialize what will become a list of strings repesenting terms in the Hamiltonian
    
    for ind in range(terms):
        while True:# generates terms until a new one is created (to avoid duplicates)
            term = np.array(["I"] * N)# initial term is all identities
            sites = random.sample(range(N),k=locality)# choose k (unique) random sites to apply Paulis at
            paulis =  [random.choice(["I","X","Y","Z"]) for i in range(locality)]# choose k random Paulis (including identity)
            term[sites] = paulis# assign the paulis at the chosen sites 
            string = "".join(term)# convert from list of chars to string

            if string not in H_symbolic:# check if this pauli string has already been in the Hamiltonian
                H_symbolic.append(string)# if it's new, add this pauli string to the Hamiltonian
                break# leave the while loop and return to generating terms

    return H_symbolic
# %%

def str_to_matrix(string):
    """
    Convert a Pauli string to its sparse matrix representation.

    :param string: the Pauli string, in the form e.g. "IXYZ" 
    """
    I = csr_matrix(np.array([[1, 0], [0, 1]], dtype=complex))# Identity
    X = csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))# Pauli X
    Y = csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))# Pauli Y
    Z = csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))# Pauli Z

    paulis = {'I': I, 'X': X, 'Y': Y, 'Z': Z}

    result = paulis[string[0]]# first pauli
    
    for pauli_char in string[1:]:# Iteratively apply the Kronecker product with subsequent matrices
        result = kron(result, paulis[pauli_char], format='csr')
    return result

# %%
