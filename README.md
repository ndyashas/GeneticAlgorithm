# Genetic Algorithm Utility for python

### What is Genetic Algorithm ?
Genetic Algorithm is inspired by the natural selection process in our environment. GA is very good for optimisation problems , read more about  [GA here](https://en.wikipedia.org/wiki/Genetic_algorithm) . 

### The ga2 module 
ga2 is a highly flexible and easy to use utility module implementing Genetic Algorithm. 

### Usage 
* clone or download this repository onto your machine
```
git clone https://github.com/yashasbharadwaj111/GeneticAlgorithm ga2
```
* import the Genetic Algorithm utility as 
```
import ga2.gaDiscrete as gad

session1 = gad.Session()
print(session1.sessID)
```
this should print the session ID of that session

### Development
A lot of work still needs to be done, which I hope will be done soon . 
The following list contains only gaDiscrete class' functions that are done , and those that need to be done.
* gaDiscrete
	- [x] initialize
	- [ ] getAgent
	- [ ] getAllAgents
	- [ ] updateAgent
	- [ ] getBestAgent
	- [ ] getAverageFitness
	- [ ] createNextGen
	- [ ] resetEnv
	- [ ] delete

Open to ideas , and contributions ! 
  