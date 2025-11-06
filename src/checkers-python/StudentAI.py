import Math
import random
from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
EXPLORATION_PARAM = 1 # C constant for UCT calculations
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)

        root = Node(None, None, moves)          # Create first node of the tree
        tree = MCTS(self.board)                 # Create tree structure

        move = tree.search(root)                # Return the best move to make from the root node
        self.board.make_move(move,self.color)   # Perform the move

        return move



class Node:
    def __init__(self, parent: Node, color: int, move: Move, moves: List[Move]) -> None:
        """ Initialize values of a Node """
        self.move = move            # The Move which brings you to this node
        self.parent = parent        # The Node that comes before this node
        self.children = []          # A list of Nodes representing the children nodes
        self.total_games = 0        # The number of times the node has been visited
        self.wins = 0               # The number of times the node results in a winning result
        self.untried_moves = moves  # A list of Moves that have not been made into a child node
        self.color = color          # The color of the player at this node
    
    def get_color(self) -> int:
        """ Returns color of node's turn """
        return self.color

    def get_parent(self) -> Node:
        """ Returns parent node of current node """
        return self.parent
    
    def get_untried_moves(self) -> List[Move]:
        """ Returns a list of moves not yet tried """
        return self.untried_moves

    def has_children(self) -> bool:
        """ Returns True if the node has at least one child node
                    False otherwise
        """
        return len(self.children) != 0

    def is_fully_expanded(self)-> bool:
        """ Returns True if the node has no more untried moves
                    False otherwise
        """
        return len(self.untried_moves) == 0

    def get_best_child(self, c = EXPLORATION_PARAM) -> Node:
        """ Returns the child with the best UCT value of the current node 
            UCT = w_i/s_i + c * sqrt(ln(s_p)/s_i)
                i = current node
                p = parent node
                w = win count
                s = total visit count
                c = exploration constant, larger = more exploration, smaller = more exploitation
            @return: Node representing the best move to take, which has the highest UCT value
        """
        best_child = None               # Start best child as none
        score = 0                       # Track UCT score of the best child
        for child in self.children:     # Run through each child node
            uct = (self.wins / self.total_games) + c * Math.sqrt(Math.ln(self.parent.total_games) / self.total_games)
            if uct > score:             # If the UCT is greater than the current best score, replace
                best_child = child
                score = uct
           
        if not best_child:              # If all children nodes have a value of 0, randomly select a node
            random.choice(self.children)
        return best_child
    
    def add_child(self, move: Move, moves: List[Move]) -> Node:
        """ Adds a new child node to the current node and
            removes the corresponding move from untried_moves
            @param:  move - Move representing the move that brings you to this node
                     moves - List of possible Moves from this node
            @return: Node corresponding to the newly created child node
        """
        new_node = Node(self, 3 - self.color, move, moves)
        self.children.append(new_node)
        self.untried_moves.remove(move)
        return new_node

    def add_children(self, moves: List[Move]) -> None:
        """ Creates children node for each move """
        for move in moves:
            self.add_child(move)

    def update_node(self, result: int) -> None:
        """ Updates the score of the node based on the result
            @param: result - reward value where 1 is a win, 0 is a loss
        """
        self.total_games += 1
        self.wins += result
    

class MCTS:
    def __init__(self, board: Board, num_simulations=500):
        """ Initialize values of a Monte Carlo Tree Search """
        self.num_simulations = num_simulations  # Number of iterations to run
        self.board = board                      # Reference to the game board
    
    def select(self, node: Node) -> Node:
        """ Select node to expand based on UCT 
            @param:  node - Node to start selection process from (root)
            @return: Deepest non-fully-expanded Node
        """
        while node.has_children() and node.is_fully_expanded(): # While node is nonterminal and fully expanded
            color = node.get_color()
            node = node.get_best_child()                        # Get best child using UCT
            self.board.make_move(node.get_move(), color)        # Perfom move
        return node

    def expand(self, node: Node) -> Node:
        """ Expand children of selected node 
            @param:  node - Node selected to expand
            @return: Newly created expanded child Node
        """
        if self.board.is_win(node.get_color()) != 0:                    # Node is terminal, no expansion possible
            return node
        move = random.choice(node.get_untried_moves())                  # Pick a random move to create expanded node
        self.board.make_move(move, node.get_color())                    # Perform move
        moves = self.board.get_all_possible_moves(3 - node.get_color()) # Get all possible moves for child node
        return node.add_child(move, moves)                              # Create child node
    
    def simulate(self, node: Node) -> int:
        """ Simulate games from child node 
            @param:  node - Node returned from expansion
            @return: value representing the reward from the result
                     1 if win, 0 if loss
        """
        i = 0                                                   # Tracks how many simulated moves were made
        color = node.get_color()                                # Tracks the color of the current move
        while self.board.is_win(color) == 0:                    # While no outcome has been determined yet
            moves = self.board.get_all_possible_moves(color)    # Get all possible moves according to color player
            move = random.choice(moves)                         # Randomly select a move
            self.board.make_move(move, color)                   # Perform move
            color = 3 - color                                   # Swap color, 1 if color was 2, 2 if color was 1
            i += 1                                              # Increase move counter by 1
        result = self.board.is_win(color)                       # -1 for tie, 1 for black win, 2 for white win
        for _ in range(i):                                      # Undo all moves back to child node
            self.board.undo()
        return 1 if node.get_color() == result or node.get_color() == -1 else 0 # 1 if winner is same as node color
                                                                                # or if tie, otherwise 0
    
    def backpropagate(self, node: Node, reward: int) -> None:
        """ Backpropagate and update statistics
            @param: node - child Node created from expansion
                    reward - win value of node, 1 if win/tie, 0 if loss
        """
        if node == None:                                  # If node is none, then this is the tree root node
            return
        self.board.undo()                                 # Undo move
        node.update_node(reward)                          # Update the values of the current node
        self.backpropagate(node.get_parent(), 1 - reward) # Propagate to previous node, flip reward value

    def select_move(self, node: Node) -> Move:
        """ Retrieves the best move to make at the current node/state
            @param:  node - Node representing current state, tree root node
            @return: Move representing the best move based on UCT value
        """
        return node.get_best_child().get_move()

    def search(self, node: Node) -> Move:
        """ Perform MCTS to find the best move to take at a specific turn
            @param:  node - Node representing current state, tree root node
            @return: Move representing best move based on UCT value
        """
        for _ in range(self.num_simulations): # Runs for specified number of iterations
            leaf = self.select()              # Select a leaf node to perform expansion
            child = self.expand(leaf)         # Create child node from leaf node
            reward = self.simulate(child)     # Simulate a game from the child node and retrieve the outcome
            self.backpropagate(child, reward) # Update all previous values based on the reward outcome
        return self.select_move(node)         # Select the best move from the current node


