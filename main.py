# deactivate to deactivate the virtual environment  .venv\Scripts\deactivate
# .venv\Scripts\Activate.ps1 to activate the virtual environment
# python -m venv .venv to create the virtual environment

print("hola mundo")
grupo = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

for i in range(2):
    print(grupo[i])

print("La Letra " + grupo[-1] + " esta en la posicion " + str(grupo.index(grupo[-1])+1))

print("\033[1mLa Letra " + grupo[-2] + " esta en la posicion " + str(grupo.index(grupo[-2])+1) + "\033[0m")


userinput = input("Ingrese una letra: ")

if userinput in grupo:
    print("Esta letra " + userinput + " esta en " + str(grupo.index(userinput)+1))
else:
    userinput = input("Letra minúscula por favor, no número. Ingrese una letra: ")
    if userinput in grupo:
        print("Esta letra " + userinput + " esta en " + str(grupo.index(userinput)+1))
    else:
        print("La letra ingresada no está en el grupo.")