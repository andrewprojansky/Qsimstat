def ESS(state):

    pass #only takes in mps

def IPR(state):

    pass #only takes in mps 

def Renyi10(state):
    
    pass #only takes in mps 

def FAF(state):
    
    pass #takes in cov, or can take in state and learn cov 

def bonddim(state):

    pass #takes in mps 

def flatness(state):

    pass

from sympy import Symbol 
from openfermion.ops import QubitOperator 
x = Symbol('x') 
hamiltonian = QubitOperator('X0 X5')

