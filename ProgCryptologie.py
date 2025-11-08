import math

# ---------- Méthode 1 : Substitution (César) ----------
def caesar_encrypt(text, shift):
    shift = shift % 26
    result = []
    for c in text.upper():
        if 'A' <= c <= 'Z':
            enc = chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
            result.append(enc)
        else:
            result.append(c)
    return ''.join(result)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ---------- Méthode 2 : Transposition ----------
def transposition_encrypt(text, key):
    clean = text.replace(" ", "")
    cols = len(key)
    rows = math.ceil(len(clean) / cols)
    grid = [['X']*cols for _ in range(rows)]

    # remplir la grille
    index = 0
    for r in range(rows):
        for c in range(cols):
            if index < len(clean):
                grid[r][c] = clean[index]
                index += 1

    # ordre des colonnes selon la clé
    order = sorted(range(len(key)), key=lambda i: key[i])
    result = []
    for c in order:
        for r in range(rows):
            result.append(grid[r][c])
    return ''.join(result)

def transposition_decrypt(cipher, key):
    cols = len(key)
    rows = math.ceil(len(cipher) / cols)
    grid = [['']*cols for _ in range(rows)]

    order = sorted(range(len(key)), key=lambda i: key[i])
    index = 0
    for c in order:
        for r in range(rows):
            if index < len(cipher):
                grid[r][c] = cipher[index]
                index += 1

    result = []
    for r in range(rows):
        for c in range(cols):
            result.append(grid[r][c])
    return ''.join(result).rstrip('X')

# ---------- Méthode 3 : Répertoire ----------
def normalize_phrase(s):
    return ' '.join(s.strip().upper().split())

def repertoire_encrypt(text, code):
    if not text:
        return ""
    norm_map = {normalize_phrase(k): v for k, v in code.items()}
    max_words = max(len(k.split()) for k in norm_map)

    tokens = text.strip().split()
    out = []
    i = 0
    while i < len(tokens):
        matched = False
        max_try = min(max_words, len(tokens)-i)
        for length in range(max_try, 0, -1):
            attempt = normalize_phrase(' '.join(tokens[i:i+length]))
            if attempt in norm_map:
                out.append(norm_map[attempt])
                i += length
                matched = True
                break
        if not matched:
            out.append(tokens[i])
            i += 1
    return ' '.join(out)

def repertoire_decrypt(text, code):
    if not text:
        return ""
    inverse = {v: normalize_phrase(k) for k,v in code.items()}
    tokens = text.strip().split()
    return ' '.join([inverse.get(t, t) for t in tokens])

# ---------- Programme principal ----------
def main():
    print("===  Programme de Cryptologie ===")
    print("1. Substitution (César)")
    print("2. Transposition")
    print("3. Répertoire")
    choix = input("Choisissez une méthode (1-3) : ").strip()

    action = input("Voulez-vous chiffrer (E) ou déchiffrer (D) ? ").strip().upper()
    if action not in ['E','D']:
        print("Action invalide."); return

    resultat = ""

    if choix == "1":
        texte = input("Entrez le texte : ")
        try:
            shift = int(input("Entrez le décalage (ex : 3) : "))
        except:
            print("Décalage invalide."); return
        resultat = caesar_encrypt(texte, shift) if action=="E" else caesar_decrypt(texte, shift)

    elif choix == "2":
        texte = input("Entrez le texte : ")
        try:
            key = list(map(int, input("Entrez la clé (ex : 3 1 4 2 5) : ").split()))
        except:
            print("Clé invalide."); return
        resultat = transposition_encrypt(texte, key) if action=="E" else transposition_decrypt(texte, key)

    elif choix == "3":
        try:
            n = int(input("Combien de mots/phrases voulez-vous définir dans le répertoire ? "))
            if n<=0: raise Exception()
        except:
            print("Nombre invalide."); return

        repertoire = {}
        for i in range(1, n+1):
            mot = input(f"\nDéfinition #{i}\nMot/phrase clair : ")
            code = input("Code pour ce mot/phrase : ")
            if not mot.strip() or not code.strip():
                print("Entrée vide, recommencez cette définition.")
                i -= 1
                continue
            repertoire[mot] = code

        texte = input("\nEntrez le texte à traiter : ")
        resultat = repertoire_encrypt(texte, repertoire) if action=="E" else repertoire_decrypt(texte, repertoire)

    else:
        print("Choix invalide (1-3)."); return

    print("\nRésultat : " + resultat)

if __name__ == "__main__":
    main()