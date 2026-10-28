"""Schüler-Gerüst: Die Kernlogik von Q-Learning selbst ergänzen.

Der Agent spielt immer O. Der zufällige Gegner X beginnt jede Trainingspartie.
get_state, get_valid_actions, get_next_states und get_q_values sind als
Hilfsmethoden bereits vorbereitet. choose_action und update_q_table sind die
Programmieraufträge; train_agent wird aus drei Codeblöcken des Arbeitshefts
übertragen.
"""

from copy import deepcopy
import random


class QLearningAgent:
    def __init__(self, game, alpha=0.2, gamma=0.9, epsilon=0.3,
                 epsilon_decay=0.9995, epsilon_min=0.02):
        """Startwerte für Umgebung, Hyperparameter und Q-Tabelle."""
        self.game = game
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        self.reward_win = 1
        self.reward_loss = -1
        self.reward_draw = 0

        # Schlüssel: Tupelzustand. Wert: neun Aktionswerte für die Felder 0–8.
        self.q_table = {}
        self.rng = random.Random()

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

    def get_next_states(self, board, player="O"):
        """Erzeuge Kopien nach jedem legalen Zug; verändert das Original nicht.

        Für mögliche Agentenzüge wird player="O" verwendet. Mögliche X-Antworten
        untersucht man auf einem hypothetischen Brett nach einem O-Zug mit
        player="X". Im Training wird nur eine zufällige Antwort wirklich gespielt.
        """
        next_states = []
        for action in self.get_valid_actions(board):
            next_board = deepcopy(board)
            row, col = divmod(action, 3)
            next_board[row][col] = player
            next_states.append(next_board)
        return next_states

    def get_q_values(self, state):
        """Liefere neun Q-Werte; ein neuer Zustand startet mit lauter Nullen."""
        if state not in self.q_table:
            self.q_table[state] = [0.0] * 9
        return self.q_table[state]

    def choose_action(self, board=None):
        """TODO A: Eine legale Aktion mit epsilon-greedy auswählen."""
        if board is None:
            board = self.game.board

        valid_actions = self.get_valid_actions(board)
        if not valid_actions:
            raise ValueError("Für ein volles Brett gibt es keine legale Aktion.")

        state = self.get_state(board)
        q_values = self.get_q_values(state)

        if self.rng.random() < self.epsilon:
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
        # raise NotImplementedError("TODO B: update_q_table vervollständigen")

    def train_agent(self, episodes=20_000_000, seed=None):
        # Trainiere gegen zufälliges X und gib ein Ergebnis pro Episode zurück.
        if seed is not None:
            self.rng.seed(seed)
        history = []
        for _ in range(episodes):
            self.game.board = [[" " for _ in range(3)] for _ in range(3)]
            board = self.game.board
            result = None
            # X beginnt jede Partie mit einem zufälligen legalen Zug.
            x_action = self.rng.choice(self.get_valid_actions(board))
            row, col = divmod(x_action, 3)
            board[row][col] = "X"
            while result is None:
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
