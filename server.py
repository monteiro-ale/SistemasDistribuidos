import threading
import socket  


array_clientes = []

def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(("localhost", 5007))
        server.listen()
    except:
        return print("Erro ao iniciar o server")
    
    
    while True:
        cliente, end = server.accept()
        array_clientes.append(cliente)
        thread = threading.Thread(target=tratamentoMensagem, args=[cliente])
        thread.start()



def tratamentoMensagem(client):
    while True:
        try:
            msg = client.recv(2048)
            decodada = msg.decode('utf-8')
            print("Mensagem aqui:", decodada)
            palavras = decodada.split()
            primeira_palavra = palavras[1]
            tamanho_arr = (len(palavras))
            if tamanho_arr == 2 and primeira_palavra.lower() == "sair":
                deletaCliente(client)
            broadcast(msg, client)
        except:
            deletaCliente(client)
            break

def broadcast(msg, client):
    for cliente in array_clientes:
        if cliente != client:
            try:
                cliente.send(msg)
            except:
                deletaCliente(cliente)

def deletaCliente(client):
    array_clientes.remove(client)


main()