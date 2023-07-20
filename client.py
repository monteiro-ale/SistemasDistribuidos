import threading
import socket  


def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    try:
        client.connect(("localhost", 5007))
    except:
        return print('\nErro ao conectar no servidor\n')
    username = input("Digite seu usuario ")
    print('\nConectado\n')

    thread1 = threading.Thread(target=recebeMensagem, args=[client])
    thread2 = threading.Thread(target= mandaMensagem, args=[client, username])

    thread1.start()
    thread2.start()




def recebeMensagem(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg +'\n')
        except:
            print("\nNão foi possivel manter conexão com server\n")
            print("Enter para continuar")
            client.close()
            break 


def mandaMensagem(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
            if msg.lower() == "sair":
                return main()
        except:
            return


main()