import socket
import random

def genera_pacchetto(dim: int = 1024) -> bytes:
    """Costruisce un pacchetto di `dim` byte (1 KB) con byte casuali."""
    # random.getrandbits produce bit casuali; li convertiamo in byte
    return random.randbytes(dim)

def main() -> None:
    # 1. Input IP della macchina target
    ip_target = input("Inserisci l'IP della macchina target: ").strip()

    # 2. Input porta UDP target
    while True:
        try:
            porta_target = int(input("Inserisci la porta UDP della macchina target: "))
            break
        except ValueError:
            print("Porta non valida, inserisci un numero intero tra 1 e 65535.")

    # 3. Numero di pacchetti da inviare
    while True:
        try:
            num_pacchetti = int(input("Quanti pacchetti da 1 KB vuoi inviare? "))
            if num_pacchetti <= 0:
                raise ValueError
            break
        except ValueError:
            print("Numero non valido, inserisci un numero intero maggiore di 0.")

    # Creazione del socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Ogni pacchetto da 1 KB con byte casuali
        pacchetto = genera_pacchetto(1024)

        print(f"\nInvio di {num_pacchetti} pacchetti da 1 KB a {ip_target}:{porta_target} ...")
        for i in range(num_pacchetti):
            s.sendto(pacchetto, (ip_target, porta_target))
            print(f"Pacchetto {i + 1}/{num_pacchetti} inviato.")

    print("\nTrasmissione completata.")

if __name__ == "__main__":
    main()
