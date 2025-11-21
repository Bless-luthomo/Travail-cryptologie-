repertoire = {}

def message_to_code(message: str) -> int:
    """
    Génère un code numérique unique pour un message.
    Toujours le même si le message est le même.
    """
    code = 0
    for ch in message:
        code = (code * 31 + ord(ch)) % 10**12  # max 12 chiffres
    return code

def encoder(message: str) -> int:
    """
    Encode un message clair et stocke l'association
    pour permettre le décodage plus tard.
    """
    code = message_to_code(message)

    # On stocke la correspondance
    repertoire[code] = message

    return code

def decoder(code: int) -> str:
    """
    Décode un code si l'association existe.
    """
    if code in repertoire:
        return repertoire[code]
    else:
        return "Code inconnu (pas encore encodé)"

# ==========================
#   PROGRAMME INTERACTIF
# ==========================

while True:
    print("\n=== SYSTEME ENCODEUR / DECODEUR ===")
    print("1 - Encoder un message clair")
    print("2 - Décoder un code")
    print("3 - Quitter")

    choix = input("\nVotre choix : ")

    if choix == "1":
        message = input("Entrez le message clair : ")
        code = encoder(message)
        print("Code associé :", code)

    elif choix == "2":
        code_str = input("Entrez le code : ")
        if code_str.isdigit():
            code = int(code_str)
            print("Message clair :", decoder(code))
        else:
            print("Code invalide")

    elif choix == "3":
        print("Fin du programme.")
        break
    else:
        print("Choix invalide.")