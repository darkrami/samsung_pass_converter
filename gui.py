import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import sys
import darkdetect
import sv_ttk

from convert import run_conversion

class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set theme before creating widgets
        if darkdetect.isDark():
            sv_ttk.set_theme("dark")
        else:
            sv_ttk.set_theme("light")

        self.title("Samsung Pass Converter")
        self.geometry("600x280") # Adjusted height for the new label

        self.create_widgets()

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

        # Status Label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status_var, font=("Segoe UI", 10))
        self.status_label.pack(pady=5)

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
        # Clear previous status
        self.status_var.set("")

        file_path = self.file_path_var.get()
        password = self.password_var.get()
        output_dir = self.output_dir_var.get()
        output_filename = self.output_filename_var.get()

        if not file_path or not os.path.exists(file_path):
            self.show_status_message("Error: Please select a valid input file.", is_error=True)
            return
        if not password:
            self.show_status_message("Error: Please enter the password.", is_error=True)
            return
        if not output_dir or not os.path.isdir(output_dir):
            self.show_status_message("Error: Please select a valid output directory.", is_error=True)
            return

        self.convert_button.config(state="disabled")

        self.conversion_thread = threading.Thread(
            target=self.run_conversion_thread,
            args=(file_path, password, output_dir, output_filename),
            daemon=True
        )
        self.conversion_thread.start()

    def run_conversion_thread(self, file_path, password, output_dir, output_filename):
        try:
            # We don't need the output from run_conversion anymore, just whether it succeeded.
            # The print statements from convert.py will still go to the console.
            run_conversion(file_path, password, output_dir, output_filename)
            self.after(0, self.on_conversion_complete, True)
        except Exception:
            self.after(0, self.on_conversion_complete, False)

    def on_conversion_complete(self, success):
        self.convert_button.config(state="normal")
        if success:
            self.show_status_message("Success!")
        else:
            self.show_status_message("Something went wrong :(", is_error=True)

    def show_status_message(self, message, is_error=False):
        self.status_var.set(message)
        if is_error:
            self.status_label.config(foreground="red")
        else:
            # Use the default text color of the theme
            self.status_label.config(foreground="")

        # Clear the message after 5 seconds
        self.after(5000, lambda: self.status_var.set(""))


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
