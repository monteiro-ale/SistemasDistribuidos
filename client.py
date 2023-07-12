import socket  
import select 
import errno  
import sys

limiteHeader = 40 
hostServidor = "127.0.0.1"
portaServidor = 1234
   
nomeUsuario = input("Nome do usuário: ")


# Cria um novo objeto de socket para o cliente
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketCliente.connect((hostServidor, portaServidor))
socketCliente.setblocking(False)

nomeClienteCodificado = nomeUsuario.encode('utf-8')
headerNomeUsuario = f"{len(nomeClienteCodificado):<{limiteHeader}}".encode('utf-8')
# Envia o cabeçalho e o nome do cliente para o servidor
socketCliente.send(headerNomeUsuario + nomeClienteCodificado)

while True:
    mensagem = input(f'{nomeUsuario} Digite uma mensagem: ')

    if mensagem:
        mensagem = mensagem.encode('utf-8')
        mensagemHeader = f"{len(mensagem): {limiteHeader}}".encode('utf-8')
        socketCliente.send(mensagemHeader + mensagem) 
        #Se a mensagem for "sair" encerra o programa cliente
        if mensagem.decode().upper() == 'SAIR':
            exit()

    try:
        while True:
            headerNomeUsuario = socketCliente.recv(limiteHeader)

            if not len(headerNomeUsuario):
                print('Conexao Fechada')
                sys.exit()

            usernameLength = int(headerNomeUsuario.decode('utf-8').strip())
            nomeClienteCodificado = socketCliente.recv(usernameLength).decode('utf-8')

            mensagemHeader = socketCliente.recv(limiteHeader)
            mensagemLength = int(mensagemHeader.decode('utf-8').strip())  
            mensagem = socketCliente.recv(mensagemLength).decode('utf-8')

            print(f'{nomeClienteCodificado} > {mensagem}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erro: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:
        print('Erro: '.format(str(e)))
        sys.exit()
