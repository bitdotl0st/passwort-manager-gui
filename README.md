# 🔐 Passwort-Manager mit GUI & AES-Verschlüsselung

Ein sicherer, lokal verschlüsselter Passwortgenerator und -verwalter in Python – ideal für dein Cybersecurity-Portfolio.  
Enthält Passwortstärke-Bewertung, moderne GUI und vollständige AES-Verschlüsselung.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![GUI](https://img.shields.io/badge/interface-GUI%20(ttk)-lightgrey?logo=windows)
![Encryption](https://img.shields.io/badge/encryption-AES256-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/project-stable-brightgreen)


---
![Vorschau](sc1.png)

## Funktionen

✅ Passwort-Generator (Länge & Zeichentypen wählbar)  
✅ Passwortstärke-Anzeige  
✅ In Zwischenablage kopieren  
✅ Dienste + Passwörter lokal verschlüsselt speichern  
✅ Verwaltung mit Suchfunktion, Kopieren, Löschen  
✅ Verschlüsselung mit Master-Passwort (AES via `Fernet`)  
✅ GUI mit `tkinter` & `ttk` – keine externe GUI-Frameworks nötig

---

## Schnellstart

1. **Repository klonen oder herunterladen**
git clone https://github.com/dein-nutzername/passwort-manager.git
cd passwort-manager

2. **Abhängigkeiten installieren**
pip install cryptography pyperclip

3. **Tool starten**
python gui_tool.py

**Beim ersten Start wird nach einem Master-Passwort gefragt.**
**Dieses verschlüsselt deine Passwortdaten in der Datei passwoerter.enc.**

Hinweise zur Verwendung
Der Master-Key wird nicht gespeichert – vergiss ihn nicht!

Beim ersten Start werden key.salt & passwoerter.enc automatisch erstellt

Du kannst mehrere Dienste und Passwörter sicher verwalten

Keine Cloud – alles lokal & verschlüsselt