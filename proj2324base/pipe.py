# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 17:
# 107161 Irell Zane
# 106078 Joana Vaz

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:

    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.expansion_id = 0

    def __lt__(self, other):
        return self.id < other.id

    def rotate(self, row, col, new_piece):
        new_board = self.board.copy_board()
        new_board.pipes[row][col] = new_piece
        return PipeManiaState(new_board)
    
    def copy_state(self):
        new_board = self.board.copy_board()
        return PipeManiaState(new_board)

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pipes) -> None:
        self.pipes = pipes
        self.nrows = len(self.pipes)
        self.ncols = len(self.pipes)


    def is_valid_indices(self, row: int, col: int) -> bool:
        """Devolve True se os indices existem no Board e
        False caso contrário"""

        return 0 <= row < self.nrows and 0 <= col < self.ncols

    def get_value(self, row: int, col: int) -> str:
        if not self.is_valid_indices(row, col):
            raise IndexError("Board row or column out of bounds")
        return self.pipes[row][col]


    def adjacent_vertical_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if not self.is_valid_indices(row, col):
            raise IndexError("Board row or column out of bounds")

        if self.is_valid_indices(row - 1, col):
            pipe_above = self.get_value(row - 1, col)
        else:
            pipe_above = None

        if self.is_valid_indices(row + 1, col):
            pipe_below = self.get_value(row + 1, col)
        else:
            pipe_below = None

        return (pipe_above, pipe_below)

    def copy_board(self):
        """Copia da Representação interna de um tabuleiro de PipeMania."""
        return Board([[self.get_value(row, col) for col in range(self.ncols)] for row in range(self.nrows)])

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple[str, str]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if not self.is_valid_indices(row, col):
            raise IndexError("Board row or column out of bounds")

        if self.is_valid_indices(row, col - 1):
            pipe_left = self.get_value(row, col - 1)
        else:
            pipe_left = None

        if self.is_valid_indices(row, col + 1):
            pipe_right = self.get_value(row, col + 1)
        else:
            pipe_right = None

        return (pipe_left, pipe_right)

    @staticmethod 
    def read_pipes():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma matriz dos pipes."""
        pipes = list()
        while True:
            pipe_row = sys.stdin.readline().split()
            if not pipe_row:
                break
            pipes.append(pipe_row)
        return pipes

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt


        """
        pipes = Board.read_pipes()
        return Board(pipes)

    def print(self):
        """Imprime o tabuleiro de PipeMania."""
        board_output = []
        for row in range(self.nrows):
            board_output.append("\t".join([self.get_value(row, col) for col in range(self.ncols)]))
        return "\n".join(board_output)



    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board ,goal_board: Board = None):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))
        self.goal_board = goal_board

    
    def append_F_piece_actions(self, i, j, pipe, action_list):
        for new_pipe in ['FC', 'FB', 'FE', 'FD']:
            if new_pipe != pipe:
                action_list.append((i, j, new_pipe))
    
    def append_B_piece_actions(self, i, j,pipe, action_list):
        for new_pipe in ['BC', 'BB', 'BE', 'BD']:
            if new_pipe != pipe:
                action_list.append((i, j, new_pipe))

    def append_V_piece_actions(self, i, j,pipe, action_list):
        for new_pipe in ['VC', 'VB', 'VE', 'VD']:
            if new_pipe != pipe:
                action_list.append((i, j, new_pipe))

    def append_L_piece_actions(self, i,j, pipe, action_list):
        for new_pipe in ['LH', 'LV']:
            if new_pipe != pipe:
                action_list.append((i, j, new_pipe))

    def append_piece_actions(self, i, j, pipe, action_list):
        if pipe[0] == 'F':
            self.append_F_piece_actions(i, j, pipe, action_list)
        if pipe[0] == 'B':
            self.append_B_piece_actions(i, j, pipe, action_list)
        if pipe[0] == 'V':
            self.append_V_piece_actions(i, j, pipe, action_list)
        if pipe[0] == 'L':
            self.append_L_piece_actions(i, j, pipe, action_list)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        action_list = [None]

        nrows = self.initial.board.nrows
        ncols = self.initial.board.ncols
        i = state.expansion_id // ncols
        j = state.expansion_id % ncols
        if i == nrows:
            return []
        pipe = state.board.get_value(i, j)
        if(i,j) == (0,0):
            if pipe == 'VB':
                return action_list
        if (i, j) == (0, ncols - 1):
            if pipe == 'VE':
                return action_list
        if (i, j) == (nrows - 1, 0):
            if pipe == 'VD':
                return action_list
        if (i, j) == (nrows - 1, ncols - 1):
            if pipe == 'VC':
                return action_list
        if i == 0:
            if pipe == "BB" or pipe == "LH":
                return action_list
        # Casos para linha de baixo
        if i == nrows - 1:
            if pipe == "BC" or pipe == "LH":
                return action_list
        # Casos para a linha da direita
        if j == ncols - 1:
            if pipe == "BE" or pipe == "LV":
                return action_list
        # Casos para a linha da esquerda
        if j == 0:
            if pipe == "BD" or pipe == "LV":
                return action_list 
        self.append_piece_actions(i, j, pipe, action_list)
        return action_list

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if action == None:
            new_state = state.copy_state()
        else:
            new_state = state.rotate(*action)
        new_state.expansion_id = state.expansion_id + 1
        return new_state

        
    def h(self, node: Node):
        """Função heurística utilizada para a procura A*."""
        state = node.state
        misplaced_pieces = 0
        nrows = state.board.nrows
        ncols = state.board.ncols

        for row in range(nrows):
            for col in range(ncols):
                current_pipe = state.board.get_value(row, col)
                if self.goal_board:
                    goal_pipe = self.goal_board.get_value(row, col)
                    if current_pipe != goal_pipe:
                        misplaced_pieces += 1

        # Weight for connected pipes
        connected_pieces = 0
        for row in range(nrows):
            for col in range(ncols):
                pipe = state.board.get_value(row, col)
                above, below = state.board.adjacent_vertical_values(row, col)
                left, right = state.board.adjacent_horizontal_values(row, col)
                if above and above[1] in ['B', 'C'] and pipe[1] in ['F', 'H']:
                    connected_pieces += 1
                if below and below[1] in ['F', 'H'] and pipe[1] in ['B', 'C']:
                    connected_pieces += 1
                if left and left[1] in ['D', 'E'] and pipe[1] in ['C', 'H']:
                    connected_pieces += 1
                if right and right[1] in ['C', 'H'] and pipe[1] in ['D', 'E']:
                    connected_pieces += 1

        return misplaced_pieces + connected_pieces * 2



    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas corretamente e formam um caminho contínuo."""

        pipe_list = ["FD", "FC", "FE", "FB", "BD", "BC", "BE", "BB", "VD", "VC", "VE", "VB", "LH", "LV"]

        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                pipe = state.board.get_value(row, col)
                if pipe not in pipe_list:
                    return False 

        visited = [[False] * state.board.ncols for _ in range(state.board.nrows)]

        def dfs(row, col, direction):
            stack = [(row, col, direction)]  # (row, col, direcao de onde viemos)
            while stack:
                r, c, source = stack.pop()
                if not state.board.is_valid_indices(r, c):
                    continue
                if visited[r][c]:
                    continue

                visited[r][c] = True
                pipe = state.board.get_value(r, c)

                connections = {
                    "left": ["FE", "BC", "BB", "BE", "VC", "VE", "LH"],
                    "right": ["FD", "BC", "BB", "BD", "VB", "VD", "LH"],
                    "up": ["FC", "BC", "BE", "BD", "VC", "VD", "LV"],
                    "down": ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
                }

                if pipe in connections["right"] and source != "left":
                    stack.append((r, c + 1, "right"))
                if pipe in connections["down"] and source != "up":
                    stack.append((r + 1, c, "down"))
                if pipe in connections["left"] and source != "right":
                    stack.append((r, c - 1, "left"))
                if pipe in connections["up"] and source != "down":
                    stack.append((r - 1, c, "up"))

        dfs(0, 0, None)

        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                if not visited[row][col]:
                    return False
        return True






if __name__ == "__main__":

    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = astar_search(problem)
    if goal_node:
        print(goal_node.state.board.print())
    pass
