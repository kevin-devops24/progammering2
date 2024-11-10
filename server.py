import socket
import threading
import sys

class ChatServer:
    def __init__(self, host='127.0.0.1', port=55555):
        """Initierar servern med angiven host och port."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # Lista för att hålla reda på anslutna klienter
        
        try:
            self.server.bind((host, port))
            self.server.listen()
            print(f"Server startad på {host}:{port}")
        except Exception as e:
            print(f"Fel vid serverstart: {e}")
            sys.exit(1)

    def broadcast(self, message, sender=None):
        """Skickar meddelande till alla anslutna klienter utom avsändaren."""
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)

    def handle_client(self, client_socket, address):
        """Hanterar kommunikation med en enskild klient."""
        try:
            # Skicka välkomstmeddelande
            client_socket.send("Välkommen till chatten!".encode('utf-8'))
            
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                
                # Broadcast meddelandet till alla andra klienter
                print(f"Meddelande från {address}: {message.decode('utf-8')}")
                self.broadcast(message, client_socket)
                
        except Exception as e:
            print(f"Fel vid hantering av klient {address}: {e}")
        finally:
            self.remove_client(client_socket)
            
    def remove_client(self, client_socket):
        """Tar bort en klient från listan och stänger anslutningen."""
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            client_socket.close()

    def start(self):
        """Startar servern och lyssnar efter nya anslutningar."""
        try:
            while True:
                client_socket, address = self.server.accept()
                print(f"Ny anslutning från {address}")
                
                self.clients.append(client_socket)
                
                # Starta en ny tråd för att hantera klienten
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nStänger servern...")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()