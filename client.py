import socket
import json
import sys 

class Client:
    def __init__(self):
        self.current_board = []
        self.current_player = ''
        self.winner = ''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect(('', 1213))
            print("conectado")
        except socket.error:
            print("no fue posible conectar")
            exit(0)

        #se concatena string y jugador que realiza jygada
        self.sock.sendall(b'ready')
        self.player_id = self.sock.recv(34).decode('utf-8')
        print(self.player_id)

        self.sock.recv(38)
        
        self.loop_de_cliente()

    def loop_de_cliente(self):

        #ciclo eterno para,
        # sincronizar con servidor
        # imprimir tablero, 
        # evaluar si se muestra ganador 
        while True:
            self.sincronizar_con_servidor()
            self.imprimir_tablero()

            if(self.winner != '-'):
                self.mostrar_ganador()
                break

            if(self.current_player == self.player_id):
                move = self.get_player_move()
                self.enviar_jugada(move)

    #metodo para enviar datos a servidor
    def sincronizar_con_servidor(self):
        state = self.sock.recv(333)
        print(state)
        state = json.loads(state.decode('utf-8'))
        self.current_board = state['board']
        self.current_player = state['active']
        self.winner = state['winner']

    #metodo para mostrar ganador
    def mostrar_ganador(self):
        print("\n")
        
        win = "UD. HA GANADO"
        
        lose = "UD. HA PERDIDO"

        if(self.winner == self.player_id):
            print(win)
        else:
            print(lose)

    #metodo para mostrar tablero
    def imprimir_tablero(self):
        output = ""
        for row in self.current_board[::-1]:
            for e in row:
                #si es vacio
                if e == '-':
                    output += '⚪️'
                #si juega A
                if e == 'A':
                    output += '🔴'
                #si juega B
                if e == 'B':
                    output += '🔵'
            output += '\n'

        output += ' 1 2 3 4 5 6 7 \n'

        sys.stdout.write("\033[H")
        sys.stdout.write("\033[2J")
        sys.stdout.write("%s" % output)

    def get_player_move(self):
        valid_input = False

        while(not valid_input):
            message = input("ingrese el numero de columna deseado: ")
            col = message[0]
            if(col.isdigit() and int(col) > 0 and int(col) <= len(self.current_board[0])):
                valid_input = True
            else:
                print("\nnot valid input, try again")

        col = str(int(col) - 1)
        return col

    def enviar_jugada(self, move):
        message = self.player_id
        message += move
        message = bytes(message, 'utf-8')
        print(message)
        print(sys.getsizeof(message))
        self.sock.sendall(message)

if __name__ == "__main__":
    Client()