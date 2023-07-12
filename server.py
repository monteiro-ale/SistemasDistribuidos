import socket  
import select 

limiteHeader = 40 
hostServidor = "127.0.0.1"
portaServidor = 1234

socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 # Permite a reutilização do endereço de IP
socketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServidor.bind((hostServidor, portaServidor))
socketServidor.listen()

listaSockets = [socketServidor]

clients = {}

def recebeMensagem(client_socket):
    try:
        mensagemHeader = client_socket.recv(limiteHeader)

        if not len(mensagemHeader):
            return False

        mensagemLength = int(mensagemHeader.decode("utf-8").strip())
        return {"header": mensagemHeader, "data" : client_socket.recv(mensagemLength)}

    except:
        return False


while True:
     # Utiliza a função select para monitorar os sockets
    leituraSocket, _, socketsExceptions = select.select(listaSockets, [], listaSockets)

    for socketNotified in leituraSocket:
        # Verifica se o socket notificado é o socket do servidor
        if socketNotified == socketServidor:
            socketCliente, enderecoCliente = socketServidor.accept()

            user = recebeMensagem(socketCliente)
            if user is False:
                continue

            listaSockets.append(socketCliente) 
            clients[socketCliente] = user

            print("Nova conexão aceita!")
            print(f"Nova conexão aceita do endereço {enderecoCliente[0]}:{enderecoCliente[1]} nome: {user['data'].decode('utf-8')}")

        else:
            mensagem = recebeMensagem(socketNotified)

            if mensagem is False:
                print(f"Conexão encerrada {clients[socketNotified]['data'].decode('utf-8')}")
                listaSockets.remove(socketNotified)

            user = clients[socketNotified]
            mensagemRecebida = mensagem['data'].decode('utf-8') 
            print("########## Mensagem recebida ##########: " + mensagem['data'].decode('utf-8')) 

            if mensagemRecebida.upper() == 'SAIR':
                exit()

            for socketCliente in clients:
                if socketCliente != socketNotified:
                    socketCliente.send(user['header'] + mensagem['header'] + mensagem['data'])

    for socketNotified in socketsExceptions:
         # Remove o socket da lista de sockets monitorados em caso de exceção
        listaSockets.remove(socketNotified) 