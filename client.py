import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        """Initierar klienten med angiven host och port."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
            print("Ansluten till servern!")
        except Exception as e:
            print(f"Kunde inte ansluta till servern: {e}")
            sys.exit(1)

    def receive_messages(self):
        """Tar emot meddelanden från servern."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    print("Anslutningen till servern bröts")
                    break
                print(message)
            except Exception as e:
                print(f"Fel vid mottagning av meddelande: {e}")
                break
        
        self.client.close()

    def send_messages(self):
        """Skickar meddelanden till servern."""
        try:
            while True:
                message = input()
                if message.lower() == 'quit':
                    break
                
                try:
                    self.client.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Kunde inte skicka meddelande: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\nAvslutar...")
        finally:
            self.client.close()

    def start(self):
        """Startar klienten och hanterar meddelanden."""
        # Starta en separat tråd för att ta emot meddelanden
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Huvudtråden används för att skicka meddelanden
        self.send_messages()

if __name__ == "__main__":
    client = ChatClient()
    client.start()