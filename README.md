# Genetic Algorithm Utility for python

### What is Genetic Algorithm ?
Genetic Algorithm is inspired by the natural selection process in our environment. GA is very good for optimisation problems , read more about  [GA here](https://en.wikipedia.org/wiki/Genetic_algorithm) . 

### The ga2 module 
ga2 is a highly flexible and easy to use utility module implementing Genetic Algorithm. 

### Installation
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

### Usage
ga2 is designed to be flexible and also simple to use for a variety of use cases, check the [EXAMPLES.md](EXAMPLES.md) for examples. Documentation will be done as soon as a stable stage is reached

### Current Development
A lot of work still needs to be done, which I hope will be done soon . 
The following list contains only gaDiscrete class' functions that are done , and those that need to be done.
* gaDiscrete
	- [x] init
	- [x] getAgent
	- [x] getAllAgents
	- [x] updateAgent
	- [x] getBestAgent
	- [x] getAverageFitness
	- [ ] createNextGen
	- [x] resetEnv
	- [x] delete

Open to ideas , and contributions ! 