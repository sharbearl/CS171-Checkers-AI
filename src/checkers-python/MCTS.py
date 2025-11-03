import Math
from BoardClasses import Board
from Checker import Checker
from Move import Move

class Node:
    def __init__(self, state: Any, parent: Node, moves: List[Move]) -> None:
        self.state = state
        self.parent = parent
        self.children = []
        self.total_games = 0
        self.wins = 0
        self.possible_moves = moves
        self.untried = moves

    def get_state(self) -> Board:
        """ Returns state of the board at current node """
        return self.state
    
    def get_parent(self) -> Node:
        """ Returns parent node of current node """
        return self.parent
    
    def get_children(self) -> List[Node]:
        """ Returns a lsit of nodes representing the children of the current node """
        return self.children
    
    def get_total_games(self) -> int:
        """ Returns the number of total times the node has been visited/played """
        return self.total_games
    
    def get_wins(self) -> int:
        """ Return the total times the node has resulted in a winning game """
        return self.wins
    
    def get_possible_moves(self) -> List[Move]:
        """ Returns a list of possible moves the node can take """
        return self.total_games
    
    def get_untried(self) -> List[Move]:
        """ Returns a list of moves not yet tried """
        return self.wins
    
    def get_ucb(self, c: int | float) -> Node:
        """ Returns the UCB value of the node 
            UCB = wi/si + c * sqrt
        """
        best_child = None
        score = 0
        for child in self.children:
            ucb = (self.wins / self.total_games) + c * Math.sqrt(Math.ln(self.parent.total_games) / self.total_games)
            if ucb > score:
                best_child = child
                score = ucb
        return best_child
    
    def add_child(self, new_child: Node) -> None:
        self.children.append(new_child)

    def is_win(self):
        pass
    

class MCSTree:
    def __init__(self):
        self.head = None