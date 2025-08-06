import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess
import platform
from pathlib import Path

from generator.generator import Generator
from config import DESTINATION_PATH

class CoverLetterGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cover Letter Generator")
        self.root.geometry("600x500")
        
        self.url_entries = []
        self.destination_path = DESTINATION_PATH
        
        # Main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame, 
            text="AI Cover Letter Generator",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Instructions
        instructions = tk.Label(
            self.main_frame,
            text="Enter job posting URLs (one per field):",
            font=("Arial", 11)
        )
        instructions.pack(pady=(0, 10))
        
        # Scrollable frame for URL entries
        self.canvas = tk.Canvas(self.main_frame, height=200)
        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add initial URL field
        self.add_url_field()
        
        # Button frame
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        # Add URL button
        self.add_button = tk.Button(
            button_frame,
            text="+ Add URL",
            command=self.add_url_field,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        self.generate_button = tk.Button(
            button_frame,
            text="Generate Cover Letters",
            command=self.launch_generation,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Open folder button (initially hidden)
        self.folder_button = tk.Button(
            button_frame,
            text="Open Output Folder",
            command=self.open_destination_folder,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        # Don't pack yet - will show after generation
        
        # Progress bar
        self.progress_frame = tk.Frame(self.main_frame)
        self.progress_label = tk.Label(self.progress_frame, text="", font=("Arial", 10))
        self.progress_label.pack()
        self.progress = ttk.Progressbar(self.progress_frame, mode="indeterminate", length=400)
        self.progress.pack(pady=5)
        
        # Status text
        self.status_text = tk.Text(
            self.main_frame,
            height=8,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#f5f5f5"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Configure status text tags
        self.status_text.tag_config("success", foreground="green")
        self.status_text.tag_config("error", foreground="red")
        self.status_text.tag_config("info", foreground="blue")
    
    def add_url_field(self):
        """Add a new URL input field."""
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(fill=tk.X, pady=2)
        
        # URL entry
        entry = tk.Entry(frame, width=60, font=("Arial", 10))
        entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Remove button
        remove_btn = tk.Button(
            frame,
            text="×",
            command=lambda: self.remove_url_field(frame, entry),
            fg="red",
            font=("Arial", 12, "bold"),
            padx=5,
            pady=0
        )
        remove_btn.pack(side=tk.LEFT)
        
        self.url_entries.append(entry)
        
        # Focus on the new entry
        entry.focus()
    
    def remove_url_field(self, frame, entry):
        """Remove a URL input field."""
        if len(self.url_entries) > 1:  # Keep at least one field
            self.url_entries.remove(entry)
            frame.destroy()
    
    def launch_generation(self):
        """Start the cover letter generation process."""
        urls = [entry.get().strip() for entry in self.url_entries if entry.get().strip()]
        
        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one job posting URL.")
            return
        
        # Clear status text
        self.status_text.delete(1.0, tk.END)
        self.add_status("Starting generation process...\n", "info")
        
        # Show progress
        self.progress_frame.pack(pady=10)
        self.progress_label.config(text="Generating cover letters...")
        self.progress.start()
        
        # Disable buttons during generation
        self.generate_button.config(state=tk.DISABLED)
        self.add_button.config(state=tk.DISABLED)
        
        # Start generation in separate thread
        thread = threading.Thread(target=self._generate_letters, args=(urls,))
        thread.daemon = True
        thread.start()
    
    def _generate_letters(self, urls):
        """Generate cover letters in background thread."""
        try:
            self.add_status(f"Processing {len(urls)} job posting(s)...\n", "info")
            
            generator = Generator(urls)
            results = generator.run()
            
            # Show results
            self.root.after(0, self._show_results, results)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}\n"
            self.root.after(0, lambda: self.add_status(error_msg, "error"))
            self.root.after(0, self._generation_complete, False)
    
    def _show_results(self, results):
        """Display generation results."""
        if results:
            self.add_status(f"\nSuccessfully generated {len(results)} cover letter(s):\n", "success")
            for i, letter in enumerate(results, 1):
                self.add_status(f"  {i}. {letter.title}\n", "info")
            
            self.add_status(f"\nFiles saved to: {self.destination_path}\n", "info")
            
            # Show open folder button
            self.folder_button.pack(side=tk.LEFT, padx=5)
            
            messagebox.showinfo(
                "Success",
                f"Generated {len(results)} cover letter(s) successfully!\n\n"
                f"Files saved to:\n{self.destination_path}"
            )
        else:
            self.add_status("No cover letters were generated.\n", "error")
            messagebox.showwarning("No Results", "No cover letters were generated.")
        
        self._generation_complete(bool(results))
    
    def _generation_complete(self, _):
        """Clean up after generation completes."""
        self.progress.stop()
        self.progress_frame.pack_forget()
        self.generate_button.config(state=tk.NORMAL)
        self.add_button.config(state=tk.NORMAL)
    
    def add_status(self, message, tag=None):
        """Add a status message to the text widget."""
        self.status_text.insert(tk.END, message, tag)
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def open_destination_folder(self):
        """Open the destination folder in the system file explorer."""
        path = Path(self.destination_path)
        if not path.exists():
            messagebox.showerror("Error", f"Folder not found: {path}")
            return
        
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(path)])
            elif system == "Windows":
                subprocess.run(["explorer", str(path)])
            else:  # Linux and others
                subprocess.run(["xdg-open", str(path)])
            
            self.add_status(f"Opened folder: {path}\n", "info")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoverLetterGeneratorUI(root)
    root.mainloop()