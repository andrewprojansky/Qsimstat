import random
import numpy as np

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
