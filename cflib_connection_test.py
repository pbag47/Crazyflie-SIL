

import time
import threading
import cflib
import cflib.crtp
from cflib.crazyflie import Crazyflie
from tcp_bridge import TcpUdpBridge


CF_CONNECTED = threading.Event()


def connected(link_uri):
    global CF_CONNECTED
    print(f'Connected to {link_uri}')
    cf.commander.send_setpoint(0, 0, 0, 0) 
    CF_CONNECTED.set()
    

def disconnected(link_uri):
    global CF_CONNECTED
    CF_CONNECTED.clear()
    cf.commander.send_setpoint(0, 0, 0, 0) 
    print(f'Disconnected from {link_uri}')


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    URI = 'udp://localhost:3458'

    cf = Crazyflie(rw_cache='./cache')
    cf.connected.add_callback(connected)
    cf.disconnected.add_callback(disconnected)
    cf.packet_received.add_callback(lambda packet: print(f'Paquet reçu : {packet}'))

    bridge = TcpUdpBridge()
    bridge.start()

    print(f'Connecting to {URI}')
    cf.open_link(URI)
    try:
        if CF_CONNECTED.wait(timeout=60):
            cf.commander.send_setpoint(0, 0, 0, 0)   # déverrouille la poussée
            for _ in range(50):
                cf.commander.send_setpoint(0, 0, 0, 10000)
                time.sleep(0.02)
    finally:
        cf.close_link()
        bridge.stop()
