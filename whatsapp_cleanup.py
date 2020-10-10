import re

# les fonctions prennent en entrée un corpus sous la forme d'une chaîne de caractères

# on veut transformer
    # [22/03/2019 23:28:44] Alice 💞: Luxe, calme et volupté
# en :
    # BEGIN NOW Alice 💞: Luxe, calme et volupté END

stop_start = r' END\nBEGIN NOW'

def whatsapp_clean(corpus):
    result = remove_timestamps(corpus)
    result = remove_missing_files(result)
    # remove the first line of the file
    result = re.sub(r'[^\n]+\n', '', result, count=1)
    return result

def remove_timestamps(corpus) :
    pattern = r'\n\[.+ .+\]'  # saut à la ligne et timestamp
    clean = re.sub(pattern, stop_start, corpus, flags=re.IGNORECASE)
    return clean

def remove_missing_files(corpus):
    pattern = r"\n.+(image absente|document manquant|vidéo absente|GIF retiré)"
    clean = re.sub(pattern, "", corpus)
    return clean