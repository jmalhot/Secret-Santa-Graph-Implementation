#===========================================================================================================================================
#  File Name		- gift_exchange.py	
#  Author	   		- Jatin Malhotra
#  When			  	- 15th Sep 2018
#  Reference   		- Secret Santa Graph Theory
#  Dependencies		- pip install ortools
#===========================================================================================================================================


#===========================================================================================================================================
# Import Libraries
#===========================================================================================================================================

from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp



#===========================================================================================================================================
#  Function Name	- REGISTER()
#  Description 		- Adds a new family member and a spouse for Gift Exchange Program:
#==========================================================================================================================================

def register():	

	new_member = input("Enter Member Name \n");
	new_member_partner = input("Enter Partner Name (Enter -1 if Single or Not having spouse) \n");
		
			
	members.append(new_member);
	members_partner.append(new_member_partner);
		
	members.append(new_member_partner);
	members_partner.append(new_member);
		
			
	arr_len=len(members)
		
	#print ("members count is :"+arr_len);
	choice = input("Do you wish to add more members: yes/no \n");
	
	if(choice.upper()== "YES"):
		register();
	else:
		game_choice = input("Do you wish to start a game: yes/no \n");
		if (game_choice.upper()=="YES"):
			play_game();

	  
	  
#===========================================================================================================================================
#  Function Name	- PLAY_GAME()
#  Description 		- Uses CP programming technique to list all possible permutations of how gifts can be exchanged among members.
#  Reference		- Uses Secret Santa Graph Theory 
#==========================================================================================================================================
def play_game():

	
	#========================================================================
	# Create CP solver.
	#========================================================================
	solver = pywrapcp.Solver('Gift Exchange Application');

	
	#========================================================================
	# Variables.
	# #Couples and Single
	#========================================================================
	n_no_single = 8;
	M = n_no_single + 1;

	#========================================================================
	# The matrix version of earlier rounds. 
	# M means that no earlier Santa has been assigned.
	#========================================================================
	
	rounds_no_single = [
	  # N  A  R  M  El J  L  Ev
	  [0, M, 3, M, 1, 4, M, 2],  # Nikhil
	  [M, 0, 4, 2, M, 3, M, 1],  # Anjali
	  [M, 2, 0, M, 1, M, 3, 4],  # Rajeev
	  [M, 1, M, 0, 2, M, 3, 4],  # Meera
	  [M, 4, M, 3, 0, M, 1, 2],  # Eleena
	  [1, 4, 3, M, M, 0, 2, M],  # Johny
	  [M, 3, M, 2, 4, 1, 0, M],  # Lina
	  [4, M, 3, 1, M, 2, M, 0]   # Evan
	];


	print("rounds_no_single",rounds_no_single);
	

	n = n_no_single;
	Nikhil, Anjali, Rajeev, Meera, Eleena, Johny, Lina, Evan = list(range(n));
	rounds = rounds_no_single;


	M = n + 1;

	#========================================================================
	# Family Member List
	#========================================================================
	members = [
	  'Nikhil', 'Anjali', 'Rajeev', 'Meera', 'Eleena', 'Johny', 'Lina', 'Evan', 'Single'
	];

	#========================================================================
	# Spouse List: 
	# member at ith position in members[] has a spouse at ith position in members_partner[], 
	# if members has no spouse than put -1 instead of spouse name
	#========================================================================
	members_partner = [
	  Anjali,  # Nikhil
	  Nikhil,  # Anjali
	  Meera,   # Rajeev
	  Rajeev,  # Meera
	  Johny,   # Eleena
	  Eleena,  # Johny
	  Evan,    # Lina
	  Lina,    # Evan
	  -1       # Single, has no spouse
	];

	#========================================================================
	# Declare variables
	#========================================================================
	santas = [
			 solver.IntVar(0, n - 1, 'santas[%i]' % i) for i in range(n)
			 ];
	
	santa_distance = [
					 solver.IntVar(0, M, 'santa_distance[%i]' % i) for i in range(n)
					 ];
					 

	#========================================================================
	# Total of 'distance', to maximize
	#========================================================================
	z = solver.IntVar(0, n * n * n, 'z');

	
	#========================================================================
	# Add Constraints
	#========================================================================
	
	solver.Add(solver.AllDifferent(santas));

	solver.Add(z == solver.Sum(santa_distance));

	#========================================================================
	# RULE 1 - You can't draw your own name
	#========================================================================
	# (i.e. ensure that there are no fix-point in the array.)
	for i in range(n):
		solver.Add(santas[i] != i);	

	#========================================================================
	# RULE 2 - You can’t draw the name of your partner if you have one
	#========================================================================
	for i in range(n):
		if members_partner[i] > -1:
			solver.Add(santas[i] != members_partner[i]);

	#========================================================================
	# Optimize 'distance' to earlier rounds:
	#========================================================================
	for i in range(n):
		solver.Add(santa_distance[i] == solver.Element(rounds[i], santas[i]));



	#========================================================================
	# Objective
	#========================================================================
	objective = solver.Maximize(z, 1);

	#========================================================================
	# Solution and Search
	#========================================================================
	db = solver.Phase(santas, solver.CHOOSE_MIN_SIZE_LOWEST_MIN,
					solver.ASSIGN_CENTER_VALUE);

	solver.NewSearch(db, [objective]);

	num_solutions = 0;
	
	while solver.NextSolution():
		num_solutions += 1;
		
		print();
		print('===============================');
		print('Solution :', num_solutions);
		print('Total Distances:', z.Value());
		print('Santas:', [santas[i].Value() for i in range(n)]);
		print('Description: ');
		
		for i in range(n):
			print('%s\tis a Santa to %s (distance %i)' % \
				(members[i],
				 members[santas[i].Value()],
				 santa_distance[i].Value()));
	print();

	#
	#========================================================================
	# Additional Information
	#========================================================================
	print('num_solutions:', num_solutions);
	print('failures:', solver.Failures());
	print('branches:', solver.Branches());
	print('WallTime:', solver.WallTime(), 'ms');

	
	

#===========================================================================================================================================
#  Function Name	- MAIN()
#  Description 		- Main function performs two tasks:
#						1) Registers a new member - REGISTER()
#					   (For sake of simplicity, I have skipped the automated registration process and assumed 8 members with a spouse list
#						2) Problem statement logic processing using CP programming - PLAY_GAME()
#==========================================================================================================================================

if __name__ == '__main__':

	print("Welcome to Gift Exchange Application \n");

	
	
	#========================================================================
	#Family Members Array
	#========================================================================
	members=[];
	
	#========================================================================
	# Spouse Array
	# Member at ith position in members[] has a spouse at ith position in members_partner[], 
	# if members has no spouse than put -1 instead of spouse name
	#========================================================================
	members_partner=[];

	
	#================================================================================================
	#------------------------------------------------------------------------------------------------
	# !IMPORTANT!
	# For sake of simplicity and ease in running script, registration part has been commented. 
	#------------------------------------------------------------------------------------------------
	#================================================================================================
	
	#print("Press 1 to register a new family member")
	#print("Press 2 to start a game\n");
	
	#choice = input("Enter Choice \n");
		
	#if (choice == "1"):
	#	register();
			
	#elif (choice == "2"):
		#play_game();
	
	#else:
	#	print ("INVALID_CHOICE.");
	
	#================================================================================================
	# Start Gift Exchange Application
	#================================================================================================
	play_game();
	