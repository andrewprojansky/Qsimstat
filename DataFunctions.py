import numpy as np

def ESS(state, N):
    """Calculate the Entanglement Spectrum Statistics (ESS).

    Computes the ratio of consecutive gaps in the Schmidt spectrum to
    characterize the entanglement structure.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.
        N (int): Number of qubits in the system.

    Returns:
        float: Average ESS value computed from Schmidt value gaps.

    Note:
        Canonizes the state at the center (N//2) before computing Schmidt values.
        Filters out NaN values from the calculation.
    """

    state.canonize(N//2)
    s_d = self.mps.schmidt_values(N//2)
    lt = []
    rt = []
    for g in range(1, len(s_d)-1):
        vals = [s_d[g-1]-s_d[g], s_d[g]-s_d[g+1]]
        lt.append(min(vals)/max(vals))
        rt.append(vals[0]/vals[1])
    lt = [x for x in lt if str(x) != 'nan']
    result += np.average(lt)
    return result

def repulsion(state):
    """Calculate the level repulsion distribution of Schmidt gaps.

    Computes the distribution of ratios between consecutive Schmidt value gaps,
    which characterizes quantum chaos and thermalization behavior.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.

    Returns:
        np.ndarray: Normalized frequency distribution of gap ratios binned
            into 200 bins between 0 and 4.

    Note:
        Canonizes the state at the center (N//2) before computing Schmidt values.
        Filters out outlier ratios greater than 5.
    """

    state.canonize(N//2)
    s_d = self.mps.schmidt_values(N//2)
    rt = []
    for g in range(1, len(s_d)-1):
        vals = [s_d[g-1]-s_d[g], s_d[g]-s_d[g+1]]
        rt.append(vals[0]/vals[1])
    rt = [x for x in rt if x < 5]
    bins = np.linspace(0,4,201)
    digitized = np.digitize(rt, bins)
    frt = np.array([len(np.array(rt)[digitized==dn]) for dn in range(1, len(bins))]) / len(rt)
    return frt

def IPR(state):
    """Calculate the Inverse Participation Ratio (IPR).

    Measures the localization of the quantum state in the computational basis.
    A smaller IPR indicates more localization.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.

    Returns:
        float: IPR value (to be implemented).

    Note:
        Currently not implemented. Only works with MPS representation.
    """

    pass #only takes in mps 

def Renyi10(state, N):
    """Calculate Renyi entropies (technically tr(rho^k)) for k=0 to 9.

    Computes the trace of powers of the reduced density matrix for various orders,
    which characterizes the entanglement structure.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.
        N (int): Number of qubits in the system.

    Returns:
        np.ndarray: Array of 10 values, where index k contains tr(rho^k).
            For k=1, returns the von Neumann entropy.

    Note:
        This is technically tr(rho^k), not the standard Renyi entropy definition.
        Consider renaming or creating a separate metric for true Renyi entropies.
    """
    #this is techincally not renyi, but tr(rho^k), need to edit/make new metric
    renyis = np.zeros(10)
    for k in range(10):
        if k == 1:
            renyis[k] += self.mps.entropy(N//2)
        else:
            renyis[k] += sum( np.array(self.mps.schmidt_values(N//2)**k) )
    return renyis

def FAF(state, encoding, N, k):
    """Calculate the Fermionic Anti-Flatness (FAF).

    Measures non-Gaussianity of the state in a fermionic encoding by computing
    deviations from Gaussian structure via the covariance matrix.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.
        encoding (list): Set of 2N majoranas/Pauli operators for the encoding.
        N (int): Number of qubits in the system.
        k (int): Power to which the covariance matrix is raised.

    Returns:
        float: FAF value computed as N - 1/2 * tr((cov.T @ cov)^k).
            Measures deviation from Gaussian (free fermion) behavior.

    Note:
        Currently only takes MPS input. Future versions may accept covariance
        matrix directly or compute it from the state.
        Assumes symbolic encoding of 2N majoranas/Paulis.
    """

    #takes in cov, or can take in state and learn cov
    #for now, just takes in mps
    #assumes encoding set of 2n majoranas/Paulis (will build in few, first symbolic only)
    cov = np.zeros(2*N, 2*N)
    for i in range(2*N):
        for j in np.arange(i+1,2*N,1):
            cov[i,j] = state.exp(encoding[i]* encoding[j])
    return N - 1/2 * np.trace( (cov.T . cov)**k )

def bonddim(state):
    """Calculate the bond dimensions of the MPS.

    Returns the bond dimensions (virtual dimensions) at each bond of the
    Matrix Product State, which characterizes entanglement growth.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.

    Returns:
        np.ndarray or list: Bond dimensions at each position (to be implemented).

    Note:
        Currently not implemented. Only works with MPS representation.
    """

    pass #takes in mps 

def flatness(state):
    """Calculate the flatness of the entanglement spectrum.

    Measures how uniform the Schmidt values are across the entanglement cut,
    which indicates the degree of entanglement spreading.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.

    Returns:
        float: Flatness metric value (to be implemented).

    Note:
        Currently not implemented. Only works with MPS representation.
    """

    pass #takes in mps

def porter_thomas(state):
    """Analyze the Porter-Thomas distribution of state coefficients.

    Compares the distribution of state coefficient magnitudes to the expected
    Porter-Thomas distribution, which is a signature of quantum chaos.

    Args:
        state (qtn.MPS): Quantum state as Matrix Product State.

    Returns:
        float or dict: Kullback-Leibler divergence from Porter-Thomas distribution
            and/or related statistics (to be implemented).

    Note:
        Currently not implemented. Implementation steps:
        1. Convert MPS to dense state vector
        2. Compute magnitude of each coefficient
        3. Sort coefficients
        4. Plot distribution
        5. Calculate DKL against e^(-xN)/N (Porter-Thomas)
    """

    pass #takes in mps
    #make state dense
    #magnitude each coefficient
    #sort
    #plot
    #check DKL against e^(-xN)/N