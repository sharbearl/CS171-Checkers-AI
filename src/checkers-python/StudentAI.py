import Math
import random
from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
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
    
    def get_best_child(self, c: int | float) -> Node:
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

    def add_children(self, moves: List[Move]):
        for move in moves:
            self.add_child(move)

    def is_win(self):
        pass

    def update_node(self, win):
        """ win = 0 if loss
            win = 1 if win/tie
        """
        if not self.parent:
            return
        self.total_games += 1
        self.wins += win
        self.parent.update_node(win)
    

class MCSTree:
    def __init__(self):
        self.head = None