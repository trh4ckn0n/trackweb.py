import uuid
import hashlib
from datetime import datetime
import requests
import os
import questionary
import webbrowser
import time

# === CONFIGURATION TELEGRAM ===
BOT_TOKEN = ""
CHAT_ID = ""
# === FONCTION POUR ENVOYER MESSAGE TELEGRAM ===
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# === GÉNÉRATION DU FICHIER HTML ===
def generate_html(output="spy.html"):
    uid = str(uuid.uuid4())
    timestamp = datetime.datetime.now(datetime.UTC)
    spy_hash = hashlib.sha256((uid + timestamp).encode()).hexdigest()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Document confidentiel</title>
    </head>
    <body>
        <h1>Fichier sensible - Ne pas partager</h1>
        <p>UID : {uid}</p>
        <p>Date : {timestamp}</p>
        <p>Hash : {spy_hash}</p>
        <img src="https://your-server.com/log.php?id={uid}" style="display:none;" />
    </body>
    </html>
    """

    with open(output, "w") as f:
        f.write(html)

    print(f"\n✅ Fichier HTML généré : {output}")
    print(f"📌 UID  : {uid}")
    print(f"🔒 Hash : {spy_hash}\n")
    return uid, spy_hash

# === RECHERCHE GOOGLE (DORKING) ===
def search_google(query):
    print("🔍 Recherche sur Google...")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    send_telegram(f"🔍 Nouvelle recherche en ligne : {query}\nGoogle : {url}")

# === INTERFACE INTERACTIVE ===
def main():
    os.system("clear")
    print("🕵️‍♂️ Générateur de fichier piégé HTML - trhacknon edition\n")

    action = questionary.select(
        "Que veux-tu faire ?",
        choices=[
            "1️⃣ Générer un fichier HTML piégé",
            "2️⃣ Rechercher où il a été publié",
            "❌ Quitter"
        ]).ask()

    if action.startswith("1"):
        filename = questionary.text("Nom du fichier HTML ?", default="spy.html").ask()
        uid, spy_hash = generate_html(filename)
        send_telegram(f"✅ Nouveau fichier généré\nUID : {uid}\nHash : {spy_hash}\nNom : {filename}")
        print("\n📬 UID et hash envoyés sur Telegram.")
        input("\nAppuie sur [Entrée] pour revenir au menu.")
        main()

    elif action.startswith("2"):
        hash_search = questionary.text("Hash à rechercher ? (copier depuis Telegram)").ask()
        query = f'intext:"{hash_search}"'
        search_google(query)
        input("\nAppuie sur [Entrée] pour revenir au menu.")
        main()

    else:
        print("👋 Au revoir.")
        exit()

if __name__ == "__main__":
    main()
