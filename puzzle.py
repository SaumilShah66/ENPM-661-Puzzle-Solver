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
	
	### keys generated which indicates the possible movements on the basis of current position of blank tile
	def setCombos(self):
		for_00 = [(0,1), (1,0)]
		for_01 = [(0,0), (0,2), (1,1)]
		for_02 = [(0,1), (1,2)]
		for_10 = [(0,0), (1,1), (2,0)]
		for_11 = [(0,1), (1,0), (1,2), (2,1)]
		for_12 = [(0,2), (1,1), (2,2)]
		for_20 = [(1,0), (2,1)]
		for_21 = [(2,0), (1,1), (2,2)]
		for_22 = [(2,1), (1,2)]
		self.all_combi = [[for_00,for_01,for_02],[for_10,for_11,for_12],[for_20,for_21,for_22]]
		pass

	### Returns possible combinations for a given zero position
	def possible_combination(self, zero_position):
		return self.all_combi[zero_position[0]][zero_position[1]]

	## pos1 -- (x,y)  ----- pos2 -- (new_x, new_y)
	## state_to_change ----- array
	## return new_array
	def swap_values(self, state_to_change, old_pos_of_zero, new_pos_of_zero):
		new_state = np.copy(state_to_change) ### Creating a copy for new state
		## Swapping the values
		new_state[old_pos_of_zero] = new_state[new_pos_of_zero] 
		new_state[new_pos_of_zero] = 0
		return new_state

	def giveNewStates(self, oldState, pos):
		newMoves = self.possible_combination(self.find_blank(current_state))
		# newMoves.remove(oldState)
		local_states = []
		for move in newMoves:
			self.pastMoves.append(move)
			newState = self.swap_values(oldState, pos, move)
			if not self.checkGoal(newState):
				if not self.checkStateInData(newState):
					local_states.append(newState)
		return local_states

	#### Checks if state is already achieved in the enrire tree
	def checkStateInData(self, check_state):
		for s in self.all_states_:
			if np.array_equal(s, check_state):
				return False
			else:
				pass
		self.all_states_.append(check_state)
		return True

	#### Checks if goal is reached
	def checkGoal(self, state):
		return np.array_equal(state, self.final)

	def firstMove(self, state):
		current_state = np.copy(state)
		current_blank = self.find_blank(current_state)
		combos_for_current_state = self.possible_combination(current_blank)
		start = 1
		for child_index in range(len(combos_for_current_state)):
			temp_state = self.swap_values(current_state, current_blank, combos_for_current_state[child_index])
			if self.checkGoal(temp_state):
				self.main_data.append([1,child_index+1,0])
				self.solved_state = [1,child_index+1,0]
				break
			else:
				self.all_states_.append(temp_state)
				self.pastMoves.append(current_blank)
				self.main_data.append([1,child_index+1,0])
				pass
			pass
		self.startEndIndexOfNode.append([start, child_index+1])
		pass

	def solvePuzzle(self):
		self.firstMove(self.initial)
		current_node = 1
		child_index = self.main_data[-1][1]+1
		while (not self.solved):
			current_node += 1
			new_states = []
			print("Node number : "+str(current_node))
			s, e = self.startEndIndexOfNode[current_node-1][0] , self.startEndIndexOfNode[current_node-1][1] +1
			print("start = "+str(s))
			print("end = "+str(e))
			for parent_ids in range(s,e):
				if not self.solved:
					current_state_ = self.all_states_[parent_ids]
					current_blank = self.find_blank(current_state_)
					combos_for_current_state = self.possible_combination(current_blank)
					past_move = self.pastMoves[parent_ids]
					# print(past_move, combos_for_current_state)
					# print(self.pastMoves)
					# print("last_move : " + str(past_move))
					# print(past_move , combos_for_current_state)
					# combos_for_current_state.remove(past_move)
					for newpose in combos_for_current_state:
						if not self.solved:
							# print(str(parent_index))
							temp_state = self.swap_values(current_state_, current_blank, newpose)
							if self.checkGoal(temp_state):
								print("Found the match")
								print(temp_state)
								self.solved = True
								self.solved_state = [current_node , child_index, parent_ids]
								self.main_data.append([current_node , child_index, parent_ids])
								self.all_states_.append(temp_state)
								break
							elif self.checkStateInData(temp_state):
								# print(temp_state)
								self.pastMoves.append(current_blank)
								self.main_data.append([current_node , child_index, parent_ids])
								child_index += 1
							else:
								pass
			self.startEndIndexOfNode.append([e, child_index-1])
			print(str(child_index)+" ran")
		pass

	def backTrack(self):
		self.bestMoves = []
		self.bestMoves.append(self.final)
		stateData = self.solved_state
		while stateData[0]>0:
			self.bestMoves.append(self.all_states_[stateData[2]])
			stateData = self.main_data[stateData[2]]
		self.bestMoves.reverse()
		return self.bestMoves
