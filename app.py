import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from tkinter import ttk

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imagem para ICO")
        self.root.geometry("400x300")
        self.root.configure(background="pink")

        self.destination_folder = tk.StringVar()
        self.destination_folder.set(self.load_destination_folder())

        self.source_image = tk.StringVar()
        self.source_image.set("")

        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0)

        self.stats_var = tk.StringVar()
        self.stats_var.set("")

        source_frame = tk.Frame(root, bg="pink")
        source_frame.pack(pady=10)

        tk.Label(source_frame, text="Imagem de Entrada:", bg="pink", fg="black").grid(row=0, column=0)
        self.source_entry = tk.Entry(source_frame, textvariable=self.source_image, width=30, state='readonly')
        self.source_entry.grid(row=1, column=0)
        source_button = tk.Button(source_frame, text="Selecionar Imagem", command=self.select_image, bg="lightpink", fg="black")
        source_button.grid(row=2, column=0)

        destination_frame = tk.Frame(root, bg="pink")
        destination_frame.pack(pady=10)

        tk.Label(destination_frame, text="Pasta de Destino:", bg="pink", fg="black").grid(row=0, column=0)
        self.destination_entry = tk.Entry(destination_frame, textvariable=self.destination_folder, width=30, state='readonly')
        self.destination_entry.grid(row=1, column=0)
        destination_button = tk.Button(destination_frame, text="Selecionar Pasta de Destino", command=self.select_destination_folder, bg="lightpink", fg="black")
        destination_button.grid(row=2, column=0)

        convert_button = tk.Button(root, text="Converter", command=self.convert_image, bg="lightpink", fg="black")
        convert_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, length=300, mode='determinate')
        self.progress_bar.pack()

        self.stats_label = tk.Label(root, textvariable=self.stats_var, bg="pink")
        self.stats_label.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.webp;*.svg;*.raw;*.tiff;*.pdf;*.gif;*.psd;*.bmp")])
        if file_path:
            self.source_image.set(file_path)

    def select_destination_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.destination_folder.set(folder_path)
            self.save_destination_folder(folder_path)

    def convert_image(self):
        source_path = self.source_image.get()
        destination_path = self.destination_folder.get()

        if not source_path or not destination_path:
            messagebox.showerror("Erro", "Por favor, selecione uma imagem e uma pasta de destino.")
            return

        try:
            image = Image.open(source_path)
            filename = os.path.splitext(os.path.basename(source_path))[0]
            image.save(os.path.join(destination_path, f"{filename}.ico"), format="ICO", quality=100, optimize=True)
        except Exception as e:
            messagebox.showerror("Erro na Conversão", f"Ocorreu um erro durante a conversão: {e}")

        self.progress_var.set(100)
        self.stats_var.set("Conversão concluída: 100%")

    def load_destination_folder(self):
        try:
            with open("destination_folder.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ""

    def save_destination_folder(self, folder_path):
        with open("destination_folder.txt", "w") as file:
            file.write(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()