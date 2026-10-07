import tkinter as tk
from tkinter import ttk, filedialog

class Vision_Digest_GUI : 
    def __init__ (self, root):
        self.root = root
        self.root.title("Vision Digest")
        self.root.geometry("1280x700")

        style = ttk.Style()
        style.theme_use("default")

        style.configure("TNotebook", background="#lightgray")
        style.configure("TNotebook.Tab", background="lightblue", padding=[10, 5])
        style.configure("TabBG.TFrame", background="#27374D")

        style.map("TNotebook.Tab", background=[("selected", "#27374D")], foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.setup_screenshot_tab()
        self.setup_camera_tab()

    def setup_screenshot_tab(self):
        tab = ttk.Frame(self.notebook,style="TabBG.TFrame")
        self.notebook.add(tab, text="Screenshot / File OCR (Tesseract)")

        label = tk.Label(tab, text="Upload a clean screenshot or document image", font=("Ariel", 16))
        label.pack(pady=20)

        btn_upload = tk.Button(tab, text="Select Image File", command=self.upload_file, width=24, height=3, bg="#4CAF50", fg="white")
        btn_upload.pack(pady=10)

        self.screeshot_output = tk.Text(tab, wrap=tk.WORD, width=70, height=15)
        self.screeshot_output.pack(pady=10)

    def setup_camera_tab(self):
        tab = ttk.Frame(self.notebook, style="TabBG.TFrame")
        self.notebook.add(tab, text="Live Camera Feed (EasyOCR)")

        label = tk.Label(tab, text="Open Live camera  stream to capture real world text", font=("Ariel", 16))
        label.pack(pady=20)

        btn_cam = tk.Button(tab, text="Lauch Camera Stream", command=self.launch_camera, width=24, height=3, bg="#2196F3", fg="white")
        btn_cam.pack(pady=10)

        self.camera_output = tk.Text(tab, wrap=tk.WORD, width=70, height=15)
        self.camera_output.pack(pady=10)

    def upload_file(self):
        pass

    def launch_camera(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = Vision_Digest_GUI(root)
    root.mainloop()