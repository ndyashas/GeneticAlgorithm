import time
import math
import random
import ga2.gaDisc as gad


def fitnessFun(agentObj, target, spread):
    return((spread)-(meanSquareError(agentObj.dna, target)))

def meanSquareError(target, op):
    error = 0
    for i in range(len(target)):
        error += (op[i] - target[i])**2

    error = math.sqrt(error/len(target))
    return(error)


if(__name__ == "__main__"):
    # running this file as main
    TARGET_VECTOR_LEN = 100
    
    SPREAD = 10
    target = [random.uniform(0, SPREAD) for i in range(TARGET_VECTOR_LEN)]
    NUMBER_OF_EPOCH = 500000
    NUMBER_OF_AGENTS = 200
    NUMBER_OF_PARAM = len(target)
    SURVIVAL_RATE = 0.01
    MUTATION_RATE = 0.1
    GENE_COPY = 0.95
    GEN_MODE = 'S'
    MODE = 'UNSAFE'
    VAL_TYPE = 'FLOAT'
    
    try:
        sess = gad.Session(agentCount=NUMBER_OF_AGENTS,
                           numParam=NUMBER_OF_PARAM,
                           spread = SPREAD,
                           genecopy = GENE_COPY,
                           survival=SURVIVAL_RATE,
                           mutation=MUTATION_RATE,
                           generateMode=GEN_MODE,
                           mode=MODE,
                           valType=VAL_TYPE)
        sess.init()
    
        epoch = 0
        start = time.time()
        while(epoch < NUMBER_OF_EPOCH):
            
            # Code for getting a single agent from current environment
            currGen = sess.getAllAgents()
            for agentID in currGen:
                # Update the agent's fitness value
                agent = sess.getAgent(agentID)
                agent.fitness = fitnessFun(agent, target, SPREAD)
                sess.updateAgent(agent)

            # Display epoch details
            # Code for printing the details of the epoch
            print("")
            print("Epoch number {} session {} ****************".format(epoch, sess.sessID))
            print("Average fitness is      {}".format(sess.getAverageFitness()))
            print("maximum fitness is      {}".format(sess.getBestAgent().fitness))
            print("best agent agentID is   {}".format(sess.getBestAgent().agentID))
            error = (meanSquareError(target, sess.getBestAgent().dna)/(SPREAD))*100
            print("Error   % is            {}".format(error))
            
            #print("Best agent              {}".format(sess.getBestAgent().dna))
            #print("Target agent            {}".format(target))
            # Generates the next generation
            sess.createNextGen()
            epoch += 1
            if(error < 5):
                break
      
    except Exception as e:
        print("Exception cought with message as {}".format(e))

    finally:
        sess.delete()
    
    
    stop = time.time()
    sec = stop - start
    hours = sec // 3600
    sec = sec % 3600
    mins = sec // 60
    sec = sec % 60
    print("Total time taken is {}:{}:{} Hours".format(int(hours), int(mins), int(sec)))
