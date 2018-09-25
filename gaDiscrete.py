# This program impliments the discrete genetic algorithm
# here, Discrete means that the new generation is generated
# all at the same time by considering the top agents at that
# given point.

import os
import shutil
import ga2.gaUtils.gaDeamon as deamon

class Session:
    """
    This is the session class which is used to access all
    the agents in the current session, invoke different
    functions on this session and setting session
    parameters.
    """

    def __init__(self,sessID=None, agentCount=100, numParam=10, fixParam=True,
                 spread=2, generateMode='A'):

        if(sessID is None):
            self.sessID = deamon.getNewSessionID()
            self.agentCount = agentCount
            self.numParam = numParam
            self.fixParam = fixParam
            self.spread = spread
            self.generateMode = generateMode
            deamon.setSession(self)
            
        else:
            tmpObj = deamon.getSession(sessID)
            self.sessID = tmpObj.sessID
            self.agentCount = tmpObj.agentCount
            self.numParam = tmpObj.numParam
            self.fixParam = tmpObj.fixParam
            self.spread = tmpObj.spread
            self.generateMode = tmpObj.generateMode
        
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
        try:
            toRet = deamon.getCurrGen(self.sessID)
        except Exception:
            print("Error while retrieving current agents")
            toRet = set()

        return(toRet)

    def getAgent(self, agentID):
        """
        INPUT       : AgentID
        OUTPUT      : Returns the agent with the given AgentId

        DESCRIPTION : Self explanatory from OUTPUT
        """

        agentObj = deamon.getAgent(self.sessID, agentID)
        return(agentObj)
        
    def updateAgent(self, agentObj):
        """
        INPUT       : Agent object
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Updates the status of Agent in the cluster.
        """
        return(deamon.storeAgent(agentObj))
    
    def getBestAgent(self):
        """
        INPUT       : None
        OUTPUT      : Returns the Agent with the best fitness value
                      at present.

        DESCRIPTION : Self explanatory from OUTPUT
        """

        #try:

        bestAgent = None
        currGen = deamon.getCurrGen(self.sessID)
        for agentID in currGen:
            agent = deamon.getAgent(self.sessID, agentID)
            if((bestAgent is None) or (bestAgent.fitness < agent.fitness)):
                bestAgent = agent
        """
        except Exception:
            print("error getting best agent")
            bestAgent = None
        """
        return(bestAgent)

    def getAverageFitness(self):
        """
        INPUT       : None
        OUTPUT      : Returns the current avegare of the fitness value
                      of all the agents in the session.

        DESCRIPTION : Self explanatory from OUTPUT
        """

        try:

            totalFitness = 0
            currGen = deamon.getCurrGen(self.sessID)
            for agentID in currGen:
                totalFitness += deamon.getAgent(self.sessID, agentID).fitness

        except Exception:
            print("error getting average fitness")
            totalFitness = 0

        return(totalFitness/self.agentCount)
                
    def createNextGen(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Creates the next generation based on the session
                      conf that is set in the beginning of the session
        """
        pass

    def resetEnv(self, saveSettings=True):
        """
        INPUT       : saveSettings = False
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Deletes all the agents in the current session
        """
        try:
            
            sessDir = deamon.GA_UTIL_DIR + "/utilFiles/tmp" + str(self.sessID)
            shutil.rmtree(sessDir+"/smtf")
            shutil.rmtree(sessDir+"/dnaPool")
            os.mkdir(sessDir+"/smtf")
            os.mkdir(sessDir+"/dnaPool")
            fp = open(sessDir+"/smtf/LOCK.smtf", "w")
            fp.write(str(0))
            fp.close()
            deamon.setSession(self)
            
        except Exception:
            print("Error resetting session")
            return(0)
        return(1)

    def delete(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Closes and deletes the current session
        """

        try:

            sessDir = deamon.GA_UTIL_DIR + "/utilFiles/tmp" + str(self.sessID)
            shutil.rmtree(sessDir)
            del self
            
        except Exception:
            print("Error deleting session")
