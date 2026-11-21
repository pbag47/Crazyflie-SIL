
import socket
import threading
import time
import logging


logging.basicConfig(format='%(asctime)s.%(msecs)03d %(message)s', level=logging.INFO)

RADIO_RAW = 0x00  # à vérifier dans syslink.h


class TcpUdpBridge:
    def __init__(self, 
                 tcp_host='localhost', 
                 tcp_port=3457, 
                 udp_host='localhost', 
                 udp_port=3458,
                 client=None,
                 ):
        self.tcp_host = tcp_host
        self.tcp_port = tcp_port
        self.udp_host = udp_host
        self.udp_port = udp_port
        self.client = client
        self.tcp = None
        self.udp = None
        self.tcp_udp_thread = threading.Thread(target=self.renode_to_cflib, daemon=True)
        self.udp_tcp_thread = threading.Thread(target=self.cflib_to_renode, daemon=True)
        self.stop_flag = threading.Event()
        logging.info(f'Bridge TCP {tcp_host}:{tcp_port} <-> UDP {udp_host}:{udp_port} initialized')

    def start(self):
        logging.info('Starting TCP <-> UDP bridge')
        self.stop_flag.clear()
        self.tcp = socket.create_connection((self.tcp_host, self.tcp_port))
        self.tcp.settimeout(0.5)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind((self.udp_host, self.udp_port))
        self.udp.settimeout(0.5)
        self.tcp_udp_thread.start()
        self.udp_tcp_thread.start()
        logging.info('TCP <-> UDP bridge started')

    def stop(self):
        logging.info('Stopping TCP <-> UDP bridge')
        self.stop_flag.set()
        self.tcp_udp_thread.join(timeout=1)
        self.udp_tcp_thread.join(timeout=1)
        self.tcp.close()
        self.udp.close()
        logging.info('TCP <-> UDP bridge stopped')

    def cflib_to_renode(self):
        while not self.stop_flag.is_set():
            try:
                data, self.client = self.udp.recvfrom(1024)
            except socket.timeout:
                continue
            logging.info(f'UDP -> Renode : {data.hex(" ")}')
            if data[0] == 0xFF:  # connection packet
                continue
            # self.tcp.sendall(frame(RADIO_RAW, data[:-1]))   # remove checksum and send
            # self.tcp.sendall(frame(RADIO_RAW, data)) 
            f = frame(RADIO_RAW, data)
            logging.info(f'Bridge -> Renode : {f.hex(" ")}')
            self.tcp.sendall(f)

    def renode_to_cflib(self):
        buf = b''
        while not self.stop_flag.is_set():
            try:
                chunk = self.tcp.recv(1024)
            except socket.timeout:
                continue
            logging.info(f'Renode -> bridge : {chunk.hex(" ")}')
            buf += chunk
            frames, buf = parse(buf)
            for type_, payload in frames:
                if type_ == RADIO_RAW and self.client:
                    # ck = bytes([sum(payload) & 0xFF])  # checksum
                    # self.udp.sendto(payload + ck, self.client)
                    self.udp.sendto(payload, self.client)


def cksum(buf):
    a = b = 0
    for x in buf:
        a = (a + x) & 0xFF
        b = (b + a) & 0xFF
    return bytes([a, b])


def frame(type_, data):
    body = bytes([type_, len(data)]) + data
    return b'\xBC\xCF' + body + cksum(body)


def parse(buf):
    """Renvoie ([(type, data), ...], reste non consommé)."""
    out = []
    while True:
        i = buf.find(b'\xBC\xCF')
        if i < 0:
            return out, b''
        buf = buf[i:]
        if len(buf) < 4 or len(buf) < 6 + buf[3]:
            return out, buf
        n = buf[3]
        body, ck = buf[2:4 + n], buf[4 + n:6 + n]
        if cksum(body) == ck:
            out.append((body[0], body[2:]))
            buf = buf[6 + n:]
        else:
            logging.warning('Checksum invalid')
            buf = buf[2:]  # fausse synchro, on réessaie


if __name__ == '__main__':
    bridge = TcpUdpBridge()
    bridge.start()
    time.sleep(10)
    bridge.stop()
