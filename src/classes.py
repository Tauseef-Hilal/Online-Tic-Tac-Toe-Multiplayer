"""
    Network class
"""

import socket
import pickle


class Network():
    """Handle sockets"""

    def __init__(self, server=False):
        self.is_server = server
        self._ADDR = ("localhost", 5050)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not self.is_server:
            self._server.connect(self._ADDR)

    def send(self, obj, conn=None):
        if not self.is_server:
            self._server.sendall(pickle.dumps(obj))
        else:
            conn.sendall(pickle.dumps(obj))

    def receive(self, conn=None):
        if not self.is_server:
            return pickle.loads(self._server.recv(4096))
        return pickle.loads(conn.recv(4096))

    def __repr__(self):
        if self.is_server:
            return f"<Network => Server>"
        return f"<Network => Client>"


class Player():
    """Handle a player"""

    def __init__(self, id, mark):
        self.id = id
        self.mark = mark

    def __repr__(self):
        return f"Player({self.id}, {self.mark})"


class Game:
    """Game class"""

    def __init__(self, id, board) -> None:
        self.id = id
        self.board = board
        self.players = []
        self.matching = []

    def get_player(self) -> Player:
        """Grab a player"""
        if len(self.matching) == 0:
            self.matching.append(self.players[-1])
            return self.players[-1]
        else:
            print(self.players)
            for player in self.players:
                if player not in self.matching:
                    self.matching.append(player)
                    return player

    def rem_player(self, mark) -> bool:
        """Remove a player"""

        for player in self.players:
            if player.mark == mark:
                self.players.remove(player)
                self.matching.remove(player)
                print(f"[STATUS] {player} removed!")
                return True
        return False

    def __repr__(self) -> str:
        string = f"""
        ------------------
        Game: {self.id}
        Players:
        {self.players}
        ------------------
        """
        return string
