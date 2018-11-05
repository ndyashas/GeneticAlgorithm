"""
This is the DnaClass / AgentClass file all agents
are objects of this class
"""

import random
import numpy as np

def generateDna(numParam, spread, valType):
    """
    INPUT       : numParam, spread
    OUTPUT      : a list of length numParam

    DESCRIPTION : returns a list whose number of rows is as specified
                  and with numbers varying between [0, spread]
    """
    if(valType == 'FLOAT'):
        retDna = [random.uniform(0, spread) for row in range(numParam)]
    else:
        retDna = [random.randint(0, spread) for row in range(numParam)]
    return(retDna)


def normalize(val):
    return(1/(1+val))


class AgentDna:
    """
    This is the AgentDna class, all the agents will be
    of this class, this class impliments some of the 
    basic methods to interact with the Agent and also holds
    all the attributes required to identify and measure the
    agent's fitness
    """
    def __init__(self, sess):
        
        self.agentID = None
        self.sessID = None
        self.dna = generateDna(numParam=sess.numParam,
                               spread=sess.spread,
                               valType=sess.valType)
        self.fitness = 0
        self.nn = None

    def fuNNy(self, ipVector, opVectorSize):
        """
            INPUT       : sess, ipVector, opVectorSize, agentID
            OUTPUT      : opVector of size = opVectorSize
            
            DESCRIPTION : This function is used to genrate dynamic
                          output vectors. This function generates a
                          dynamic neural network based on the three
                          input parameters, runs the ipVector through
                          this network and finally generates the output
                          vector.
        
                          This is a simple feed-forward forward-propagation only neural net
                          The requirement of this functionality was pointed out
                          by Vaibhav V (GitHub @ Vaibhav530), when we tried using
                          ga2 to train an agent in a dynamic environment where
                          there was no fixed target vector. Ofcource neural networks
                          have many efficient training algorithms, but having ga2 to
                          train this neural network is a new thing we wanted to try and
                          allow ga2 to be used in these dynamically changing target vector
                          environments All sessions of ga2 will come along with a nn such
                          this, and can use these if required
        """
        if(self.nn is None):
            self.nn = (np.array(self.dna[:(len(ipVector))*opVectorSize])).reshape((len(ipVector)), opVectorSize)

        return(np.ndarray.tolist(normalize(np.dot(np.array(ipVector), self.nn))))
