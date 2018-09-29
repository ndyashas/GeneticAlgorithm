# This program impliments the discrete genetic algorithm
# here, Discrete means that the new generation is generated
# all at the same time by considering the top agents at that
# given point.

import os
import shutil
import random
import ga2.gaUtils.gaDeamon as deamon

class Session:
    """
    This is the session class which is used to access all
    the agents in the current session, invoke different
    functions on this session and setting session
    parameters.
    """

    def __init__(self,sessID=None, agentCount=100, numParam=10, fixParam=True,
                 spread=2, survival=0.05, genecopy=0.9, mutation=0.01, generateMode='A'):

        if(sessID is None):
            self.sessID = deamon.getNewSessionID()
            self.agentCount = agentCount
            self.numParam = numParam
            self.fixParam = fixParam
            self.spread = spread
            self.generateMode = generateMode
            self.mutation = mutation
            self.genecopy = genecopy
            self.survival = survival
            deamon.setSession(self)

        else:
            tmpObj = deamon.getSession(sessID)
            self.sessID = tmpObj.sessID
            self.agentCount = tmpObj.agentCount
            self.numParam = tmpObj.numParam
            self.fixParam = tmpObj.fixParam
            self.spread = tmpObj.spread
            self.mutation = mutation
            self.survival = survival
            self.genecopy = genecopy
            self.generateMode = tmpObj.generateMode
        
    def init(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Initializes the session with initial
                      values based on the session conf .

        we create self.agentCount number of agents here
        using the deamon function createAgent
        """
        
        try:
            for i in range(self.agentCount):
                agentObj = deamon.createAgent(self)
        
        except Exception as e:
            print("gaDiscrete.init failed with error as : {}".format(e))
        
    def getAllAgents(self):
        """
        INPUT       : None
        OUTPUT      : Returns all the current AgentIDs of all the active
                      agents in a list, or None on error

        DESCRIPTION : Self explanatory from OUTPUT

        
        toRet is the set containing the agentIDs of all
        agents who are currently active.
        toRet is populated by using the deamon function
        getCurrGen
        """
        
        try:
            toRet = deamon.getCurrGen(self.sessID)
        except Exception as e:
            print("gaDiscrete.getAllAgents failed with error as : {}".format(e))
            toRet = None
            
        return(toRet)

    def getAgent(self, agentID):
        """
        INPUT       : AgentID
        OUTPUT      : Returns the agent with the given AgentId, 
                      None on error

        DESCRIPTION : Self explanatory from OUTPUT

        agentObj is the agent corresponding to the agentID = agentID
        and belonging to the session with sessID = sessID
        uses the deamon function
        """

        try:
            agentObj = deamon.getAgent(self.sessID, agentID)
            return(agentObj)
        
        except Exception as e:
            print("gaDiscrete.getAgent failed with error as : {}".format(e))
        
    def updateAgent(self, agentObj):
        """
        INPUT       : Agent object
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Updates the status of Agent in the cluster.

        Stores the agent in the current session agent's file
        this storage is for persistance and to save the RAM
        for tree building or other more important jobs
        uses the deamon storeAgent function
        """

        try:
            return(deamon.storeAgent(agentObj))
        
        except Exception as e:
            print("gaDiscrete.updateAgent failed with error as : {}".format(e))            
    
    def getBestAgent(self):
        """
        INPUT       : None
        OUTPUT      : Returns the Agent with the best fitness value
                      at present , and None on error

        DESCRIPTION : Self explanatory from OUTPUT

        This is used to retrieve the best agent in the current
        pool of agents based on their fitness value with
        higher fitness corresponding to being better
        uses deamon functions getCurrGen, getAgent
        """

        try:
            bestAgent = None
            currGen = deamon.getCurrGen(self.sessID)
            for agentID in currGen:
                agent = deamon.getAgent(self.sessID, agentID)
                if((bestAgent is None) or (bestAgent.fitness < agent.fitness)):
                    bestAgent = agent
                    
        except Exception as e:
            print("gaDiscrete.getBestAgent failed with error as : {}".format(e))
            bestAgent = None
        
        return(bestAgent)

    def getAverageFitness(self):
        """
        INPUT       : None
        OUTPUT      : Returns the current avegare of the fitness value
                      of all the agents in the session.

        DESCRIPTION : Self explanatory from OUTPUT

        This function is used to get the average fitness value of
        agents in the current session, this uses deamon functions
        getCurrGen, getAgent
        """

        try:
            totalFitness = 0
            currGen = deamon.getCurrGen(self.sessID)
            for agentID in currGen:
                totalFitness += deamon.getAgent(self.sessID, agentID).fitness

        except Exception:
            print("gaDiscrete.getAverageFitness failed with error as : {}".format(e))
            totalFitness = 0

        return(totalFitness/self.agentCount)
                
    def createNextGen(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Creates the next generation based on the session
                      conf that is set in the beginning of the session

        This is the main attraction in this session file XD
        the algorithm follows as this :
        
        a 'numberOfSurvivors' number is selected randomly between
        5 - 10 % of the population size. These many top agents will
        qualify for next generation.
        
        now, 1 % of the agents from the unselected agents pool is selected
        in random and made to come into the survivor agents group as 
        wildcard entry
        
        all the unselected agents are deleted (killed ?)
        now the current population is used to create new children
        by calling a deamon function aSexualRep, which returns a
        new agentObj as a child when a parent agentObj is sent
        this new child-agentObj will inherit the fitness value and
        slightly modified from its parent
        """
        
        try:
            if(self.survival > 0.95):
                survivalPerc = 0.95
                
            numberOfSurvivors = int((random.uniform(self.survival, self.survival+0.05) * self.agentCount))                      
            if(numberOfSurvivors < 1):
                numberOfSurvivors = 1

            listOfAgents = [(agent.agentID, agent.fitness) for agent in
                            [deamon.getAgent(self.sessID, agentID) for agentID in
                             deamon.getCurrGen(self.sessID)]]

            listOfAgents.sort(key=lambda x: x[1], reverse=True)
            unselected = listOfAgents[numberOfSurvivors:]
            wildCardEntries = random.sample(unselected, int(len(unselected)*0.01))
            finalUnselected = [agent for agent in unselected if(agent not in wildCardEntries)]

            for agent in finalUnselected:
                deamon.deleteAgent(self.sessID, agent[0])

            currPop = list(deamon.getCurrGen(self.sessID))
            itr = 0
            while(len(deamon.getCurrGen(self.sessID)) < self.agentCount):
                self.updateAgent(deamon.aSexualRep(self, self.getAgent(currPop[itr])))
                itr = (itr + 1)%(len(currPop))

        except Exception as e:
            print("gaDiscrete.createNextGen failed with error as : {}".format(e))
            
    def resetEnv(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Deletes all the agents in the current session
        
        This function effectively resets the session to the
        "Just created form" all the meta data files along with previous
        agents are deleted (killed ?). Uses the deamon (pun intended)
        functions setSession which registeres this session for future use
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
            
        except Exception as e:
            print("gaDiscrete.resetEnv failed with error as : {}".format(e))
            

    def delete(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Closes and deletes the current session
        
        As the name of the function says, this function deletes all of
        the meta data generated by this session and effectively deletes
        this session uses the deamon data GA_UTIL_DIR
        """

        try:
            sessDir = deamon.GA_UTIL_DIR + "/utilFiles/tmp" + str(self.sessID)
            shutil.rmtree(sessDir)
            del self
            
        except Exception as e:
            print("gaDiscrete.delete failed with error as : {}".format(e))
