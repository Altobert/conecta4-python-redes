import socket
import json
import sys

#Se utiliza caracteristica orientada al objeto de lenguaje python
class Server:

    #Se inicia la clase servidor
    def __init__(self):

        #se inicia juego con 6 filas y 7 columnas
        self.ROW_NUM = 6
        self.COL_NUM = 7
        self.winner = '-'

        PORT = 1213

        #se inicializa un arreglo que representara el tablero
        #se inicia cada espacio del arreglo vacio con simbolo "-"
        self.board = []
        for _ in range(7):
            self.board.append(['-']*7)

        # no funciono juego de forma automatica
        # se inicializa en nulo ambos jugadores
        self.player_a = None
        self.player_b = None

        # se inicializan los socket
        self.socket = socket.socket()
        self.socket.bind(('', PORT))
        
        #se invoca funcion para conectar jugadores
        self.connect_players()
        
        #aun no se ha tomado el turno por ningun jugador
        self.current_turn = False

        #se simula un loop hasta que algun jugador gane.
        self.game_loop()


    def connect_players(self):
        self.socket.listen(5)

        #ciclo while infinito
        ##espera hasta que ingrese un jugador 
        while True:
            self.player_a, _ = self.socket.accept()
            message = self.player_a.recv(38)
            #se concatena string al momento de inicializar terminal
            if(message == b'ready'):
                self.player_a.sendall(b'A')
                print('jugador A conectado')
                break
        
        ##espera hasta que ingrese un jugador
        while True:
            self.player_b, _ = self.socket.accept()
            message = self.player_b.recv(38)
            #entrada del segundo jugador
            if(message == b'ready'):
                self.player_b.sendall(b'B')
                print('jugador B conectado')
                break

        print('Ambos jugadores sincronizados')
        #se da inicio al juego con ambos jugadores enviando mensajes.
        self.player_a.sendall(b'start')
        self.player_b.sendall(b'start')


    def game_loop(self):
        current_player = None

        #mientras el ganador sea vacio
        while(self.winner == '-'):

            #asignar el turno hacia jugador A si no jugador B
            if(self.current_turn):
                current_player = self.player_a
            else:
                current_player = self.player_b

            self.sincronizar_cliente()

            message = (current_player.recv(35).decode('utf-8'))
            player = message[0]
            place = int(message[1])

            self.hacer_jugada(place, player)
            self.revisar_tablero()                

            self.current_turn = not self.current_turn

        self.sincronizar_cliente()
        self.player_a.close()
        self.player_b.close()

    def hacer_jugada(self, place, player):

        for c in range(7):
            if(self.board[c][place] == '-'):
                self.board[c][place] = player
                break

    def revisar_tablero(self):
        for i in range(self.ROW_NUM):
            for j in range(self.COL_NUM):
                self.check_spot(i, j)

    def check_spot(self, row, col):
        current = self.board[row][col]
        if current != '-':
            for i in range(4):
                if self.in_board(row + i, col) and current != self.board[row + i][col]:
                    break
            else:
                self.winner = current

            for i in range(4):
                if self.in_board(row, col + i) and current != self.board[row][col + i]:
                    break
            else:
                self.winner = current

            for i in range(4):
                if self.in_board(row + i, col + i) and current != self.board[row][col + i]:
                    break
            else:
                self.winner = current

    def in_board(self, row, col):
        if row >= 0 and row < self.ROW_NUM:
            if col >= 0 and col < self.COL_NUM:
                return True

        return False

    def sincronizar_cliente(self):
        print("traza del tablero")

        #demostracion como va quedando el tablero luego
        #de una jugada.
        package = {}
        package['board'] = self.board
        package['active'] = 'A' if self.current_turn else 'B'
        package['winner'] = self.winner

        message = bytes(json.dumps(package), 'utf-8')

        #traza de la jugada se muestra en server
        print(message)
        self.player_a.sendall(message)
        self.player_b.sendall(message)

if __name__ == "__main__":
    Server()