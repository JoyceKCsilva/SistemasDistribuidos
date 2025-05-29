import socket
import threading

# Configurações do servidor
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede
PORT = 12345      # Porta para a comunicação

# Lista para salvar conexões de clientes
clients = []

# Função para lidar com cada cliente
def handle_client(client_socket, client_address):
    print(f"[NOVA CONEXÃO] {client_address} conectado.")
    clients.append(client_socket)

    try:
        while True:
            # Recebe mensagem do cliente
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"[MENSAGEM DE {client_address}]: {message}")
            
            # Retransmite a mensagem para todos os clientes conectados
            broadcast_message(f"{client_address}: {message}")
    except Exception as e:
        print(f"[ERRO] {client_address}: {e}")
    finally:
        print(f"[DESCONECTADO] {client_address} desconectou.")
        clients.remove(client_socket)
        client_socket.close()

# Função para enviar mensagens para todos os clientes conectados
def broadcast_message(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)

# Função para entrada do servidor para enviar mensagens aos clientes
def server_send_messages():
    while True:
        message = input("[SERVIDOR] Digite uma mensagem para os clientes: ")
        broadcast_message(f"[SERVIDOR]: {message}")

# Função principal para iniciar o servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVIDOR INICIADO] Escutando em {HOST}:{PORT}...")

    # Thread para permitir que o servidor envie mensagens
    threading.Thread(target=server_send_messages, daemon=True).start()

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 2}")  # Subtraindo 2 (thread principal e de envio do servidor)

if __name__ == "__main__":
    start_server()