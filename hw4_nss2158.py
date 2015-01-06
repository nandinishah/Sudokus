#!/usr/bin/env python
#coding:utf-8

from copy import deepcopy
import time

ROW = "ABCDEFGHI"
COL = "123456789"
domain = {}
q1 = []
q2 = []
count = 0

# Arcs: Get block of the cell to add arc to the elements of that block 
def getblock(row, column):
	if (row == 0 or row == 1 or row == 2) and (column==0 or column == 1 or column == 2):
		return(1)
	if (row == 0 or row == 1 or row == 2) and (column==3 or column == 4 or column == 5):
		return(2) 
	if (row == 0 or row == 1 or row == 2) and (column==6 or column == 7 or column == 8):
		return(3) 
	if (row == 3 or row == 4 or row == 5) and (column==0 or column == 1 or column == 2):
		return(4) 
	if (row == 3 or row == 4 or row == 5) and (column==3 or column == 4 or column == 5):
		return(5) 
	if (row == 3 or row == 4 or row == 5) and (column==6 or column == 7 or column == 8):
		return(6) 
	if (row == 6 or row == 7 or row == 8) and (column==0 or column == 1 or column == 2):
		return(7) 
	if (row == 6 or row == 7 or row == 8) and (column==3 or column == 4 or column == 5):
		return(8) 
	if (row == 6 or row == 7 or row == 8) and (column==6 or column == 7 or column == 8):
		return(9)


# Arcs: Generating the list of arcs for a cell based on its row, column and block
def Initialization(row, column):
	# Checking rows in the column
	for r in range(9):
		if row!=r:
			arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[column]))
			
	# Checking columns in the row
	for c in range(9):
		if column!=c:
			arc[ROW[row]+COL[column]].append(str(ROW[row])+str(COL[c]))

	# Checking block
	block = getblock(row, column)
	
	if block == 1:
		for r in range(0,3):
			for c in range(0,3):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 2:
		for r in range(0,3):
			for c in range(3,6):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 3:
		for r in range(0,3):
			for c in range(6,9):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))		
	elif block == 4:
		for r in range(3,6):
			for c in range(0,3):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 5:
		for r in range(3,6):
			for c in range(3,6):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 6:
		for r in range(3,6):
			for c in range(6,9):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 7:
		for r in range(6,9):
			for c in range(0,3):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 8:
		for r in range(6,9):
			for c in range(3,6):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))
	elif block == 9:
		for r in range(6,9):
			for c in range(6,9):
				if (row!=r) and (column!=c):
					arc[ROW[row]+COL[column]].append(str(ROW[r])+str(COL[c]))


# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j][0],
		print ""	
	# print "-----------------"

# AC-3: Removing the incosistent values based on arcs
def RemoveInconsistentValues(Xi, Xj):
	removed = False
	pointer1 = 0
	for di in domain[Xi]:
		for dj in domain[Xj]:
			if (di == dj and len(domain[Xj])==1):
				domain[Xi].pop(pointer1)
				pointer1 = pointer1-1
				removed = True
				break
		pointer1 = pointer1+1
	return removed

# Forward Checking
def valueValid(domainLocal, var, value):
	flag = 0
	arcArray = []
	count2 = 0
	arcArray = arc[var]
	while flag == 0 and count2<len(arcArray):
		for element in domainLocal[arcArray[count2]]:
			if value == element and len(domainLocal[arcArray[count2]])==1:
				flag = 1
				break
		count2 = count2+1
	if flag == 0:
		return True
	else:
		return False

# Recursive Backtracking (using AC-3)
def recursiveBacktracking(domainLocal):
	
	# Checking if sudoku has been solved -> len(domain) for all cells will be 1. If not cell for forward checking will be narrowed down using mrv.
	min = 10
	flag = 0
	for r in range(9):
		for c in range(9):
			# print domainLocal[ROW[r]+COL[c]]
			if len(domainLocal[ROW[r]+COL[c]])==0:
				return False
			if min>len(domainLocal[ROW[r]+COL[c]]) and len(domainLocal[ROW[r]+COL[c]])>1:
				min = len(domainLocal[ROW[r]+COL[c]])
				var = ROW[r]+COL[c]
				flag = 1
	if flag == 0:
		# Sudoku successfully solved!
		result = True
		# print "Sudoku "+str(count)+" by BT is "+str(result)
		printSudoku(domainLocal)
		# print time.time()
		# print "----------------------------------------------------"
		# print ""
		return result

	# If sudoku has still not been solved -> choose a valid value for the chosen cell (based on mrv) and reduce domain of other cells using AC-3
	for value in domainLocal[var]:
		if valueValid(domainLocal, var, value):
			domainLocal2 = deepcopy(domainLocal)
			domainLocal2[var]=[value]

			# AC-3
			q1 = []
			q2 = []
			for Xi in arc:
				t = arc[Xi]
				for Xj in t:
					q1.append(Xi)
					q2.append(Xj)
			while q1 !=[]:
				Xi = q1.pop(0)
				Xj = q2.pop(0)
				removed = False
				pointer1 = 0
				for di in domainLocal2[Xi]:
					for dj in domainLocal2[Xj]:
						if (di == dj and len(domainLocal2[Xj])==1):
							domainLocal2[Xi].pop(pointer1)
							pointer1 = pointer1-1
							removed = True
							break
					pointer1 = pointer1+1
				if removed == True:
					t = arc[Xi]
					for Xk in t:
						q1.append(Xk)
						q2.append(Xi)

			# Run backtracking again
			result = recursiveBacktracking(domainLocal2)
			
			# If sudoku solved -> Unfolding of the recursion occurs with True result
			if result == True:
				return result
	# If sudoku not possible to solve using Backtracking -> Unfolding of the recursion occurs with False result			
	return False






# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
	print "Error in reading the sudoku file."
	exit()


# 1.5 Attempt to solve sudoku using AC-3 and count number of sudokus solved by AC-3
count = 1
num_ac3_solved = 0
num_bt_solved = 0
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	# print time.time()
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
	domain = {ROW[i] + COL[j]: [] for i in range(9) for j in range(9)}
	arc = {ROW[i] + COL[j]: [] for i in range(9) for j in range(9)}
	
	# Initializing domain and arc for each non-zero element
	for row in range(9):
		for column in range(9):
			# Initializing domain of cells with already populated values
			if sudoku[ROW[row]+COL[column]] != 0:
				domain[ROW[row]+COL[column]].append(sudoku[ROW[row]+COL[column]])
				Initialization(row, column)
			# Initializing domain of cells with no initial value
			if sudoku[ROW[row]+COL[column]] == 0:
				for i in range(1,10):
					domain[ROW[row]+COL[column]].append(i)
				Initialization(row, column)

# Initializing queue q1 and q2 with all arcs	
	q1 = []
	q2 = []
	for Xi in arc:
		t = arc[Xi]
		for Xj in t:
			q1.append(Xi)
			q2.append(Xj)

	while q1 !=[]:
		Xi = q1.pop(0)
		Xj = q2.pop(0)
		if RemoveInconsistentValues(Xi, Xj):
			t = arc[Xi]
			for Xk in t:
				q1.append(Xk)
				q2.append(Xi)
	
	flag = 0
	for i in domain:
		if len(domain[i]) != 1:
			# print "Sudoku "+str(count)+" not solved by ac-3"
			flag = 1
			break
	if flag == 0:
		num_ac3_solved = num_ac3_solved+1
		# print "Sudoku "+str(count)+" solved by ac-3"
		printSudoku(domain)
		# print time.time()
		# print "----------------------------------------------------"
		# print ""

# 1.6 solve all sudokus by backtracking	
	# Running Backtracking and Forward search if AC-3 does not produce a result
	if flag ==1 :
		domainLocal = deepcopy(domain)
		result = recursiveBacktracking(domainLocal)
		if result == True: num_bt_solved = num_bt_solved+1
	
	flag = 0
	count = count + 1

# Printing final answer
# print ""
# print "----------------------------------------------------"
print "Number of sudokus solved by AC-3 = "+str(num_ac3_solved)
# print "Number of sudokus solved by Backtracking = "+str(num_bt_solved)
# print time.time()
# print "----------------------------------------------------"
print ""













