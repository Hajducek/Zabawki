import socket
import paramiko
import threading
import sys

host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'Wojtek') and (password == 'WUNSZ'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Nasluchiwanie polaczen...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Nasluch sie nie udal: ' + str(e)
    sys.exit(1)
print '[+] Jest polaczenie!'

try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] Negocjacja SSH nie powiodla sie.'
    chan = bhSession.accept(20)
    print '[+] Uwierzytelniono!'
    print chan.recv(1024)
    chan.send('Witaj w bh_ssh')
    while True:
        try:
            command = raw_input("Wprowadz polecenie: ").strip('\n')
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print 'exiting'
                bhSession.close()
                raise Exception ('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception, e:
    print '[-] Przechwycono wyjatek: ' + str(e)
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)