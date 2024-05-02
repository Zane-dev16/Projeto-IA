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

    def __lt__(self, other):
        return self.id < other.id

    def rotate(self, row, col, clockwise):
        headings_list = {
            "F": ["FD", "FC", "FE", "FB"],
            "B": ["BD", "BC", "BE", "BB"],
            "V": ["VD", "VC", "VE", "VB"],
            "L": ["LH","LV"]
        }
        print(row, col, clockwise)

        pipes = self.board.pipes
        value = self.board.get_value(row, col)
        headings = headings_list[value[0]]
        inc = -1 if clockwise else 1
        pipes[row][col] = headings[(headings.index(value) + inc) % len(headings)]
        return PipeManiaState(Board(pipes))


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pipes) -> None:
        self.pipes = pipes
        self.nrows = len(self.pipes)
        self.ncols = len(self.pipes)

    def copy_board(self):
        """Copia da Representação interna de um tabuleiro de PipeMania."""

        new_board = Board()
        new_board.pipes = self.pipes
        new_board.nrows = self.nrows
        new_board.ncols = self.ncols

        return new_board

    def is_valid_indices(self, row: int, col: int) -> bool:
        """Devolve True se os indices existem no Board e
        False caso contrário"""

        return 0 <= row < self.nrows and 0 <= col < self.ncols

    def get_value(self, row: int, col: int) -> str:
        if not self.is_valid_indices(row, col):
            raise IndexError("Board row or column out of bounds")
        return self.pipes[row][col]

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

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(PipeManiaState(board))

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        action_list = list()
        nrows = self.initial.board.nrows
        ncols = self.initial.board.ncols
        for i in range(nrows):
            for j in range(ncols):
                action_list.append((i, j, True))
                action_list.append((i, j, False))
        return action_list

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        return state.rotate(*action)
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas corretamente e formam um caminho contínuo."""

        # Verificar se todas as posicoes do board estao corretamente preenchidas
        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                pipe = state.board.get_value(row, col)
                if pipe != ("FD" or "FC" or "FE" or "FB" or "BD" or "BC" or "BE" or "BB" or "VD" or "VC" or "VE" or "VB" or "LH" or "LV"):
                    return False  # Encontrou uma posicao vazia ou com input errado, nao e um estado objetivo

        # Verificar se todas as peças estao conectadas formando um caminho contínuo
        visited = [[False] * state.board.ncols for _ in range(state.board.nrows)]

        def dfs(row, col):
            if not state.board.is_valid_indices(row, col) or visited[row][col]:
                return
            visited[row][col] = True
            pipe = state.board.get_value(row, col)
            
            if pipe[1] in ['C', 'E', 'B', 'D']:
                next_row, next_col = row, col + 1
                dfs(next_row, next_col)
            if pipe[1] in ['C', 'B', 'F', 'H']:
                next_row, next_col = row + 1, col
                dfs(next_row, next_col)
            if pipe[1] in ['F', 'E', 'H', 'V']:
                next_row, next_col = row, col - 1
                dfs(next_row, next_col)
            if pipe[1] in ['D', 'E', 'V', 'L']:
                next_row, next_col = row - 1, col
                dfs(next_row, next_col)

        dfs(0, 0)  # comeca a procura na posicao inicial
        # Verifica se todas as posicoes foram visitadas
        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                if not visited[row][col]:
                    return False  # Encontrou uma posicao que nao foi visitada, nao e um estado objetivo

        return True


        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        #conta o numero de peças fora do lugar
 
        misplaced_pieces = 0
        nrows = node.state.board.nrows
        ncols = node.state.board.ncols
        for row in range(nrows):
            for col in range(ncols):
                current_pipe = node.state.board.get_value(row, col)
                goal_pipe = self.goal.get_value(row, col)
                if current_pipe != goal_pipe:
                    misplaced_pieces += 1
        return misplaced_pieces



if __name__ == "__main__":
    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Criar um estado com a configuração inicial:
    initial_state = PipeManiaState(board) # Mostrar valor na posição (2, 2):
    print(initial_state.board.get_value(2, 2))
    # Realizar ação de rodar 90° clockwise a peça (2, 2)
    result_state = problem.result(initial_state, (2, 2, True)) # Mostrar valor na posição (2, 2):
    print(result_state.board.get_value(2, 2))