Name: Jennifer Finaldi
CSC665-Assignment02

Files Modified: multiAgents.py

Topics: Multi Agent Learning

Description: 
    This project ended up being a lot of tinkering, especially in parts 1 and 5. It took a 
while of playing with different values as maximizers and minimizers in order to find a balance
that yielded a good result. I tried to think of all of the things that could work to pacman's
advantage as well as disadvantage and then played with adding and subtracting them. It was a
lot of trial and error. For Q5, this same algorithm wouldn't work, so it ended up being a lot
more tinkering and tweaking of values, with the most notable addition being the random number
between -1 and 1 being added, in the case where two subtrees produced the same number, it
seemed like this was the reason pacman would get stuck. Also I decided to omit minimum ghost 
distance as a minimizer if there are no ghosts in the immediate vicinity of pacman, which 
helped reduce pacman's fear of the ghost going up as the score would decrease. For the minimax
agent, the greatest challenge was figuring out the depth and how this factors into the 
algorithm. As we analyze each potential successor action, the depth would increase with each
recursive call. I decided to create one function, minOrMax that would do either minimizing or
maximizing based on the value of a boolean parameter, in order to cut down on repeat code. 
This same code for minimax was able to be recycled for expectimax, only adding about 5 lines
of code to determine what value goes into the second position of the tuple in each successor. 
For AlphaBeta, I couldn't exactly recycle the code from the other two because it breaks the 
pruning effect. So I got rid of the getSuccessors function and put that code inside the minOrMax
function, when each legal action is getting iterated through. Pruning allows me to escape that 
process prematurely before all nodes have been explored, which was not possible in the previous
code structures. 

Approx Time Spent: 29 hrs