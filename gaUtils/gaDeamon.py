# This is the lower level deamon that is used to do
# all the dirty jobs and make it look tidy to the
# people above .. sigh . well see the program for yourself

import os
import sys
import time
import random
import pickle

import ga2.gaUtils.AgentClass as AgentClass
GA_UTIL = os.path.dirname(os.path.realpath(__file__))


def getNewSessionID():
    """
    INPUT       : None
    OUTPUT      : New SessionID

    DESCRIPTION : Returns a new SessionID , or 0 when its the
                  first session
    """

    lock()
    try:
        
        sessFp = open(GA_UTIL+"/utilFiles/SESSIONNEXT.smtf", "r")
        sessID = int(sessFp.readline())
        sessFp.close()

    except Exception:
        print("Generating first session")
        sessID = 0
    
    try:
        sessFp = open(GA_UTIL+"/utilFiles/SESSIONNEXT.smtf", "w")
        sessFp.write(str(sessID+1))
        sessFp.close()

    except Exception:
        print("Error updating the SESSIONNEXT.smtf file")

    unlock()
    lock(sessID)
    unlock(sessID)
    return(sessID)


def isLocked(sessID=None):
    """
    INPUT       : sessID = None
    OUTPUT      : current status of the lock based on 
                  sessIDx

    DESCRIPTION : checks the locks, based on sessID
    """

    if(sessID is not None):
        smtf = "tmp" + str(sessID) + "/LOCK.smtf"
    else:
        smtf = "SESSIONLOCK.smtf" 
    
    try:
        lckfp = open(GA_UTIL+"/utilFiles/"+smtf, "r")
        lckpos = int(lckfp.readline())
        lckfp.close()

    except Exception:
        lckpos = 0

    return(lckpos)


def lock(sessID=None):
    """
    INPUT       : sessID = None
    OUTPUT      : returns 1 if locked, 0 on error

    DESCRIPTION : locks the session files if sessID is passed
                  else , does it for the entire session
    """

    while(isLocked(sessID)):
        time.sleep(0.5)

    if(sessID is not None):
        smtf = "tmp" + str(sessID) + "/smtf/LOCK.smtf"
    else:
        smtf = "SESSIONLOCK.smtf" 
        
    try:
        lckfp = open(GA_UTIL+"/utilFiles/"+smtf, "w")
        lckfp.close()
    
    except Exception:
        os.mkdir(GA_UTIL+"/utilFiles/"+"tmp"+str(sessID))
        os.mkdir(GA_UTIL+"/utilFiles/"+"tmp"+str(sessID)+"/smtf")
        os.mkdir(GA_UTIL+"/utilFiles/"+"tmp"+str(sessID)+"/dnaPool")
        
    lckval = 1
    lckfp = open(GA_UTIL+"/utilFiles/"+smtf, "w")
    lckfp.write(str(lckval))
    lckfp.close()
    return(lckval)


def unlock(sessID=None):
    """
    INPUT       : sessID = None
    OUTPUT      : 1 on successful unlocking 0 on unsuccessful

    DESCRIPTION : unlocks the session files if sessID is passed
                  else , does it for the entire session
    """

    if(sessID is not None):
        smtf = "tmp" + str(sessID) + "/smtf/LOCK.smtf"
    else:
        smtf = "SESSIONLOCK.smtf"

    try:
        lckfp = open(GA_UTIL+"/utilFiles/"+smtf, "w")
        lckfp.write(str(0))
        lckfp.close()
        
    except Exception:
        print("Couldnt unlock file !")
        return(0)
    
    return(1)


def getCurrGen(sessID):
    """
    INPUT       : sessID
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    try:
        cgfp = open(GA_UTIL+"/utilFiles/tmp"+str(sessID)+"/smtf/VALID.smtf", "rb")
        currImg = pickle.load(cgfp)
        cgfp.close()
    except Exception:
        #print("error in getting the curr gen")
        currImg = set()

    return(currImg)


def setCurrGen(sessID, agentList):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    try:
        cgfp = open(GA_UTIL+"/utilFiles/tmp"+str(sessID)+"/smtf/VALID.smtf", "wb")
        pickle.dump(agentList, cgfp)
        cgfp.close()
    except Exception:
        print("error in setting curr gen")
        return(0)
    return(1)


def storeAgent(agentObj):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    
    currAgents = getCurrGen(agentObj.sessID)

    try:
        tpfp = open(GA_UTIL+"/utilFiles/tmp"+str(agentObj.sessID)+"/dnaPool/dna"
                    +str(agentObj.agentID)+".dna", "wb")
        pickle.dump(agentObj, tpfp)
        tpfp.close()
        currAgents.add(agentObj.agentID)
    except Exception:
        print("error in store agent, couldnt wb")
        return(0)
    
    setCurrGen(agentObj.sessID, currAgents)
    return(agentObj.agentID)


def generateAgentID(sessID):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    try:
        nextfp = open(GA_UTIL+"/utilFiles/tmp"+str(sessID)+"/smtf/NEXTID.smtf", "r")
        Idp = int(nextfp.readline())
        nextfp.close()
    except Exception:
        #print("error in generate Agent ID, couldnt read")
        Idp = 0

    try:
        nextfp = open(GA_UTIL+"/utilFiles/tmp"+str(sessID)+"/smtf/NEXTID.smtf", "w")
        nextfp.write(str(Idp+1))
        nextfp.close()
        return(Idp)

    except Exception:
        print("error in generate agent ID, couldnt write")
        return(-1)



def createAgent(sessID):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    lock(sessID)
    agent = AgentClass.AgentDna()
    agent.sessID = sessID
    agent.agentID = generateAgentID(sessID)
    agent.dna = None
    agent.fitness = 0

    storeAgent(agent)
    unlock(sessID)

if(__name__ == "__main__"):
    pass
