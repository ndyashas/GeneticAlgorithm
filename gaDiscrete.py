# This program impliments the discrete genetic algorithm
# here, Discrete means that the new generation is generated
# all at the same time by considering the top agents at that
# given point.

import gaUtils.gaDeamon as deamon

class Session:
    """
    This is the session class which is used to access all
    the agents in the current session, invoke different
    functions on this session and setting session
    parameters.
    """

    def __init__(self,agentCount=100, numParam=10, fixParam=True,
                 spread=2, generateMode='A'):

        self.sessID = deamon.getNewSessionID()
        self.agentCount = agentCount
        self.numParam = numParam
        self.fixParam = fixParam
        self.spread = spread
        self.generateMode = generateMode
        self.a = None
        
    def initialize(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Initializes the session with initial
                      values based on the session conf
        """
        
        for i in range(self.agentCount):
            a = deamon.createAgent(self.sessID)

    def getAllAgents(self):
        """
        INPUT       : None
        OUTPUT      : Returns all the current AgentIDs of the active
                      agents in a list.

        DESCRIPTION : Self explanatory from OUTPUT
        """
        pass

    def getAgent(self):
        """
        INPUT       : AgentID
        OUTPUT      : Returns the agent with the given AgentId

        DESCRIPTION : Self explanatory from OUTPUT
        """
        pass

    def updateAgent(self):
        """
        INPUT       : Agent object
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Updates the status of Agent in the cluster.
        """
        pass

    def getBestAgent(self):
        """
        INPUT       : None
        OUTPUT      : Returns the Agent with the best fitness value
                      at present.

        DESCRIPTION : Self explanatory from OUTPUT
        """
        pass

    def getAverageFitness(self):
        """
        INPUT       : None
        OUTPUT      : Returns the current avegare of the fitness value
                      of all the agents in the session.

        DESCRIPTION : Self explanatory from OUTPUT
        """
        pass

    def createNextGen(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Creates the next generation based on the session
                      conf that is set in the beginning of the session
        """
        pass

    def resetEnv(self, saveSettings=False):
        """
        INPUT       : saveSettings = False
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Deletes all the agents in the current session
        """
        pass

    def delete(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Closes and deletes the current session
        """
        pass

a = Session()
a.initialize()
print(a.sessID)
