'''
#This is all going to be pseudo-code for now. Will fill in later, 
#using previous work and new code. But this will establish file
#structure and workflow. 
'''

import pandas as pd
import quimb.tensor as qtn
import numpy as np
from quimb import *
import scipy.linalg as lng
from qiskit_qec.operators import Pauli
from qiskit.quantum_info import random_clifford
from qiskit.quantum_info import random_pauli

class Experiment:

    def __init__(self, N):

        self.N = N
        self.tracktag = {mps:False, cov:False, pauliprop :False, majprop:False}
        self.statstag = {renyi10: False, FAF:False, IRP:False, ESS:False, bonddim:False, flatness:False}
        self.circuittag = {depth:0, iter:0, sequence:"", dataC:""}
        self.frames = {}

    def exp_setup(self):

        for tags in [self.tracktag, self.statstag]:
            for k in tags.keys():
                t = input(str(k) + "?: ")
                if t not in ["", " ", "false", "False"]:
                    tags[k] = True

        self.circuittag[depth] = int(input("depth?: "))
        self.circuittag[iter] = int(input("iterations?: "))
        self.circuittag[sequence] = (input("gate sequence? (csv): "))
        self.circuittag[dataC] = (input("When to take data? (2,10,end): "))

        if self.circuittag[dataC] == "end":
            num_data_points = 1
        else:
            num_data_points = self.circuittag[depth] // int(self.circuittag[dataC])

        for k in self.statstag.keys():
            if self.statstag[k] = True:
                self.frames[k] = np.array((self.circuittag[iter], num_data_points))


    def execute(self):

        for iter in self.circuittag[iter]:
            state = #init based on tracktag 
            circuit_list = self.circuittag.sequence
            #adjust depth based on instruction list
            for instruction in circuit_list:
                circuit_params = self.run_circuit(instruction)
                #APPLY CIRCUIT HERE, SAVE THINGS TO FRAMES
                #make it divide depth by the # of instructions


    def run_circuit(self, instruction, state):

        pass
