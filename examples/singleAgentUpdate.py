# This is the test client file of the ga2 module , here we
# try to test the module for any potential errors, as well
# as for its reliability. 

import random
import ga2.gaDiscrete as gad

if(__name__ == "__main__"):
    # running this file as main
    
    NUMBER_OF_EPOCH = 10

    try:
        sess = gad.Session(agentCount=5)
        sess.init()
        
        epoch = 0
        while(epoch < NUMBER_OF_EPOCH):

            # Code for printing the details of the epoch
            print("Epoch number {} ****************".format(epoch))
            print("Average fitness is            {}".format(sess.getAverageFitness()))
            print("Agent with maximum fitness is {}".format(sess.getBestAgent().agentID))

            # Code for getting a single agent from current environment
            currGen = sess.getAllAgents()
            for agentID in currGen:
                agent = sess.getAgent(agentID)

                # Send out the agent for performing and getting his/her fitness
                # evaluated and updated
                # ...

                # Here change the RHS accordingly
                agent.fitness = random.random()
                sess.updateAgent(agent)
                
            # Generates the next generation
            sess.createNextGen()
            epoch += 1
            
    except Exception as e:
        print("Exception cought with message as {}".format(e))

    finally:
        sess.delete()

