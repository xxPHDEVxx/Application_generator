import tkinter as tk
from tkinter import messagebox

from generator.generator import Generator

class UrlScraperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-URL Scraper")

        self.url_entries = []

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.instructions = tk.Label(self.frame, text="Entrez les URL à scraper :")
        self.instructions.pack()

        self.entries_frame = tk.Frame(self.frame)
        self.entries_frame.pack()

        self.add_url_field()

        self.add_button = tk.Button(self.frame, text="Ajouter une URL", command=self.add_url_field)
        self.add_button.pack(pady=5)

        self.scrape_button = tk.Button(self.frame, text="Générer les lettres de motivation", command=self.launch_generation)
        self.scrape_button.pack(pady=10)

    def add_url_field(self):
        entry = tk.Entry(self.entries_frame, width=80)
        entry.pack(pady=2)
        self.url_entries.append(entry)

    def launch_generation(self):
        urls = [entry.get().strip() for entry in self.url_entries if entry.get().strip()]
        if not urls:
            messagebox.showwarning("Aucune URL", "Veuillez entrer au moins une URL.")
            return

        try:
            generator = Generator(urls)
            results = generator.run()

            # Affichage simple du titre des lettres générées
            titles = "\n".join([letter.title for letter in results])
            messagebox.showinfo("Lettres générées", f"{len(results)} lettre(s) générée(s) :\n\n{titles}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UrlScraperUI(root)
    root.mainloop()
