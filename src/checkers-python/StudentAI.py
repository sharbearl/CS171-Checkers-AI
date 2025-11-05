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

        # root = Node(board_state)
        # for move in moves:
        #     Node(move)




        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move

    def simulate_one_game(self, cur: Node):
        while not cur.is_win():
            moves = self.board.get_all_possible_moves(self.color)
            move = random.choice(moves)
            cur = cur.add_child(move)

        return cur


    
    def simulate_games(self, root, moves):
        moves = self.board.get_all_possible_moves(self.color)
        root.add_children(moves) # Expand node

        for child in root.get_children():
            leaf = self.simulate_one_game(child) ## This adds one child node per node, 
                                          ## Might need to figure a way to not readd the child during expansion
            update_path(leaf)

        best_child = root.best_child ## repeat continuously
                                     ## if all children are expanded already, then choose its best child
        simulate_game(best_child)



class Node:
    def __init__(self, state: Any, parent: Node, move: Move) -> None:
        self.move_made = move ## instead of state maybe save the move that gets you here?
        self.parent = parent
        self.children = []
        self.total_games = 0
        self.wins = 0
        self.untried = []

    def get_state(self) -> Board:
        """ Returns state of the board at current node """
        return self.state
    
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
    
    def add_child(self, move: Move):
        new_node = Node(self, move)
        self.children.append(new_node)
        return new_node

    # def add_children(self, moves: List[Move]):
    #     for move in moves:
    #         self.add_child(move)

    def update_node(self, win):
        """ win = 0 if loss
            win = 1 if win/tie
        """
        if not self.parent:
            return
        self.total_games += 1
        self.wins += win
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


