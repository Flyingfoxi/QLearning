import random, os

class Game:
    def __init__(self):
        self.playerX = None
        self.playerO = None
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " "

    def check_winner(self, player):
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]) or all([self.board[j][i] == player for j in range(3)]):
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player or self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    def print_board(self):
        print("  0   1   2")
        for i, row in enumerate(self.board):
            print(i, " | ".join(row))
            if i < 2:
                print("  ---+---+---")

    def human_move(self, player):
        while True:
            move = input("Dein Zug (gib Zeile und Spalte als \"Zeile, Spalte\" an): ")
            row, col = [int(i.strip()) for i in move.split(",")]
            if self.is_valid_move(row, col):
                break
            print("Ungültiger Zug, versuch es nochmal.")
        self.board[row][col] = player

    def computer_move(self, agent, player):
        state = agent.get_state(self.board)
        action = agent.choose_action()
        return action

    def playerX_move(self):
        state = self.pagent.get_state(self.board)
        if self.playerX is None:
            action = self.human_move("X")
        else:
            action = self.computer_move(self.playerX, "X")

        row, col = divmod(action, 3)
        self.board[row][col] = "X"
        return state, action


    def playerO_move(self):
        if self.playerO is None:
            self.human_move("O")
        else:
            self.computer_move(self.playerO, "O")


        row, col = divmod(action, 3)
        self.board[row][col] = player


    def set_playerX(self, agent=None):
        self.playerX = agent

    def set_playerO(self, agent=None):
        self.playerO = agent

    def play_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        print("Spiel beginnt")
        self.print_board()

        while True:
            self.human_move("X")
            if self.check_winner("X"):
                print("Herzlichen Glückwunsch! Du hast gewonnen!")
                break
            if all(self.board[i][j] != " " for i in range(3) for j in range(3)):
                print("Es ist ein Unentschieden!")
                break

            print("Computerzug:")
            self.playerO_move()

            self.print_board()

            if self.check_winner("O"):
                print("Der Computer hat gewonnen. Versuch es nochmal!")
                break

            if all(self.board[i][j] != " " for i in range(3) for j in range(3)):
                print("Es ist ein Unentschieden!")
                break

    def train(self, episodes=10_000):
        history = []
        for _ in range(episodes):
            self.board = [[" " for _ in range(3)] for _ in range(3)]

            result = None
            while result is None:
                state, action = self.playerX_move()
                # Zustand und Aktion des Agenten vor dem Zug sichern.
                state = self.get_state(board)
                action = self.choose_action(board)
                row, col = divmod(action, 3)
                board[row][col] = "O"

                if self.game.check_winner("O"):
                    self.update_q_table(
                    state, action, self.reward_win, terminal=True
                    )
                    result = "win"
                elif self.game.is_board_full():
                    self.update_q_table(
                    state, action, self.reward_draw, terminal=True
                    )
                    result = "draw"
                else:
                    # Die Umgebung führt genau eine Zufallsantwort aus.
                    x_action = self.rng.choice(self.get_valid_actions(board))
                    row, col = divmod(x_action, 3)
                    board[row][col] = "X"
                    if self.game.check_winner("X"):
                        self.update_q_table(
                        state, action, self.reward_loss, terminal=True
                        )
                        result = "loss"
                    elif self.game.is_board_full():
                        self.update_q_table(
                        state, action, self.reward_draw, terminal=True
                        )
                        result = "draw"
                    else:
                        # s' ist das Brett nach Xs realer Antwort.
                        next_state = self.get_state(board)
                        self.update_q_table(
                        state,
                        action,
                        reward=0,
                        next_state=next_state,
                        terminal=False,
                        )
            history.append(result)
            self.epsilon = max(
                self.epsilon_min,
                self.epsilon * self.epsilon_decay,
            )
            return history
