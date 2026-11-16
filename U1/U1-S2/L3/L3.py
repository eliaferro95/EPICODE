

print("Calcolatore di perimetri per diverse figure geometriche")
print("scegli figura?: ")
print("1 - Quadrato")
print("2 - Cerchio")
print("3 - Rettangolo")

scelta = input("Quale figura geometrica?: ")

def perimetro_quadrato(lato):
    return lato * 4

def perimetro_cerchio(raggio):
    return 2 * 3.14 * raggio

def perimetro_rettangolo(base, altezza):
    return 2 * (base + altezza)

def main():

 if scelta == '1':
     lato = float(input("Immetti lungezza del lato del Quadrato: "))
     perimetro = perimetro_quadrato(lato)
     print(f"Il perimetro del quadrato è {perimetro}")

 elif scelta == '2':
     raggio = float(input("Immetti lunghezza del raggio del Cerchio: "))
     perimetro = perimetro_cerchio(raggio)
     print(f"Il perimetro del cerchio è {perimetro}")

 elif scelta == '3':
     altezza = float(input("Immetti l'altezza del rettangolo: "))
     base = float(input("Immetti la lunghezza della base del Rettangolo: "))
     perimetro = perimetro_rettangolo(base + altezza)
     print(f"Il perimetro del rettangolo è {perimetro}")

 else:
     print("Comando non valido, Riprovare")

if __name__ == "__main__":
    main()