import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import threading
import queue
import sys
import darkdetect
import sv_ttk

from convert import run_conversion

# A custom stream object to redirect stdout
class QueueIO(queue.Queue):
    def write(self, msg):
        self.put(msg)
    def flush(self):
        # This is needed for stdout redirection
        pass

class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set theme before creating widgets
        if darkdetect.isDark():
            sv_ttk.set_theme("dark")
        else:
            sv_ttk.set_theme("light")

        self.title("Samsung Pass Converter")
        self.geometry("600x450")

        self.create_widgets()

        # Queue for logging from other threads
        self.log_queue = QueueIO()
        self.process_log_queue()

    def create_widgets(self):
        # Theme toggle button
        self.theme_button = ttk.Button(self, text="Toggle Theme", command=sv_ttk.toggle_theme)
        self.theme_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=5)

        # Frame for inputs
        input_frame = ttk.Frame(self, padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)

        # File selection
        ttk.Label(input_frame, text="Samsung Pass File (.spass):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(input_frame, textvariable=self.file_path_var)
        self.file_path_entry.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)
        self.browse_file_button = ttk.Button(input_frame, text="Browse...", command=self.browse_file)
        self.browse_file_button.grid(row=0, column=2, sticky=tk.W, pady=2)

        # Password
        ttk.Label(input_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(input_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=5)

        # Output directory
        ttk.Label(input_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = ttk.Entry(input_frame, textvariable=self.output_dir_var)
        self.output_dir_entry.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=5)
        self.browse_dir_button = ttk.Button(input_frame, text="Browse...", command=self.browse_dir)
        self.browse_dir_button.grid(row=2, column=2, sticky=tk.W, pady=2)

        # Custom output filename
        ttk.Label(input_frame, text="Output Filename (optional):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.output_filename_var = tk.StringVar()
        self.output_filename_entry = ttk.Entry(input_frame, textvariable=self.output_filename_var)
        self.output_filename_entry.grid(row=3, column=1, sticky=tk.EW, pady=2, padx=5)
        self.output_filename_entry.insert(0, "spass.csv")

        # Convert button
        self.convert_button = ttk.Button(self, text="Convert", command=self.start_conversion)
        self.convert_button.pack(pady=10)

        # Status/Log area
        log_frame = ttk.Frame(self, padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ttk.Label(log_frame, text="Log:").pack(anchor=tk.W)
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.configure(state='disabled')

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Samsung Pass File",
            filetypes=(("Samsung Pass files", "*.spass"), ("All files", "*.*"))
        )
        if filepath:
            self.file_path_var.set(filepath)
            if not self.output_dir_var.get():
                self.output_dir_var.set(os.path.dirname(filepath))

    def browse_dir(self):
        dirpath = filedialog.askdirectory(title="Select Output Directory")
        if dirpath:
            self.output_dir_var.set(dirpath)

    def start_conversion(self):
        file_path = self.file_path_var.get()
        password = self.password_var.get()
        output_dir = self.output_dir_var.get()
        output_filename = self.output_filename_var.get()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid input file.")
            return
        if not password:
            messagebox.showerror("Error", "Please enter the password.")
            return
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return

        self.convert_button.config(state="disabled")
        self.log_message("Starting conversion...\n")

        self.conversion_thread = threading.Thread(
            target=self.run_conversion_thread,
            args=(file_path, password, output_dir, output_filename),
            daemon=True
        )
        self.conversion_thread.start()

    def run_conversion_thread(self, file_path, password, output_dir, output_filename):
        original_stdout = sys.stdout
        sys.stdout = self.log_queue

        try:
            run_conversion(file_path, password, output_dir, output_filename)
            self.log_queue.put("\n--- Conversion successful! ---\n")
        except Exception as e:
            self.log_queue.put(f"\n--- An error occurred: {e} ---\n")
            import traceback
            self.log_queue.put(traceback.format_exc())
        finally:
            sys.stdout = original_stdout
            self.after(0, self.on_conversion_complete)

    def on_conversion_complete(self):
        self.convert_button.config(state="normal")
        messagebox.showinfo("Complete", "Conversion process finished.")

    def process_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_message(msg)
        except queue.Empty:
            pass
        self.after(100, self.process_log_queue)

    def log_message(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')


if __name__ == "__main__":
    try:
        from cryptography.hazmat.primitives import hashes
        import sv_ttk
        import darkdetect
    except ImportError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Dependency Error", "A required library is not found. Please install dependencies by running:\npip install cryptography sv-ttk darkdetect")
        sys.exit(1)

    app = ConverterApp()
    app.mainloop()
