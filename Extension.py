import random

class GameError(Exception):
    def __init__(self, loc, reason):
        super().__init__(f"QLearning Game failed at: {loc}, reason: {reason}")

class Game:
    board: list[list[str]]


    def __init__(self, playerX, playerO):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players: "list[Player]" = [playerX, playerO]
        self.move = 0

    def perform_move(self) -> bool:
        if self.move % 2 == 0:
            player = "X"
        else:
            player = "O"

        # only pass imutable reference to the players
        move = self.players[self.move % 2].play_move(self.get_board())

        if not self.is_valid_move(*move):
            raise GameError(f"move{self.move}", f"invalid move from player {player}")

        if self.check_winner(player):
            print(f"GAME ENDED: Winner {player}")
            return False

        if self.is_board_full():
            print("GAME ENDED: Draw")
            return False

        return True

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " "

    def get_board(self):
        return tuple(tuple(row) for row in self.board)

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def check_winner(self, player):
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]) or all([self.board[j][i] == player for j in range(3)]):
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player or self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def print_board(self):
        print("  0   1   2")
        for i, row in enumerate(self.board):
            print(i, " | ".join(row))
            if i < 2:
                print("  ---+---+---")

    def get_board(self) -> list[list[str]]:
        return self.board

class Player:

    def play_move(self, game: Game) -> tuple[int, int]:
        ...


class QAgent:
    def __init__(self, learning: bool = True, testing: bool = True, alpha=0.2, gamma=0.9, epsilon=0.3,
                 epsilon_decay=0.999, epsilon_min=0.01,):
        """Startwerte für Umgebung, Hyperparameter und Q-Tabelle."""

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.reward_win = 1
        self.reward_loss = -10
        self.reward_draw = -0.1

        self.learning = learning
        self.testing = testing

        # Schlüssel: Tupelzustand. Wert: neun Aktionswerte für die Felder 0–8.
        self.q_table = {}
        self.rng = random.Random()

    def play_move(self, game: Game) -> tuple[int, int]:

        move = self.choose_action(game.get_board())


        if self.learning:
            self.update_q_table


    def get_q_values(self,  state):
        if state not in self.q_table:
            self.q_table[state] = [0.0] * 9
        return self.q_table[state]

    def get_state(self, board):
        """Wandle eine veränderbare Liste von Listen in einen Tupelschlüssel um."""
        return tuple(tuple(row) for row in board)

    def get_valid_actions(self, board):
        """Liefere nur freie Felder als Aktionen 0 bis 8."""
        return [
            row * 3 + col
            for row in range(3)
            for col in range(3)
            if board[row][col] == " "
        ]

    def choose_action(self, board):

        valid_actions = self.get_valid_actions(board)
        if not valid_actions:
            raise ValueError("Für ein volles Brett gibt es keine legale Aktion.")

        state = self.get_state(board)
        q_values = self.get_q_values(state)

        if (self.rng.random() < self.epsilon and self.testing):
            # exploration
            return random.choice(valid_actions)

        else:
            # exploitation
            max_q = max([q_values[i] for i in valid_actions])
            best_moves = [i for i in valid_actions if q_values[i] == max_q]
            return random.choice(best_moves)


    def update_q_table(self, state, action, reward, next_state=None, terminal=False):
        """TODO B: Genau Q(state, action) gemäss Q-Learning aktualisieren."""
        q_values = self.get_q_values(state)
        old_value = q_values[action]

        if terminal:
            target = reward
        else:
            if next_state is None:
                raise ValueError("Für ein nicht-terminales Update ist next_state nötig.")
            next_actions = self.get_valid_actions(next_state)
            if not next_actions:
                raise ValueError("Ein terminaler Folgezustand braucht terminal=True.")

            next_q_values = self.get_q_values(next_state)
            target = reward + self.gamma * max(next_q_values)

        self.q_table[state][action] = old_value + self.alpha * (target - old_value)
