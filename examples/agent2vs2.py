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

            # Code for matching 2 agents against each other and changing fitness
            currGen = sess.getAllAgents()
            matches = [(agent1, agent2) for agent1 in currGen for agent2 in currGen]
            
            for players in matches:
                agent1 = sess.getAgent(players[0])
                agent2 = sess.getAgent(players[1])
                # play match based on the dna's you get of the two players
                # i.e players[0].dna and players[1].dna
                # ...

                # You need to update the fitness value of both the agents
                # Here change the RHS accordingly
                agent1.fitness = random.random()
                agent2.fitness = random.random()
                sess.updateAgent(agent1)
                sess.updateAgent(agent2)

            # Generates the next generation
            sess.createNextGen()
            epoch += 1
            
    except Exception as e:
        print("Exception cought with message as {}".format(e))

    finally:
        sess.delete()
