
import socket
import threading

import paramiko

HOST, PORT = "127.0.0.1", 2222
HOSTNAME = "Router"
PROMPT = f"\r\n{HOSTNAME}#"

host_key = paramiko.RSAKey.generate(2048)

RUNNING_CONFIG = (
    "Building configuration...\r\n\r\n"
    "Current configuration :\r\n"
    "version 16.9\r\n"
    "hostname TestRouter\r\n"
    "!\r\n"
    "interface GigabitEthernet0/0\r\n"
    " ip address 192.168.1.1 255.255.255.0\r\n"
    "!\r\n"
    "end\r\n"
)


class FakeCiscoServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        return 0

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return 0
        return 1

    def check_channel_pty_request(self, channel, term, width, height,
                                  pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def handle_client(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(host_key)
    server = FakeCiscoServer()

    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        return

    channel = transport.accept(20)
    if channel is None:
        return

    server.event.wait(5)

    channel.send(PROMPT.encode("utf-8"))

    while True:
        try:
            data = channel.recv(1024)
            if not data:
                break

            command = data.decode("utf-8", errors="ignore").strip()

        
            if "terminal width" in command:
                response = f"\r\n{command}{PROMPT}"
            elif "show running-config" in command or "sh run" in command:
                response = f"\r\n{command}\r\n{RUNNING_CONFIG}{PROMPT}"
            else:
                response = f"\r\n{command}{PROMPT}"

            channel.send(response.encode("utf-8"))
        except Exception:
            break


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(10)
    print(f"[*] Servidor SSH simulado listo en {HOST}:{PORT}...")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()


if __name__ == "__main__":
    run_server()
