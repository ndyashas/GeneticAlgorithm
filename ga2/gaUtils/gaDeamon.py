# This is the lower level deamon that is used to do
# all the dirty jobs and make it look tidy to the
# people above .. sigh . well see the program for yourself

import os
import sys
import time
import random
import pickle

import ga2.gaUtils.AgentClass as AgentClass
GA_UTIL_DIR = os.path.dirname(os.path.realpath(__file__))


# current functions included are as follows:
#
# ** uses lock
# *
# 
# 1 ) ** getNewSessionID()
# 2 ) isLocked()
# 3 ) lock()
# 4 ) unlock()
# 5 ) getCurrGen()
# 6 ) setCuttGen()
# 7 ) ** storeAgent()
# 8 ) generateAgentID()
# 9 ) createAgent()
# 10) ** deleteAgent()
# 11) getAgent()
# 12) ** setSession()
# 13) getSession()
# 14) asexualRep()
# 15) mutateAgentObj()


def mutateAgentObj(agentObj, sess):
    """
    INPUT       : sessID
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """

    currDna = agentObj.dna
    itr = 0
    while((sess.mutation > random.random()) or (itr > int(len(currDna)/3))):

        if(0.5 > random.random()):
            mutateVal = (sess.mutation)*(10**(sess.spread))
        else:
            mutateVal = -1 * (sess.mutation)*(10**(sess.spread))
            
        currDna[random.randint(0, len(currDna)-1)] += mutateVal
        
    return(currDna)
    

def aSexualRep(sess, agentObj):
    """
    INPUT       : agentObj
    OUTPUT      : child agentObj

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """

    childDna = []
    
    itr = 0
    while(itr < len(agentObj.dna)):
        if(sess.genecopy < random.random()):
            childDna.append(random.randint(0, 10**(sess.spread)))
        else:
            childDna.append(agentObj.dna[itr])
        itr += 1
            
    childObj = createAgent(sess)
    childObj.dna = childDna
    childObj.fitness = agentObj.fitness
    childObj.dna = mutateAgentObj(childObj, sess)
    return(childObj)
        

def getSession(sessID):
    """
    INPUT       : sessID
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    try:
    
        cgfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)
                    +"/smtf/SESS.smtf", "rb")
        currImg = pickle.load(cgfp)
        cgfp.close()
    
    except Exception:
        print("error in getting the session {}".format(sessID))
        currImg = None
        
    print(currImg.agentCount)
    return(currImg)


def setSession(sessionObj):
    """
    INPUT       : sessionObj
    OUTPUT      : 1 on success 0 on failure

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    
    lock(sessionObj.sessID)
    #try:
    tpfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessionObj.sessID)
                +"/smtf/SESS.smtf", "wb")
    pickle.dump(sessionObj, tpfp)
    tpfp.close()
    '''
    except Exception:
        print("error in store of session, couldnt wb")
        return(0)
    '''
    unlock(sessionObj.sessID)
    
    return(1)


def getNewSessionID():
    """
    INPUT       : None
    OUTPUT      : New SessionID

    DESCRIPTION : Returns a new SessionID , or 0 when its the
                  first session
    """

    lock()
    try:
        
        sessFp = open(GA_UTIL_DIR+"/utilFiles/SESSIONNEXT.smtf", "r")
        sessID = int(sessFp.readline())
        sessFp.close()
    
    except Exception:
        print("Generating first session")
        sessID = 0
    
    try:
        sessFp = open(GA_UTIL_DIR+"/utilFiles/SESSIONNEXT.smtf", "w")
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
        if(not os.path.isdir(GA_UTIL_DIR+"/utilFiles")):
            os.mkdir(GA_UTIL_DIR+"/utilFiles")
        lckfp = open(GA_UTIL_DIR+"/utilFiles/"+smtf, "r")
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
        lckfp = open(GA_UTIL_DIR+"/utilFiles/"+smtf, "w")
        lckfp.close()
    
    except Exception:
        os.mkdir(GA_UTIL_DIR+"/utilFiles/"+"tmp"+str(sessID))
        os.mkdir(GA_UTIL_DIR+"/utilFiles/"+"tmp"+str(sessID)+"/smtf")
        os.mkdir(GA_UTIL_DIR+"/utilFiles/"+"tmp"+str(sessID)+"/dnaPool")
        
    lckval = 1
    lckfp = open(GA_UTIL_DIR+"/utilFiles/"+smtf, "w")
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
        lckfp = open(GA_UTIL_DIR+"/utilFiles/"+smtf, "w")
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
        cgfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)+"/smtf/VALID.smtf", "rb")
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
        cgfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)+"/smtf/VALID.smtf", "wb")
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
    lock(agentObj.sessID)
    try:
        tpfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(agentObj.sessID)+"/dnaPool/dna"
                    +str(agentObj.agentID)+".dna", "wb")
        pickle.dump(agentObj, tpfp)
        tpfp.close()
        currAgents.add(agentObj.agentID)
    except Exception:
        print("error in store agent, couldnt wb")
        return(0)
    
    setCurrGen(agentObj.sessID, currAgents)
    unlock(agentObj.sessID)
    return(agentObj.agentID)


def getAgent(sessID, agentID):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """

    try:
        tpfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)+"/dnaPool/dna"
                    +str(agentID)+".dna", "rb")
        agentObj = pickle.load(tpfp)
        tpfp.close()
    
    except Exception:
        print("Error couldnt retrieve error in getAgent()")
        agentObj = None
    
    return(agentObj)


def generateAgentID(sessID):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    try:
        if(not os.path.isdir(GA_UTIL_DIR+"/utilFiles")):
            os.mkdir(GA_UTIL_DIR+"/utilFiles")
        nextfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)+"/smtf/NEXTID.smtf", "r")
        Idp = int(nextfp.readline())
        nextfp.close()
    except Exception:
        Idp = 0

    try:
        nextfp = open(GA_UTIL_DIR+"/utilFiles/tmp"+str(sessID)+"/smtf/NEXTID.smtf", "w")
        nextfp.write(str(Idp+1))
        nextfp.close()
        return(Idp)

    except Exception:
        print("error in generate agent ID, couldnt write")
        return(-1)


def createAgent(sess):
    """
    INPUT       : None
    OUTPUT      : Agent object

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    
    agent = AgentClass.AgentDna(sess.numParam, sess.spread)
    agent.sessID = sess.sessID
    agent.agentID = generateAgentID(sess.sessID)

    storeAgent(agent)
    return(agent)

def deleteAgent(sessID, agentID):
    """
    INPUT       : sessID, agentID
    OUTPUT      : None

    DESCRIPTION : Creates and stores the newly created AgentDna
                  object in that particular session's directory
    """
    
    lock(sessID)
    try:
        currGen = getCurrGen(sessID)
        if(agentID in currGen):
            toDelFile = GA_UTIL_DIR + ("/utilFiles/tmp" + str(sessID)
                                   + "/dnaPool/dna" + str(agentID)
                                   +".dna")
            os.remove(toDelFile)
            currGen.remove(agentID)
            setCurrGen(sessID, currGen)
            
        else:
            print("Trying to delete an agent not present in the session")

    except Exception:
        print("delete Agent encountered an error")
        return(0)
    
    finally:
        unlock(sessID)
        
    return(1)
