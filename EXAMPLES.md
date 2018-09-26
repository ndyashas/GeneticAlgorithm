# Examples of ga2
Currently [ga2](../) can be used for most of the discrete optimisation problems. To run the following examples, you will have to copy these files to the parent directory of project root.
```
$ cp examples/<example-code>.py ../
$ cd ../
$ python3 <example-code>.py
```

### Agent vs Agent , intra evaluation
In some cases, we might need to find the best agent in an environment by pitting against 2 agents of the same environment and measure the fittest, one such simple programming template is given in [agent2vs2.py](GeneticAlgorithm/examples/agent2vs2.py) . This program needs to be modified to accommodate the external fitness function evaluate .
  
  ### Single performance evaluation
  In this case, each agent is sent out as an object where the agent's fitness is updated externally and sent back to session. After all the agents have been sent out and got back, the next generation is generated, example for which is in [singleAgentUpdate.py](GeneticAlgorithm/examples/singleAgentUpdate.py)

### Current Development
I have made the example templates as shown above for now.
Proposals of new ideas or scenarios is a welcome !