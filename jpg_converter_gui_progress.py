import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import threading

class JPGConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("แปลง JPG เป็น PNG หรือ GIF")
        self.root.geometry("500x360")
        self.root.resizable(False, False)

        self.jpg_files = []
        self.output_format = tk.StringVar(value="PNG")
        self.output_folder = ""

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.root, text="เลือกไฟล์ JPG:").pack(pady=5)
        ttk.Button(self.root, text="เพิ่มไฟล์", command=self.select_files).pack()

        self.file_listbox = tk.Listbox(self.root, width=60, height=5)
        self.file_listbox.pack(pady=5)

        ttk.Label(self.root, text="เลือกรูปแบบที่จะบันทึก:").pack(pady=5)
        ttk.Radiobutton(self.root, text="PNG", variable=self.output_format, value="PNG").pack()
        ttk.Radiobutton(self.root, text="GIF", variable=self.output_format, value="GIF").pack()

        ttk.Button(self.root, text="เลือกโฟลเดอร์บันทึก", command=self.select_output_folder).pack(pady=5)
        ttk.Button(self.root, text="แปลงไฟล์", command=self.start_conversion).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack()

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("JPG files", "*.jpg;*.jpeg")])
        if files:
            self.jpg_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for f in self.jpg_files:
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            messagebox.showinfo("โฟลเดอร์ที่เลือก", f"จะบันทึกที่: {self.output_folder}")

    def start_conversion(self):
        thread = threading.Thread(target=self.convert_images)
        thread.start()

    def convert_images(self):
        if not self.jpg_files:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์ JPG")
            return

        if not self.output_folder:
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกโฟลเดอร์บันทึก")
            return

        self.progress["maximum"] = len(self.jpg_files)
        self.progress["value"] = 0
        self.status_label.config(text="กำลังแปลงไฟล์...")

        format_ext = self.output_format.get().lower()

        for i, file in enumerate(self.jpg_files, 1):
            try:
                img = Image.open(file).convert("RGB")
                filename = os.path.splitext(os.path.basename(file))[0]
                output_path = os.path.join(self.output_folder, f"{filename}.{format_ext}")
                img.save(output_path, self.output_format.get())
                self.progress["value"] = i
            except Exception as e:
                messagebox.showerror("เกิดข้อผิดพลาด", str(e))
                return

        self.status_label.config(text="✅ เสร็จสิ้น OK")
        messagebox.showinfo("สำเร็จ", f"แปลงไฟล์เป็น {self.output_format.get()} เรียบร้อยแล้ว!")

if __name__ == "__main__":
    root = tk.Tk()
    app = JPGConverterApp(root)
    root.mainloop()
