import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading

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

        # progress bar
        self.progress = ttk.Progressbar(self.frame, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.stop()
        self.progress.pack_forget()  # cachée au départ

    def add_url_field(self):
        entry = tk.Entry(self.entries_frame, width=80)
        entry.pack(pady=2)
        self.url_entries.append(entry)

    def launch_generation(self):
        urls = [entry.get().strip() for entry in self.url_entries if entry.get().strip()]
        if not urls:
            messagebox.showwarning("Aucune URL", "Veuillez entrer au moins une URL.")
            return

        # start progress bar
        self.progress.pack()
        self.progress.start()

        thread = threading.Thread(target=self._generate_letters, args=(urls,))
        thread.start()

    def _generate_letters(self, urls):
        try:
            generator = Generator(urls)
            results = generator.run()

            titles = "\n".join([letter.title for letter in results])
            self.root.after(0, lambda: messagebox.showinfo("Lettres générées", f"{len(results)} lettre(s) générée(s) :\n\n{titles}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Une erreur est survenue :\n{str(e)}"))
        finally:
            # stop progress bar
            self.root.after(0, self._stop_progress)

    def _stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = UrlScraperUI(root)
    root.mainloop()
