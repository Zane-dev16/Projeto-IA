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

    # TODO: outros metodos da classe


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
        
        row = action[0]
        col = action[1]
        rotate = action[2]

        new_board = [row[:] for row in state.board.pipes]  # Cria uma cópia do tabuleiro
        #if rotate:
            # Rotaciona o tubo na posição (row, col)
            #falta fazer
        #else:
            # Inverte o tubo na posição (row, col)
            #falta fazer
            
        #return PipeManiaState(Board(new_board))
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        for row in range(state.board.nrows):
            for col in range(state.board.ncols):
                pipe = state.board.get_value(row, col)
                if pipe == "-":
                    return False  # Encontrou uma posicao vazia, então nao e um estado objetivo
        return True

        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # pecas que faltam ir ao lugar
        count = 0
        for row in range(node.state.board.nrows):
            for col in range(node.state.board.ncols):
                pipe = node.state.board.get_value(row, col)
                if pipe == "-":
                    count += 1
        return count


if __name__ == "__main__":
    pipemania = PipeMania(Board.parse_instance())
    print(pipemania.actions(pipemania.initial))