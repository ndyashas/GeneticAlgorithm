"""
This program impliments the discrete genetic algorithm
here, Discrete means that the new generation is generated
all at the same time by considering the top agents at that
given point.
"""

import os
import ga2
import shutil
import random
import ga2.gaUtils.gaDaemon as daemon


class Session:
    """
    This is the session class which is used to access all
    the agents in the current session, invoke different
    functions on this session and setting session
    parameters. This class also holds the meta data of the
    current session while using the 'UNSAFE' mode option
    """

    def __init__(self,sessID=None, agentCount=100, numParam=10, fixParam=True,
                 spread=2, survival=0.05, genecopy=0.9, mutation=0.01, generateMode='A',
                 mode='UNSAFE', valType='FLOAT'):
        

        self.sessID        = daemon.getNewSessionID()
        self.spread        = spread
        self.valType       = valType
        self.numParam      = numParam
        self.fixParam      = fixParam
        self.mutation      = mutation
        self.genecopy      = genecopy
        self.survival      = survival
        self.agentCount    = agentCount
        self.generateMode  = generateMode
        
        self.currGen       = set()
        self.agentBasket   = dict()
        self.nextAgentID   = 0
        self.lock          = 0
        self.mode          = mode
        
        
    def init(self):
        """
        INPUT       : None
        OUTPUT      : None

        DESCRIPTION : Initializes the session with agents
        """
        
        try:
            for i in range(self.agentCount):
                agentObj = daemon.createAgent(self)
        
        except Exception as e:
            print("gaDisc.init failed with error as : {}".format(e))

            
    def getAllAgents(self):
        """
        INPUT       : None
        OUTPUT      : Returns all the current AgentIDs of all the active
                      agents in a list, or None on error

        DESCRIPTION : Self explanatory from OUTPUT
        """
        
        try:
            toRet = daemon.getCurrGen(self)
        except Exception as e:
            print("gaDisc.getAllAgents failed with error as : {}".format(e))
            toRet = None
            
        return(toRet)

    
    def getAgent(self, agentID):
        """
        INPUT       : AgentID
        OUTPUT      : Returns the agent with the given AgentId, 
                      None on error

        DESCRIPTION : Self explanatory from OUTPUT
        """

        try:
            agentObj = daemon.getAgent(self, agentID)
            return(agentObj)
        
        except Exception as e:
            print("gaDisc.getAgent failed with error as : {}".format(e))
            return(None)
        
        
    def updateAgent(self, agentObj):
        """
        INPUT       : Agent object
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Updates the status of Agent in the current session
        """

        try:
            return(daemon.storeAgent( self, agentObj))
        
        except Exception as e:
            print("gaDisc.updateAgent failed with error as : {}".format(e))
            return(None)
    
    def getBestAgent(self):
        """
        INPUT       : None
        OUTPUT      : Returns the Agent with the best fitness value
                      at present , and None on error

        DESCRIPTION : Self explanatory from OUTPUT

        This is used to retrieve the best agent in the current
        pool of agents based on their fitness value with
        higher fitness corresponding to being better
        uses daemon functions getCurrGen, getAgent
        """

        try:
            
            bestAgent = None
            currGen = daemon.getCurrGen(self)
            for agentID in currGen:
                agent = daemon.getAgent(self, agentID)
                if((bestAgent is None) or (bestAgent.fitness < agent.fitness)):
                    bestAgent = agent
                    
        except Exception as e:
            print("gaDisc.getBestAgent failed with error as : {}".format(e))
            bestAgent = None
        
        return(bestAgent)

    
    def getAverageFitness(self):
        """
        INPUT       : None
        OUTPUT      : Returns the current avegare of the fitness value
                      of all the agents in the session.

        DESCRIPTION : Self explanatory from OUTPUT

        This function is used to get the average fitness value of
        agents in the current session, this uses daemon functions
        getCurrGen, getAgent
        """

        try:
            totalFitness = 0
            currGen = daemon.getCurrGen(self)
            for agentID in currGen:
                totalFitness += daemon.getAgent(self, agentID).fitness

        except Exception as e:
            print("gaDisc.getAverageFitness failed with error as : {}".format(e))
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
        by calling a daemon function aSexualRep, which returns a
        new agentObj as a child when a parent agentObj is sent
        this new child-agentObj will inherit the fitness value and
        slightly modified from its parent, (Needs optimisation).
        """
        
        try:
            if(self.survival > 0.95):
                survivalPerc = 0.95
                
            numberOfSurvivors = int((random.uniform(self.survival, self.survival+0.05) * self.agentCount))                      
            if(numberOfSurvivors < 1):
                numberOfSurvivors = 1

            listOfAgents = [(agent.agentID, agent.fitness) for agent in
                            [daemon.getAgent(self, agentID) for agentID in
                             daemon.getCurrGen(self)]]

            listOfAgents.sort(key=lambda x: x[1], reverse=True)
            unselected = listOfAgents[numberOfSurvivors:]
            # wildcard zero
            wildCardEntries = random.sample(unselected, int(len(unselected)*0.00))
            finalUnselected = [agent for agent in unselected if(agent not in wildCardEntries)]

            for agent in finalUnselected:
                daemon.deleteAgent(self, agent[0])

            currPop = list(daemon.getCurrGen(self))
            itr = 0
            while(len(daemon.getCurrGen(self)) < self.agentCount):
                if(self.generateMode == 'A'):
                    self.updateAgent(daemon.aSexualRep(self, self.getAgent(currPop[itr])))
                else:
                    self.updateAgent(daemon.sexualRep(self, self.getAgent(currPop[itr]),
                                                      self.getAgent(currPop[(itr + 1)%(len(currPop))])))
                itr = (itr + 1)%(len(currPop))
        
        except Exception as e:
            print("gaDisc.createNextGen failed with error as : {}".format(e))

                        
    def resetEnv(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, None on failure

        DESCRIPTION : Deletes all the agents in the current session
        
        This function effectively resets the session to the
        "Just created form" all the meta data files along with previous
        agents are deleted (killed ?). Uses the daemon (pun intended)
        functions setSession which registeres this session for future use
        """

        if(self.mode == 'SAFE'):
            try:            
                sessDir = daemon.GA_UTIL_DIR + "/utilFiles/tmp" + str(self.sessID)
                shutil.rmtree(sessDir+"/smtf")
                shutil.rmtree(sessDir+"/dnaPool")
                os.mkdir(sessDir+"/smtf")
                os.mkdir(sessDir+"/dnaPool")
                fp = open(sessDir+"/smtf/LOCK.smtf", "w")
                fp.write(str(0))
                fp.close()
                daemon.setSession(self)
                
            except Exception as e:
                print("gaDisc.resetEnv failed with error as : {}".format(e))
        else:
            self.currGen       = set()
            self.agentBasket   = dict()
            self.nextAgentID   = 0
            self.lock          = 0


    def delete(self):
        """
        INPUT       : None
        OUTPUT      : Returns 1 on success, 0 on failure

        DESCRIPTION : Closes and deletes the current session
        
        As the name of the function says, this function deletes all of
        the meta data generated by this session and effectively deletes
        this session uses the daemon data GA_UTIL_DIR
        """

        if(self.mode == 'SAFE'):
            try:
                sessDir = daemon.GA_UTIL_DIR + "/utilFiles/tmp" + str(self.sessID)
                shutil.rmtree(sessDir)
                del self
            
            except Exception as e:
                print("gaDisc.delete failed with error as : {}".format(e))
        else:
            del self
                
