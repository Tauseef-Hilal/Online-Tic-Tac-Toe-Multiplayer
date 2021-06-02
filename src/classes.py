"""
    Network class
"""

import socket
import pickle


class Network:
    """Handle sockets"""

    def __init__(self, server=False) -> None:
        self.is_server = server
        self._ADDR = ("localhost", 5050)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not self.is_server:
            self._server.connect(self._ADDR)

    def send(self, obj, conn=None) -> None:
        if not self.is_server:
            self._server.sendall(pickle.dumps(obj))
        else:
            conn.sendall(pickle.dumps(obj))

    def receive(self, conn=None) -> object:
        if not self.is_server:
            return pickle.loads(self._server.recv(4096))
        return pickle.loads(conn.recv(4096))

    def __repr__(self) -> str:
        if self.is_server:
            return f"<Network => Server>"
        return f"<Network => Client>"


class Player:
    """Handle a player"""

    __slots__ = ["id",
                 "mark",
                 "score"]

    def __init__(self, id, mark) -> None:
        self.id = id
        self.mark = mark
        self.score = 0          # Not implemented yet!

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Player({self.id}, {self.mark})"


class Game:
    """Game class"""

    __slots__ = ["id",
                 "board",
                 "players",
                 "matching",
                 "whose_turn",
                 "moves"]

    def __init__(self, id, board) -> None:
        self.id = id
        self.board = board
        self.players = []
        self.matching = []
        self.whose_turn = None
        self.moves = 0

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
                print(f"[STATUS] {repr(player)} removed!")
                return True
        return False
    
    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __repr__(self) -> str:
        return f"Game({self.id}, {self.board})"
