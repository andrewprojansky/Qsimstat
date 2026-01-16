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

def pauli_str_check(string):
    """
    Check if strings contain only valid Pauli characters 'I', 'X', 'Y', 'Z'

    :param string: the Pauli string, in the form e.g. "IXYZ"

    :raises ValueError: if string contains characters other than 'I', 'X', 'Y', 'Z'
    """
    valid_chars = {'I', 'X', 'Y', 'Z'}
    for i, char in enumerate(string):
        if char not in valid_chars:
            raise ValueError(f"Invalid character '{char}' at position {i} in \"'{string}'\". Only 'I', 'X', 'Y', 'Z' are allowed")


def str_to_matrix(string):
    """
    Convert a Pauli string to its sparse matrix representation.

    :param string: the Pauli string, in the form e.g. "IXYZ"

    :raises ValueError: if string contains characters other than 'I', 'X', 'Y', 'Z'
    """

    pauli_str_check(string)

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

def str_commutator(string1, string2):
    """
    Returns True if the pauli spin operator represented by "string1" commutes with "string2", False otherwise (anti-commutes)

    :param string1: the first Pauli string, in the form e.g. "IXYZ"
    :param string2: the second Pauli string, same form
    
    :raises ValueError: if string1 and string2 have different lengths
    :raises ValueError: if either string contains characters other than 'I', 'X', 'Y', 'Z'
    """
    # Check for valid Pauli string entries
    pauli_str_check(string1)
    pauli_str_check(string2)
    
    # Check if strings have the same length
    if len(string1) != len(string2):
        raise ValueError(f"Pauli strings must have the same length. Got string1 length {len(string1)} and string2 length {len(string2)}")
    
    # Use a binary variable to track parity of anticommuting positions
    # This automatically handles the modulo 2 operation
    commute = True# start with commuting, check how many positions don't commute
    for p1, p2 in zip(string1, string2):
        if p1 != 'I' and p2 != 'I' and p1 != p2:
            commute ^= True  # Flip the parity
    
    # Return False if anticommute (odd number of anticommuting positions), True if commute (even)
    return commute

def commutation_graph(pauli_strings):
    """
    Generate a commutation graph for a list of Pauli strings.
    
    :param pauli_strings: List of Pauli strings, e.g. ["IXYZ", "XYYI", ...]

    :returns: A 2D numpy array where entry (i, j) is True if pauli_strings[i] commutes with pauli_strings[j], False otherwise

    :raises ValueError: if Pauli strings have different lengths or if any string is invalid
    """
    # Handle empty list case
    if len(pauli_strings) == 0:
        return np.zeros((0, 0), dtype=bool)
    
    # Validate Pauli strings
    for ps in pauli_strings:
        pauli_str_check(ps)
    
    # Check that all Pauli strings have the same length
    first_length = len(pauli_strings[0])
    if not all(len(ps) == first_length for ps in pauli_strings):
        raise ValueError("All Pauli string terms must have the same length")

    n = len(pauli_strings)
    graph = np.ones((n, n), dtype=bool)# graph starts with all True since the diagonal always commutes with itself

    # Compute full commutation graph
    for i in range(n):
        for j in range(i+1,n):
            graph[i, j] = graph[j,i] = str_commutator(pauli_strings[i], pauli_strings[j])
    
    return graph