Name: Jennifer Finaldi
CSC665-Assignment04

Files Modified: models.py

Topic: Machine Learning

Description:
	The Provided Code (Part I) section combined with the instructions for Question 1
make this assignment very straightforward. For the run() function I looked at the
nn.DotProduct definition in nn.py and figured out what order and formats the arguments
needed to be and just plugged it into the function. For the get_prediction() function,
that was also pretty easy, as it just required getting the dot product just like in 
the run() function, only we convert the result to a scalar before checking the sign and
returning the result. The train() function included a big hint in the Provided Code section,
so I copied and pasted that for-loop and then worked from there. The biggest challenge was
figuring out what the x, y represent and how to use them to determine if we keep training
or end the function. It took me a little while to figure out that y was still in node
format and needed to be converted to a scalar, since the prediction of x already returns
a scalar. Another mistake I made was forgetting that batch_size wasn't defined
when I pasted the sample code, so I had to define that as 1 in order for it to work. 
Approx Time Spent: 1hr