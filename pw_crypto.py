from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

def schluessel_aus_passwort(passwort: str, salt_datei='key.salt'):
    if not os.path.exists(salt_datei):
        with open(salt_datei, 'wb') as f:
            f.write(os.urandom(16))
    with open(salt_datei, 'rb') as f:
        salt = f.read()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(passwort.encode()))

def laden_und_entschluesseln(dateiname, fernet):
    if not os.path.exists(dateiname):
        return []
    with open(dateiname, 'rb') as f:
        daten = f.read()
    entschluesselt = fernet.decrypt(daten).decode('utf-8')
    return [zeile.strip().split(" | ") for zeile in entschluesselt.strip().split('\n') if zeile]

def speichern_verschluesselt(dateiname, daten_liste, fernet):
    daten_string = '\n'.join([' | '.join(eintrag) for eintrag in daten_liste])
    verschluesselt = fernet.encrypt(daten_string.encode('utf-8'))
    with open(dateiname, 'wb') as f:
        f.write(verschluesselt)
