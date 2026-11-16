#!/usr/bin/env python3
"""
Macchina TARGET in ascolto su una porta UDP (per il laboratorio).
Misura quanti pacchetti riesce a ricevere: in condizioni normali li
riceve tutti; sotto un UDP flood vede pacchetti persi e latenze.

USO:
    python udp_target.py --port 137
"""

import argparse
import socket
import time


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ricevitore UDP per simulare la macchina target")
    parser.add_argument("--port", type=int, default=137,
                        help="Porta UDP su cui ascoltare")
    parser.add_argument("--addr", default="192.168.50.105",
                        help="Indirizzo da bindare")
    parser.add_argument("--recv-size", type=int, default=65535,
                        help="Dimensione massima buffer di ricezione")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Buffer di ricezione ampio: simula un servizio UDP reale
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
    sock.bind((args.addr, args.port))
    print(f"Target in ascolto su {args.addr}:{args.port}/udp "
          f"(Ctrl+C per fermare)")

    received = 0
    start = time.time()
    try:
        while True:
            data, _addr = sock.recvfrom(args.recv_size)
            received += 1
            if received % 10000 == 0:
                elapsed = time.time() - start
                print(f"  {received} pacchetti ricevuti "
                      f"({received / elapsed:,.0f} pkt/s)")
    except KeyboardInterrupt:
        print()
    finally:
        sock.close()
        elapsed = time.time() - start
        if elapsed > 0:
            print(f"Totale: {received} pacchetti in {elapsed:.2f}s "
                  f"-> {received / elapsed:,.0f} pkt/s medi")


if __name__ == "__main__":
    main()
