"""
    server.py

    Server for the project
"""

import threading
from src.classes import (Network,
                         Player,
                         Game)

# Create server


class Server(Network):

    def __init__(self):
        super().__init__(server=True)
        self._games = []
        self._num_clients = 0
        self._server.bind(self._ADDR)
        print("[STATUS] Server Started!")
        self._start_listen()

    def _start_listen(self):
        print("[SERVER] Waiting for Clients...")
        self._server.listen()

        while True:
            conn, addr = self._server.accept()
            print(f"[NEW CONNECTION] Connected to Client {addr}")

            # Iterate through self._games and find
            # the game with a single player
            for game_dict in self._games:
                if len(game_dict["game"].players) % 2 == 0:
                    continue
                else:
                    # Grab the existing player and
                    # figure out what index and mark
                    # the new player should have
                    existing_player = game_dict["game"].players[-1]
                    if existing_player.mark == "o":
                        index, mark = 1, "x"
                    else:
                        index, mark = 0, "o"

                    # Insert player to the game's list
                    game_dict["game"].players.insert(index, Player(index, mark))

                    # Add the client to the clients list
                    game_dict["clients"].insert(index, (conn, addr))
                    break
            else:
                # Add client to a new game
                # Create a dict for the game
                game_dict = {"game": None,
                             "clients": None}

                # Create a Game obj
                game_id = len(self._games) + 1
                game = Game(game_id, self._create_board())

                # Create a Player obj
                index, mark = 0, "o"
                game.players.append(Player(index, mark))

                # Update the game_dict and add it to self._games
                game_dict["game"], game_dict["clients"] = game, [(conn, addr)]
                self._games.append(game_dict)

            # Update the clients counter
            self._num_clients += 1

            # Create a new thread for the client
            thread = threading.Thread(target=self._handle_client,
                                    args=(conn, game_dict),
                                    daemon=True)
            thread.start()

    def _handle_client(self, conn, game_dict):
        game, clients = game_dict.values()
        self.send(game, conn)

        # to_remove = False
        game_on = True
        while game_on:
            try:

                data = self.receive(conn)


                if data:

                    if isinstance(data, list):

                        if data[0] == "!rem":
                            updated_game = data[1]
                            game = updated_game

                            if len(game.players) == 1:
                                game.board = self._create_board()

                                if game.players[-1].mark == "x":
                                    self.send(game, clients[1][0])
                                    print(f"[DISCONNECTED] {clients[0][1]}")
                                    clients.remove(clients[0])
                                    self._num_clients -= 1

                                else:
                                    self.send(game, clients[0][0])
                                    print(f"[DISCONNECTED] {clients[1][1]}")
                                    clients.remove(clients[1])
                                    self._num_clients -= 1

                                break

                            else:
                                print(f"[DISCONNECTED] {clients[-1][1]}")
                                clients.remove(clients[-1])
                                self._num_clients -= 1
                                for _game in self._games:
                                    if len(_game["clients"]) == 0:
                                        self._games.remove(_game)
                                        game_on = False

                    if not game_on:
                        print("[INFO] Game Destroyed")
                        break

                    # Update the game
                    if isinstance(data, Game):
                        game = data
                    elif isinstance(data, list):
                        game = data[1]

                    game_dict["game"], game_dict["clients"] = game, clients
                    for _game_dict in self._games:
                        index = self._games.index(_game_dict)
                        if _game_dict["game"].id == game.id:
                            self._games[index] = game_dict

                    # Send the game to the players
                    if len(game.players) == 2:
                        for client, _ in clients:
                            if client != conn:
                                self.send(game, client)
                    else:
                        self.send(game, clients[-1][0])
                    
            except:
                print("[ERROR] Unknown Error Occurred!")

    def _create_board(self):
        """Create a new board"""
        CELL_WIDTH, CELL_HEIGHT = 150, 150
        board = []

        for i in range(3):
            y = i*CELL_HEIGHT
            board.append([])
            for j in range(3):
                x = j*CELL_WIDTH
                board[i].append(0)
                board[i][j] = ["", (x, y)]

        return board


def main():
    """Create Server Obj"""
    Server()


if __name__ == "__main__":
    main()
