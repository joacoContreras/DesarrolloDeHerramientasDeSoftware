x = None
while x == None :
    try:
        x = int(input("Ingrese entero: "))
        print(x)
    except KeyboardInterrupt :
        print("Detenido")
    except ValueError :
        print("No se puede convertir")
        print("Vuelva a intentarlo")

print("Fin")