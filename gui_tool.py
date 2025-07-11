import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import string
import random
import pyperclip
from datetime import datetime
from pw_crypto import schluessel_aus_passwort, laden_und_entschluesseln, speichern_verschluesselt
from cryptography.fernet import Fernet, InvalidToken

DATEI = "passwoerter.enc"
eintraege = []  # Globale Passwortliste

# ---------- Passwortgenerierung ----------
def generiere_passwort():
    try:
        laenge = int(e_laenge.get())
    except ValueError:
        messagebox.showerror("Fehler", "Ungültige Länge.")
        return

    zeichen = ''
    if var_gross.get(): zeichen += string.ascii_uppercase
    if var_klein.get(): zeichen += string.ascii_lowercase
    if var_zahl.get(): zeichen += string.digits
    if var_sonder.get(): zeichen += string.punctuation

    if not zeichen:
        messagebox.showerror("Fehler", "Mindestens eine Zeichengruppe auswählen.")
        return

    pw = ''.join(random.choice(zeichen) for _ in range(laenge))
    label_passwort.config(text=f"🔐 Passwort: {pw}")
    pyperclip.copy(pw)
    label_clipboard.config(text="📋 In Zwischenablage kopiert!")
    bewertung = bewerte_passwort(pw)
    label_staerke.config(text=f"📊 Stärke: {bewertung}")

    # Speichern
    if speichern_var.get():
        dienst = e_dienst.get().strip()
        if not dienst:
            messagebox.showerror("Fehler", "Dienstname erforderlich.")
            return
        zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        eintraege.append([zeit, dienst, pw])
        speichern_verschluesselt(DATEI, eintraege, fernet)
        lade_liste()
        label_speichern.config(text="💾 Gespeichert!")

# ---------- Passwortbewertung ----------
def bewerte_passwort(pw):
    punkte = 0
    if any(c.islower() for c in pw): punkte += 1
    if any(c.isupper() for c in pw): punkte += 1
    if any(c.isdigit() for c in pw): punkte += 1
    if any(c in string.punctuation for c in pw): punkte += 1
    if len(pw) < 8:
        return "❌ Schwach"
    elif len(pw) >= 12 and punkte == 4:
        return "✅ Stark"
    else:
        return "⚠️ Mittel"

# ---------- Liste laden / anzeigen ----------
def lade_liste():
    for row in tree.get_children():
        tree.delete(row)
    for eintrag in eintraege:
        tree.insert("", "end", values=eintrag)

# ---------- Suchfunktion ----------
def suche():
    query = e_suche.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for eintrag in eintraege:
        if query in eintrag[1].lower():
            tree.insert("", "end", values=eintrag)

# ---------- Löschen ----------
def loesche_auswahl():
    auswahl = tree.selection()
    if not auswahl:
        return
    index = tree.index(auswahl[0])
    if messagebox.askyesno("Löschen", "Eintrag wirklich löschen?"):
        del eintraege[index]
        speichern_verschluesselt(DATEI, eintraege, fernet)
        lade_liste()

# ---------- Kopieren ----------
def kopiere_passwort():
    auswahl = tree.selection()
    if not auswahl:
        return
    index = tree.index(auswahl[0])
    pw = eintraege[index][2]
    pyperclip.copy(pw)
    messagebox.showinfo("Kopiert", "Passwort in Zwischenablage.")

# ---------- GUI Aufbau ----------
def baue_gui():
    global e_laenge, var_gross, var_klein, var_zahl, var_sonder, e_dienst
    global speichern_var, label_passwort, label_clipboard, label_staerke, label_speichern
    global e_suche, tree

    root = tk.Tk()
    root.title("🔐 Passwort-Tool")
    root.geometry("700x600")
    root.resizable(False, False)

    # --- Generator ---
    frame_gen = ttk.LabelFrame(root, text="Passwort generieren")
    frame_gen.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_gen, text="Länge:").grid(row=0, column=0, sticky="w")
    e_laenge = ttk.Entry(frame_gen, width=5)
    e_laenge.insert(0, "16")
    e_laenge.grid(row=0, column=1, padx=5)

    var_gross = tk.BooleanVar(value=True)
    var_klein = tk.BooleanVar(value=True)
    var_zahl = tk.BooleanVar(value=True)
    var_sonder = tk.BooleanVar(value=True)

    ttk.Checkbutton(frame_gen, text="Groß", variable=var_gross).grid(row=0, column=2)
    ttk.Checkbutton(frame_gen, text="Klein", variable=var_klein).grid(row=0, column=3)
    ttk.Checkbutton(frame_gen, text="Zahlen", variable=var_zahl).grid(row=0, column=4)
    ttk.Checkbutton(frame_gen, text="Sonderz.", variable=var_sonder).grid(row=0, column=5)

    ttk.Label(frame_gen, text="Dienst:").grid(row=1, column=0, sticky="w", pady=5)
    e_dienst = ttk.Entry(frame_gen, width=30)
    e_dienst.grid(row=1, column=1, columnspan=3, sticky="w", pady=5)

    speichern_var = tk.BooleanVar()
    ttk.Checkbutton(frame_gen, text="Speichern", variable=speichern_var).grid(row=1, column=4)

    ttk.Button(frame_gen, text="Generieren", command=generiere_passwort).grid(row=1, column=5)

    label_passwort = ttk.Label(frame_gen, text="🔐 Passwort: ")
    label_passwort.grid(row=2, column=0, columnspan=6, sticky="w", pady=(10, 0))

    label_staerke = ttk.Label(frame_gen, text="📊 Stärke: ")
    label_staerke.grid(row=3, column=0, columnspan=6, sticky="w")

    label_clipboard = ttk.Label(frame_gen, text="", foreground="green")
    label_clipboard.grid(row=4, column=0, columnspan=6, sticky="w")

    label_speichern = ttk.Label(frame_gen, text="", foreground="blue")
    label_speichern.grid(row=5, column=0, columnspan=6, sticky="w", pady=(0, 5))

    # --- Verwaltung ---
    frame_verwaltung = ttk.LabelFrame(root, text="Passwortverwaltung")
    frame_verwaltung.pack(fill="both", expand=True, padx=10, pady=5)

    ttk.Label(frame_verwaltung, text="Suche:").pack(anchor="w")
    e_suche = ttk.Entry(frame_verwaltung, width=30)
    e_suche.pack(anchor="w")
    ttk.Button(frame_verwaltung, text="🔍 Suche", command=suche).pack(anchor="w", pady=2)

    tree = ttk.Treeview(frame_verwaltung, columns=("zeit", "dienst", "passwort"), show="headings")
    tree.heading("zeit", text="Zeit")
    tree.heading("dienst", text="Dienst")
    tree.heading("passwort", text="Passwort")
    tree.pack(fill="both", expand=True, pady=5)

    btns = ttk.Frame(frame_verwaltung)
    btns.pack()
    ttk.Button(btns, text="📋 Kopieren", command=kopiere_passwort).grid(row=0, column=0, padx=5)
    ttk.Button(btns, text="❌ Löschen", command=loesche_auswahl).grid(row=0, column=1, padx=5)

    root.mainloop()

# ---------- Start ----------
if __name__ == "__main__":
    # Master-Passwort abfragen
    master = simpledialog.askstring("Authentifizierung", "Master-Passwort eingeben:", show="*")
    if not master:
        exit()

    try:
        key = schluessel_aus_passwort(master)
        fernet = Fernet(key)
        eintraege = laden_und_entschluesseln(DATEI, fernet)
    except InvalidToken:
        messagebox.showerror("Fehler", "Falsches Master-Passwort oder beschädigte Datei.")
        exit()

    baue_gui()
