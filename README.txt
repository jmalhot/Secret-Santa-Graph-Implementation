#=========================================================
#  File Name		- README.txt
#  Author	   	- Jatin Malhotra
#  When			- 15th Sep 2018
#  Description 		- Gift Exchange Application
#  Reference        	- Secret Santa Graph Theory 
#=========================================================

-----------------------------------------------------------------------------------------------------
Solution Approach:-
The python implementation uses constraint programming library of Google OR-Tools
(OR-Tools library can be installed using PIP installer i.e. pip install ortools)
(OR-Tools can also be installed directly from https://developers.google.com/optimization/install/python/)

-----------------------------------------------------------------------------------------------------
Dependencies:- 
pip install ortools

-----------------------------------------------------------------------------------------------------
Configuration:- 
None

-----------------------------------------------------------------------------------------------------
Constraints:-
For the given use case, Following constrains are considered
- You can’t draw your own name
- You can’t draw the name of your partner if you have one

-----------------------------------------------------------------------------------------------------
Execution:-
script gift_exchange.py can be executed directly using command line


-----------------------------------------------------------------------------------------------------
Input:-
The implementation skips the input file (or automated member registration) for now, I currently assumed there are 8 persons and a spouse list.


-----------------------------------------------------------------------------------------------------
Output:-
Program displays all possible permutations on how gifts can be exchanged. The program chooses a Secret Santa for every name in the list.
An enhancement to this program can be made to identify the optimal solution among number the number of solutions available. 
For sake of simplicity, I have kept all the solutions at this time.


-----------------------------------------------------------------------------------------------------
Math Bonus Question:-
Ans:- 2N

