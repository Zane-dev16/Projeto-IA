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

FD, FC, FE, FB, BD, BC, BE, BB, VD, VC, VE, VB, LH, LV = range(14)
pipe_groups = [[FD, FC, FE, FB], [BD, BC, BE, BB], [VD, VC, VE, VB], [LH, LV]]
pipe_strings = ["FD", "FC", "FE", "FB", "BD", "BC", "BE", "BB", "VD", "VC", "VE", "VB", "LH", "LV"]

lig_esq = {FE, BC, BB, BE, VC, VE, LH}
lig_dir = {FD, BC, BB, BD, VB, VD, LH}
lig_cima = {FC, BC, BE, BD, VC, VD, LV}
lig_baixo = {FB, BB, BE, BD, VB, VE, LV}
# Map the pipe characters to integers
pipe_map = {
    "FD": FD, "FC": FC, "FE": FE, "FB": FB,
    "BD": BD, "BC": BC, "BE": BE, "BB": BB,
    "VD": VD, "VC": VC, "VE": VE, "VB": VB,
    "LH": LH, "LV": LV
}


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
        new_board.set_value(row, col, new_piece)
        return PipeManiaState(new_board)
    
    def copy_state(self):
        return PipeManiaState(self.board.copy_board())

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pipes, nrows, ncols) -> None:
        self.pipes = pipes
        self.nrows = nrows
        self.ncols = ncols


    def is_valid_indices(self, row: int, col: int) -> bool:
        """Devolve True se os indices existem no Board e
        False caso contrário"""

        return 0 <= row < self.nrows and 0 <= col < self.ncols

    def get_value(self, row: int, col: int) -> str:
        index = row * self.ncols + col
        return self.pipes[index]
    
    def set_value(self, row, col, new_value):
        self.pipes[row * self.ncols + col] = new_value

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
        return Board(self.pipes.copy(), self.nrows, self.ncols)

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
        """Reads pipes from standard input (stdin) and returns nrows, ncols, and pipes."""
        nrows = 0
        ncols = None
        pipes = []
        while True:
            pipe_row = sys.stdin.readline().split()
            if not pipe_row:
                break
            if ncols is None:
                ncols = len(pipe_row)
            else:
                if len(pipe_row) != ncols:
                    raise ValueError("Inconsistent number of columns in the input")
            pipes.extend([pipe_map[pipe] for pipe in pipe_row])
            nrows += 1
        return pipes, nrows, ncols

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt
        """
        return Board(*Board.read_pipes())

    def print(self):
        """Prints the PipeMania board."""
        board_output = []
        for row in range(self.nrows):
            row_output = ""
            for col in range(self.ncols):
                row_output += pipe_strings[self.get_value(row, col)] + "\t"
            board_output.append(row_output.rstrip())
        return "\n".join(board_output)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board ,goal: Board = None):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board), goal)

    
    def h(self, node: Node):
        """Função heurística utilizada para a procura A*."""
        return node.state.expansion_id

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

        
    # Define pipe constants

    # Replace string comparisons with integer comparisons


    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas corretamente e formam um caminho contínuo."""

        # Verificar se todas as posicoes do board estao corretamente preenchidas
        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                pipe = state.board.get_value(row, col)
                if pipe not in pipe_map:
                    return False  # Encontrou uma posicao vazia ou com input errado, nao e um estado objetivo

        # Convert board values to integers using the pipe_map
        board = [[pipe_map[state.board.get_value(row, col)] for col in range(state.board.ncols)] for row in range(state.board.nrows)]

        # Verificar se todas as peças estao conectadas formando um caminho contínuo
        visited = [[False] * state.board.ncols for _ in range(state.board.nrows)]

        # Define starting point, assuming (0, 0) is the start
        start_row, start_col = 0, 0  # Change this if your starting point is different

        # Helper function to check if two pipes are connected
        def is_connected(pipe, next_pipe, direction):
            if direction == "right":
                return pipe in lig_dir and next_pipe in lig_esq
            elif direction == "down":
                return pipe in lig_baixo and next_pipe in lig_cima
            elif direction == "left":
                return pipe in lig_esq and next_pipe in lig_dir
            elif direction == "up":
                return pipe in lig_cima and next_pipe in lig_baixo
            return False

        # Depth-First Search (DFS) to check connectivity
        def dfs(row, col):
            stack = [(row, col)]
            while stack:
                r, c = stack.pop()
                if not state.board.is_valid_indices(r, c) or visited[r][c]:
                    continue
                visited[r][c] = True
                pipe = board[r][c]

                # Check all 4 directions
                if state.board.is_valid_indices(r, c + 1) and not visited[r][c + 1] and is_connected(pipe, board[r][c + 1], "right"):
                    stack.append((r, c + 1))
                if state.board.is_valid_indices(r + 1, c) and not visited[r + 1][c] and is_connected(pipe, board[r + 1][c], "down"):
                    stack.append((r + 1, c))
                if state.board.is_valid_indices(r, c - 1) and not visited[r][c - 1] and is_connected(pipe, board[r][c - 1], "left"):
                    stack.append((r, c - 1))
                if state.board.is_valid_indices(r - 1, c) and not visited[r - 1][c] and is_connected(pipe, board[r - 1][c], "up"):
                    stack.append((r - 1, c))

        # Start DFS from the initial position
        dfs(start_row, start_col)

        # Check if all cells were visited
        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                if not visited[row][col]:
                    return False

        return True


if __name__ == "__main__":

    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    print(board.print())