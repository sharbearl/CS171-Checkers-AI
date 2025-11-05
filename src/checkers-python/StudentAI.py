import Math
import random
from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
EXPLORATION_PARAM = 1 ## Adjust c constant for better results
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
        # moves = self.board.get_all_possible_moves(self.color)

        root = Node(None, None) # If move is none, this is the top of the tree, 
                                ## May need to have something to check this

        self.simulate_games(root) # Simulate games -- currently
        move = root.best_child(EXPLORATION_PARAM).get_move()

        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
    

    def simulate_games(self, root: Node, limit: int) -> None:
        """ Simulates games for the given root node 
            @params: Node representing the root
                     integer representing the number of times to run simulations
        """
        moves = self.board.get_all_possible_moves(self.color)
        root.add_children(moves) # Expand node

        for child in root.get_children(): # Simulate one game for each child
            leaf, result = self.simulate_one_game(child) ## This adds one child node per node, 
                                                         ## might need to figure a way to not readd the child during expansion
            leaf.update_node(result, self.board)

        for _ in range(limit):
            best_child = root.best_child(EXPLORATION_PARAM) ## Choose the best node to expand
                                     ## repeat continuously
                                     ## if all children are expanded already, then choose its best child
            while best_child.is_unexplored(): ## This runs through the tree until you get to a bottom-most
                                              ## unexplored child, currently unwritten
                self.board.make_move(best_child.get_move()) # Perform move
                best_child = root.best_child(EXPLORATION_PARAM)

            leaf, result = self.simulate_one_game(child) 
            leaf.update_node(result, self.board)
        # self.simulate_games(best_child) ## Need to make sure to undo all the nodes

    def simulate_one_game(self, cur: Node):
        """ Simulates a single game by playing random moves until an outcome is reached 
            @return: tuple containing the terminal node and the utility value representing win/loss
        """
        while self.board.is_win() != -1: # While current node is non terminal
            moves = self.board.get_all_possible_moves(self.color)
            move = random.choice(moves) # Choose random move to make
            
            self.board.make_move(move,self.color) # Perform move
            cur = cur.add_child(move) # Add child

        return (cur, self.board.is_win())



class Node:
    def __init__(self, state: Any, parent: Node, move: Move) -> None:
        self.move_made = move ## instead of state maybe save the move that gets you here?
        self.parent = parent
        self.children = []
        self.total_games = 0
        self.wins = 0
        self.untried = []

    def __eq__(self, right: Node) -> bool:
        """ Equal operator returns true if parent and move_made are the same """
        return self.move_made == right.move_made and self.parent == right.parent

    ## The following getters may not all be necessary, remove if unneeded
    def get_move(self) -> Board:
        """ Returns state of the board at current node """
        return self.move_made
    
    def get_parent(self) -> Node:
        """ Returns parent node of current node """
        return self.parent
    
    def get_children(self) -> List[Node]:
        """ Returns a list of nodes representing the children of the current node """
        return self.children
    
    def get_total_games(self) -> int:
        """ Returns the number of total times the node has been visited/played """
        return self.total_games
    
    def get_wins(self) -> int:
        """ Return the total times the node has resulted in a winning game """
        return self.wins
    
    # def get_possible_moves(self) -> List[Move]:
    #     """ Returns a list of possible moves the node can take """
    #     return self.total_games
    
    def get_untried(self) -> List[Move]:
        """ Returns a list of moves not yet tried """
        return self.untried

    def is_fully_expanded(self)-> bool:
        return len(self.untried) == 0

    def get_best_child(self, c = EXPLORATION_PARAM) -> Node:
        """ Returns the child with the best UCT value of the current node 
            UCT = wi/si + c * sqrt
        """
        best_child = None
        score = 0
        for child in self.children:
            uct = (self.wins / self.total_games) + c * Math.sqrt(Math.ln(self.parent.total_games) / self.total_games)
            if uct > score:
                best_child = child
                score = uct
            
        if not best_child:
            random.choice(self.children)
        return best_child
    
    def add_child(self, move: Move) -> Node:
        """ Creates a child node with the given move 
            @return: newly created node
        """
        new_node = Node(self, move)
        self.children.append(new_node)
        return new_node

    def add_children(self, moves: List[Move]) -> None:
        """ Creates children node for each move """
        for move in moves:
            self.add_child(move)

    def is_win(self) -> int: ## Maybe this doesn't need to be a function, might just call in the simulate_one_game function
        """ Returns when a is made
            @return: -1 if non terminal node
                     0 if loss
                     1 if won
        """
        pass

    def update_node(self, win: int, board: Board):
        """ Backtracks through tree and updates values while undoing move made on Board
            win = 0 if loss; win = 1 if win/tie
        """
        if not self.parent:
            return
        self.total_games += 1
        self.wins += win
        board.undo()
        # self.parent.update_node(win) # parent nodes will update when backpropagating
    

class MCTS:
    def __init__(self, color, num_simulations):
        self.color = color
        self.num_simulations = num_simulations
    
    def select(self, node: Node):
        """ Select node to expand based on UCT """
        while node.get_children() and node.is_fully_expanded(): # The node has children and every child has been added to compute UCT
            node = node.get_best_child()
        return node

    def expand(self, node: Node, color, board: Board):
        """ Expand children of selected node """
        untried_moves = node.get_untried()
        if not untried_moves:   # Check if there are possible moves; if empty, populate the list
            untried_moves = [move for moves in board.get_all_possible_moves(color) for move in moves]
        if not node.untried_moves:  # If stil empty after populate, reached terminal node
            return node
        move = untried_moves.pop(random.randint(len(untried_moves))) # Pick a random child to expand
        board.make_move(move, color)
        child = node.add_child(move)
        return child
    
    def simulate(self, color, board: Board):
        """ Simulate games from child node """
    
    def backpropagate(self, node: Node, win: int, board: Board):
        """ Backpropagate and update statistics.
            win = 0 if loss
            win = 1 if win/tie """

    def search(self, root_board: Board) -> Move:
        """ Do search for best move to return """


