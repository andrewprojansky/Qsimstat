'''
#This is all going to be pseudo-code for now. Will fill in later, 
#using previous work and new code. But this will establish file
#structure and workflow. 

import qsimstat as qss
import numpy as np

class Experiment 

    def __init__(self):
    self.input.mps=False
    self.input.cov = False
    self.input.paulipro=False

track = qss.exp.settrack(mps=True, cov=True, paulipro=True)
stats = qss.exp.setstats(renyi10=True, FAF=True, IPR=True) #also implicit keeps track of bond dim, # cov, and # pauli prop 
setup = qss.exp.setexperiment(N=[10,12,14,16,18], depth = N**2, it = 1000, data_collection=depth2)
circuit = qss.exp.setcircuit(qss.random_product_circuit, 
                         qss.random_matchgate_circuit_brickwork, 
                         qss.random_clifford_circuit_brickwork)
plot = qss.exp.plotting(setup, depth_v_average=True, N_v_end = True, save=True)

experiment = qss.exp.execute(setup, track, circuit, stats, plots)

'''

