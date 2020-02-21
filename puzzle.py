import numpy as np
import time
# initial = np.array([[1,2,3],[4,0,5],[7,8,6]], dtype=np.int8)
# initial = np.array([[1,0,3],[4,2,5],[7,8,6]], dtype=np.int8) ##3
initial = np.array([[4,5,0],[2,3,8],[1,7,6]], dtype=np.int8) ###16
final = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype=np.int8)

class PuzzleSolver():
	def __init__(self, initialStateOfPuzzle):
		self.initial = initialStateOfPuzzle
		self.final = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype=np.int8)
		self.current_state = None
		self.setCombos()
		## Data structure : [ node_id , child_id , parent_id ]
		self.main_data = [[0,0,0]]
		self.new_state = None
		## All states will be saved here
		self.all_states_ = [self.initial]
		self.node = 0
		## Keep track of zero tile
		self.pastMoves = [(0,0)]
		## Flag which will indicate whether puzzle is solved or not
		self.solved = False
		## Saved where each node starts and ends
		self.startEndIndexOfNode = [[0,0]]
		self.solved_state = None

	def find_blank(self, current_state):
		for i in range(current_state.shape[0]):
			for j in range(current_state.shape[1]):
				if current_state[i,j]==0:
					return (i,j)
		return (0,0)
	