# This is the DnaClass / AgentClass file all agents
# are objects of this class
import random


def generateDna(numParam, spread):
    """
    INPUT       : rows = 10, columns = 10, spread = 2
    OUTPUT      : class Dna.dna structure

    DESCRIPTION : returns a 2D list whose number of rows is as specified
                  and whose columns is as specified and each value in the
                  matrix is in [0, 10^spread]
    """
    retDna = [random.randint(0, 10**spread) for row in range(numParam)]
    return(retDna)


class AgentDna:
    """
    This is the AgentDna class, all the agents will be
    of this class, this class impliments some of the 
    basic methods to interact with the Agent and also holds
    all the attributes required to identify and measure the
    agent's fitness
    """
    def __init__(self, numParam,  spread):
        
        self.agentID = None
        self.sessID = None
        self.dna = generateDna(numParam=numParam, spread=spread)
        self.fitness = 0
