"""
This is the DnaClass / AgentClass file all agents
are objects of this class
"""

import random


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
