# 🔐 Passwort-Manager mit GUI & AES-Verschlüsselung

Ein vollständiger, lokal verschlüsselter Passwort-Manager mit moderner Oberfläche.  
Ideal für dein Cybersecurity-Portfolio – entwickelt mit Python & `tkinter`.

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