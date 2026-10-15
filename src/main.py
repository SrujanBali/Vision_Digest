import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 as cv
from cv_pipeline.tesseract_extraction import tesseract_text_extraction
from cv_pipeline.easyOCR_extraction import easyocr_text_extraction


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

        self.cap = None
        self.is_camera_running = False

        self.raw_extracted_text = tk.StringVar()

        self.setup_screenshot_tab()
        self.setup_camera_tab()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_screenshot_tab(self):
        tab = ttk.Frame(self.notebook,style="TabBG.TFrame")
        self.notebook.add(tab, text="Screenshot / File OCR (Tesseract)")

        btn_frame = ttk.Frame(tab, style="TabBG.TFrame")
        btn_frame.pack(pady=10, fill="x", padx=20)

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        label = tk.Label(tab, text="Upload a clean screenshot or document image", font=("Ariel", 24, "bold"), bg="#27374D", fg="white")
        label.pack(pady=20)

        btn_upload = tk.Button(tab, text="Select Image File", command=self.upload_file, width=24, height=3, bg="#4CAF50", fg="white")
        btn_upload.pack(pady=10)

        self.path_label = tk.Label(tab, text="No folder selected", font=("Ariel", 14), bg="#27374D", fg="white")
        self.path_label.pack(pady=10)

        self.screenshot_output = tk.Text(tab, wrap=tk.WORD)
        self.screenshot_output.pack(pady=15, padx=20, expand=True, fill="both")

        btn_copy = tk.Button(tab, text="Copy to Clipboard", bg="blue", font=("Ariel", 15, "bold"), width=24, height=3, command= lambda: self.copy_to_clipboard())
        btn_copy.pack(padx=20, pady=10, fill="x")

    def setup_camera_tab(self):
        tab = ttk.Frame(self.notebook, style="TabBG.TFrame")
        self.notebook.add(tab, text="Live Camera Feed (EasyOCR)")

        label = tk.Label(tab, text="Open Live camera  stream to capture real world text", font=("Ariel", 16, "bold"))
        label.pack(pady=20)

        self.btn_cam = tk.Button(tab, text="Lauch Camera Stream", command=self.toggle_camera, width=24, height=3, bg="#2196F3", fg="white")
        self.btn_cam.pack(pady=10)

        btn_frame = ttk.Frame(tab, style="TabBG.TFrame")
        btn_frame.pack(pady=10, fill="x", padx=30)

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.btn_capture = tk.Button(btn_frame, text="Capture and Run EasyOCR", font=("Ariel", 16, "bold"),  command=self.capture_and_extract, width=22, height=2, bg="#4CAF50", fg="white", state=tk.DISABLED)
        self.btn_capture.pack(pady=5)

        self.video_label = tk.Label(tab, bg="#27374D")
        self.video_label.pack(pady=10)

        self.camera_output = tk.Text(tab, wrap=tk.WORD, width=70, height=10)
        self.camera_output.pack(pady=5, fill="x", padx=20)

        btn_copy = tk.Button(tab, text="Copy to Clipboard", bg="blue", font=("Ariel", 15, "bold"), width=24, height=2, command= lambda: self.copy_to_clipboard())
        btn_copy.pack(pady=8)
        
    def upload_file(self):
        filepath = filedialog.askopenfilename(title="Select image", filetypes=[("Image Files", "*png; *jpg; *jpeg")])
        if filepath:
                self.screenshot_output.delete("1.0", tk.END)
                self.path_label.config(text=f"{filepath}")
                extracted_text = tesseract_text_extraction(filepath)
                self.screenshot_output.insert(tk.END, extracted_text)
                self.raw_extracted_text.set("")
                self.raw_extracted_text.set(extracted_text)

    def toggle_camera(self):
        if not self.is_camera_running:
             self.cap = cv.VideoCapture(1, cv.CAP_DSHOW)
             self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
             self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

             if self.cap.isOpened():
                  self.is_camera_running = True
                  self.btn_cam.config(text="Stop Camera Stream", bg="#f44336")
                  self.btn_capture.config(state=tk.NORMAL)
                  self.update_video_stream()

        else:
            self.stop_camera()

    def update_video_stream(self):
         if self.is_camera_running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame

                cv_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv_image)
                self.photo = ImageTk.PhotoImage(image=pil_image)
                self.video_label.config(image=self.photo)

            self.root.after(15, self.update_video_stream)

    def capture_and_extract(self):
        if self.current_frame is not None:
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\capturedImage.png"
            cv.imwrite(filename, self.current_frame)

            self.camera_output.delete("1.0", tk.END)
            self.camera_output.insert(tk.END, "Captures Image! Running EasyOCR on the image. Please Wait...")

            text_extracted = easyocr_text_extraction(self.current_frame)
            self.camera_output.delete("1.0", tk.END)
            self.camera_output.insert(tk.END, text_extracted)
            self.raw_extracted_text.set("")
            self.raw_extracted_text.set(text_extracted)

    def copy_to_clipboard(self):
        text_to_copy = self.raw_extracted_text.get()
        if text_to_copy.strip():
            subprocess.run(["clip.exe"], input=text_to_copy.strip().encode('utf-8'), check=True)

    def stop_camera(self):
        self.is_camera_running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image="")
        self.btn_cam.config(text="Launch Camera Stream", bg="#2196F3")
        self.btn_capture.config(state=tk.DISABLED)

    def on_closing(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = Vision_Digest_GUI(root)
    root.mainloop()