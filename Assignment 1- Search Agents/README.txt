Name: Jennifer Finaldi
CSC665-Assignment01

Files Modified: search.py, searchAgents.py

Topics: Search Agents

Description:
	
	The implementation for the algorithms in search.py were achieved using the pseudo-code
from lecture slides and lectures. The most difficult part of this was figuring out the
structure of the frontier, what to put in it and when, and figuring out what the output
format should be. Originally it was assumed the path result would be a list of tuples 
representing a sequence of coordinates, and took quite a while to figure out that it was
just a list of directions for single steps. For searchAgents, the CornersProblem required
deciphering how we keep track of corners in the maze. I opted to track the corners that
remain to be visited, removing one as it is analyzed, until all corners are gone. The corners
heuristic was by far the biggest challenge of this project, and I had rewritten the function
several times before realizing it was actually a problem with the getSuccessors append
statement being indented when it shouldn't have, resulting in a non-zero h value upon goal. 
Once that was fixed, it worked. I originally had it returning the min manhattan distance,
yielding a 2/3 on the autograder, but changing it to max manhattan distance resulted in a
significantly lower amount of expanded nodes. For food heuristic, I originally tried using 
manhattan distance, but it didn't pass all the tests. I rewrote it several times with no
different result. Then looking over the code base a few times put maze distance on my radar,
so I tried using that instead and used trial and error to figure out which parameters it 
needed, before getting successful results. And for the last part, understanding the goal
test of AnyFoodSearchProblem was difficult, because I originally believed it was at a goal
when all of the food was eaten. When I realized the goal happens when a single food was 
consumed, it made sense to iterate through the grid using a list version of it, returning
true if pacman was sharing a space with an uneaten food in the list. The findPathToClosestDot
ended up being the most straightforward solution in this assignment because I could use one
of my search functions I created in search.py to get a path to a food. I tried a few
different searches and found that DFS did not work for it, but bfs, ucs, and A* all did.

Estimated hours spent on assignment: 40 