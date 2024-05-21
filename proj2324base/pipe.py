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
pipe_groups = ({FD, FC, FE, FB}, {BD, BC, BE, BB}, {VD, VC, VE, VB}, {LH, LV})
F_group, B_group, V_group, L_group = range(4)
pipe_strings = ("FD", "FC", "FE", "FB", "BD", "BC", "BE", "BB", "VD", "VC", "VE", "VB", "LH", "LV")

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
        if not self.is_valid_indices(row, col):
            return None
        index = row * self.ncols + col
        return self.pipes[index]
    
    def set_value(self, row, col, new_value):
        self.pipes[row * self.ncols + col] = new_value

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
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

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
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

    def append_piece_actions(self, i, j, pipe, action_list):
        for new_pipe in pipe_groups[pipe//4] - {pipe}:
            action_list.append((i, j, new_pipe))

    def top_connect_no_left_actions(self, i, j, pipe_group):
        if pipe_group == F_group:
            return [(i, j, FC)]
        if pipe_group == B_group:
            return [(i, j, BD)]
        if pipe_group == V_group:
            return [(i, j, VD)]
        if pipe_group == L_group:
            return [(i, j, LV)]
        
    def top_left_connect_actions(self, i, j, pipe_group):
        if pipe_group == F_group:
            return []
        if pipe_group == B_group:
            return [(i, j, BC), (i, j, BE)]
        if pipe_group == V_group:
            return [(i, j, VC)]
        if pipe_group == L_group:
            return []
    
    def top_left_no_connect_actions(self, i, j, pipe_group):
        if pipe_group == F_group:
            return [(i, j, new_pipe) for new_pipe in (FB, FD)]
        if pipe_group == B_group:
            return []
        if pipe_group == V_group:
            return [(i, j, VB)]
        if pipe_group == L_group:
            return []
        
    def left_connect_no_top_actions(self, i, j, pipe_group):
        if pipe_group == F_group:
            return [(i, j, FE)]
        if pipe_group == B_group:
            return [(i, j, BB)]
        if pipe_group == V_group:
            return [(i, j, VE)]
        if pipe_group == L_group:
            return [(i, j, LH)]
        

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        action_list = [None]

        board = state.board
        nrows = board.nrows
        ncols = board.ncols
        i = state.expansion_id // ncols
        j = state.expansion_id % ncols
        if i == nrows:
            return []
        pipe = state.board.get_value(i, j)

        top_pipe = board.get_value(i-1, j)
        left_pipe = board.get_value(i, j-1)

        if top_pipe in lig_baixo:     
            if left_pipe in lig_dir:
                return self.top_left_connect_actions(i, j, pipe // 4)
            else:
                return self.top_connect_no_left_actions(i, j, pipe // 4)
        else:
            if left_pipe in lig_dir:
                return self.left_connect_no_top_actions(i, j, pipe // 4)
            else:
                return self.top_left_no_connect_actions(i, j, pipe // 4)

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
        board = state.board

        # Verificar se todas as peças estao conectadas formando um caminho contínuo
        visited = [[False] * state.board.ncols for _ in range(state.board.nrows)]

        def is_connected_horiz(pipe, next_pipe):
            return pipe in lig_dir and next_pipe in lig_esq
        
        def is_connected_vert(pipe, next_pipe):
            return pipe in lig_baixo and next_pipe in lig_cima
        # Depth-First Search (DFS) to check connectivity
        def dfs():
            stack = [(0, 0)]
            while stack:
                r, c = stack.pop()
                if visited[r][c]:
                    continue
                visited[r][c] = True
                pipe = board.get_value(r, c)

                if pipe in lig_dir:
                    if is_connected_horiz(pipe, board.get_value(r, c + 1)):

                        stack.append((r, c + 1))
                    else:
                        return False
                if pipe in lig_esq:
                    if is_connected_horiz(board.get_value(r, c - 1), pipe):
                        stack.append((r, c - 1))
                    else:
                        return False
                if pipe in lig_baixo:
                    if is_connected_vert(pipe, board.get_value(r + 1, c)):
                        stack.append((r + 1, c))
                    else:
                        return False
                if pipe in lig_cima:
                    if is_connected_vert(board.get_value(r - 1, c), pipe):
                        stack.append((r - 1, c ))
                    else:
                        return False
        # Start DFS from the initial position
        if dfs():
            return False

        # Check if all cells were visited
        for row in visited:
            if not all(row):
                return False

        return True


if __name__ == "__main__":

    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)
    if goal_node:
        print(goal_node.state.board.print())
    else:
        pass