# This is the DnaClass / AgentClass file all agents
# are objects of this class
import random

class AgentDna:
    """
    This is the AgentDna class, all the agents will be
    of this class, this class impliments some of the 
    basic methods to interact with the Agent and also holds
    all the attributes required to identify and measure the
    agent's fitness
    """
    def __init__(self):
        
        self.agentID = None
        self.sessID = None
        self.dna = None
        self.fitness = random.randint(0, 10)
    
    
