import tkinter as tk
from tkinter import filedialog, messagebox

# Funzione per leggere il contenuto di un file SRT
def leggi_file_srt(nome_file):
    with open(nome_file, 'r', encoding='utf-8') as file:
        return file.read().split('\n\n')

# Funzione per unire i file SRT
def unisci_srt():
    if not eng_path or not ita_path:
        messagebox.showerror("Error", "Upload both files before proceeding!")
        return

    try:
        eng_srt = leggi_file_srt(eng_path)
        ita_srt = leggi_file_srt(ita_path)

        # Controlla se i due file SRT hanno lo stesso numero di righe
        if len(eng_srt) != len(ita_srt):
            messagebox.showerror("Error", "The subtitle files have a different number of lines!")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("File SRT", "*.srt")])
        if not output_file:
            return

        with open(output_file, 'w', encoding='utf-8') as out_file:
            for i in range(len(eng_srt)):  # Ora usiamo len(eng_srt), visto che hanno la stessa lunghezza
                eng_subtitle = eng_srt[i].split('\n')
                ita_subtitle = ita_srt[i].split('\n')

                # Estrai i dettagli del sottotitolo
                index = eng_subtitle[0]
                time_range = eng_subtitle[1]
                eng_text = '\n'.join(eng_subtitle[2:])
                ita_text = '\n'.join(ita_subtitle[2:])

                # Scrivi nel nuovo file SRT
                out_file.write(f"{index}\n{time_range}\n{eng_text}\n{'-'*60}\n{'-'*60}\n{ita_text}\n\n")
        
        messagebox.showinfo("Success", "Files merged successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Funzioni per caricare i file
def carica_eng():
    global eng_path
    eng_path = filedialog.askopenfilename(filetypes=[("File SRT", "*.srt")])
    if eng_path:
        eng_label.config(text=f"First subtitle: {eng_path.split('/')[-1]}")

def carica_ita():
    global ita_path
    ita_path = filedialog.askopenfilename(filetypes=[("File SRT", "*.srt")])
    if ita_path:
        ita_label.config(text=f"Second subtitle: {ita_path.split('/')[-1]}")

# Inizializza l'interfaccia Tkinter
root = tk.Tk()
root.title("Subtitles Manager")
root.geometry("500x300")

eng_path = ""
ita_path = ""

# Layout della GUI
tk.Label(root, text="Merge SRT Files", font=("Arial", 16)).pack(pady=10)

eng_button = tk.Button(root, text="Upload first subtitle", command=carica_eng)
eng_button.pack(pady=5)

eng_label = tk.Label(root, text="No file uploaded", fg="gray")
eng_label.pack()

ita_button = tk.Button(root, text="Upload second subtitle", command=carica_ita)
ita_button.pack(pady=5)

ita_label = tk.Label(root, text="No file uploaded", fg="gray")
ita_label.pack()

merge_button = tk.Button(root, text="Merge files", command=unisci_srt, bg="#4caf50", fg="white")
merge_button.pack(pady=20)

# Avvia la finestra
root.mainloop()
