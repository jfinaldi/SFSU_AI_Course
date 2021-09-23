Name: Jennifer Finaldi
CSC665-Assignment03

Files Modified: analysis.py, qlearningAgents.py, valueIterationAgents.py

Topics: Markov Decision Process, Q-Learning, Value Iteration

Description: 
    The first thing that needed to be done for Q1 was to understand what the util.Counter()
is and how it is to be used. This is the counter that keeps track of all of the values that
correspond to a particular state. After, I decided to implement the two helper functions first, 
so that when I debug the runValueIteration function, I could have real values other than 0 to 
use for debugging. Compute Q values from values was just cycling through all the transition 
states and problems storing them in a list, and returning the sum of them. Compute Action 
From Values works similar only it cycles through all the possible actions, getting the Q 
value for each, and picking the action with the highest q value to return. Once these helper 
functions were implemented,runValueIteration was easier to implement. It gets all the states 
and the iterations passed in, runs iterations many loops that loop through all the states, 
and possible actions of those states, computing and storing Q values in a list, in which 
the largest value will be stored into the self.values dictionary-counter for that particular
state. For Q's 2 and 3, it was mostly trial and error, plugging in numbers until it worked.
For the Q learning agents, it was similar to the process of Q1, only there were differences,
such as the update function, which was added in order to create a real-time learning experience,
rather than relying on MDP models computed prior to the agent taking actions. These update 
functions used equations given in lecture slides for Q-updates. 
    
Approx Time Spent: 22 hrs