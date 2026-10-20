import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 as cv
import threading
from cv_pipeline.tesseract_extraction import tesseract_text_extraction
from cv_pipeline.easyOCR_extraction import easyocr_text_extraction
from npl_pipeline.spellcheck import spelling_autocorrector


class Vision_Digest_GUI : 
    def __init__ (self, root):
        self.root = root
        self.root.title("Vision Digest")
        self.root.geometry("1600x900")

        self.camera_device = 0

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

        btn_upload = tk.Button(tab, text="Select Image File", command=self.upload_file_thread, width=24, height=3, bg="#4CAF50", fg="white")
        btn_upload.pack(pady=10)

        self.path_label = tk.Label(tab, text="No folder selected", font=("Ariel", 14), bg="#27374D", fg="white")
        self.path_label.pack(pady=10)

        self.screenshot_output = tk.Text(tab, wrap=tk.WORD, width=70, height=10)
        self.screenshot_output.pack(pady=5, fill="x", padx=20)

        btn_copy = tk.Button(tab, text="Copy to Clipboard", bg="green", font=("Ariel", 15, "bold"), width=24, height=2, command= lambda: self.copy_to_clipboard())
        btn_copy.pack(pady=8)

    def setup_camera_tab(self):
        tab = ttk.Frame(self.notebook, style="TabBG.TFrame")
        self.notebook.add(tab, text="Live Camera Feed (EasyOCR)")

        label = tk.Label(tab, text="Open Live camera  stream to capture real world text", font=("Ariel", 24, "bold"), bg="#27374D", fg="white")
        label.pack(pady=20)

        selection_frame = ttk.Frame(tab, style="TabBG.TFrame")
        selection_frame.pack(pady=5)

        tk.Label(selection_frame, text="Select Camera:", font=("Ariel", 12), bg="#27374D", fg="white").pack(side=tk.LEFT, padx=5)

        self.camera_combobox = ttk.Combobox(selection_frame, state="readonly", width=20)
        self.camera_combobox.pack(side=tk.LEFT, padx=5)
        self.camera_combobox.bind("<<ComboboxSelected>>", self.on_camera_select)

        btn_refresh = tk.Button(selection_frame, text="Scan Cameras", command=self.scan_cameras_thread, bg="#607D8B", fg="white")
        btn_refresh.pack(side=tk.LEFT, padx=5)

        self.btn_cam = tk.Button(tab, text="Lauch Camera Stream", command=self.toggle_camera, width=24, height=3, bg="#2196F3", fg="white")
        self.btn_cam.pack(pady=10)

        btn_frame = ttk.Frame(tab, style="TabBG.TFrame")
        btn_frame.pack(pady=10, fill="x", padx=30)

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.btn_capture = tk.Button(btn_frame, text="Capture and Run EasyOCR", font=("Ariel", 16, "bold"),  command=self.camera_thread, width=22, height=2, bg="gray", fg="black", state=tk.DISABLED)
        self.btn_capture.pack(pady=5)

        self.video_label = tk.Label(tab, bg="#27374D")
        self.video_label.pack(pady=10)

        self.camera_output = tk.Text(tab, wrap=tk.WORD, width=70, height=10)
        self.camera_output.pack(pady=5, fill="x", padx=20)

        btn_copy = tk.Button(tab, text="Copy to Clipboard", bg="green", font=("Ariel", 15, "bold"), width=24, height=2, command= lambda: self.copy_to_clipboard())
        btn_copy.pack(pady=8)

        self.scan_cameras_thread()

    def upload_file_thread(self):
        file_thread = threading.Thread(target=self.upload_file_and_extract)
        file_thread.start()
        
    def upload_file_and_extract(self):
        filepath = filedialog.askopenfilename(title="Select image", filetypes=[("Image Files", "*png; *jpg; *jpeg")])
        if filepath:
                self.screenshot_output.delete("1.0", tk.END)
                self.screenshot_output.insert(tk.END, "Got the file! Please wait while Tesseract extracts the text...")
                self.path_label.config(text=f"{filepath}")
                self.screenshot_output.delete("1.0", tk.END)
                extracted_text = tesseract_text_extraction(filepath)
                spell_corrected_text = spelling_autocorrector(extracted_text)
                self.screenshot_output.insert(tk.END, spell_corrected_text)
                self.raw_extracted_text.set("")
                self.raw_extracted_text.set(extracted_text)

    def scan_cameras_thread(self):
        threading.Thread(target=self.discover_cameras, daemon=True).start()

    def discover_cameras(self):
        available_devices = []

        for i in range(4):
            cap = cv.VideoCapture(i)
            if cap.isOpened():
                available_devices.append(f"Camera {i}")
                cap.release()
        if not available_devices:
            available_devices = ["No Cameras found!"]

        self.root.after(0, lambda: self.update_camera_dropdown(available_devices))

    def update_camera_dropdown(self, devices):
        self.camera_combobox["values"] = devices
        self.camera_combobox.current(0)
        self.update_selected_camera_index(devices[0])

    def on_camera_select(self, event):
        selected_text = self.camera_combobox.get()
        self.update_selected_camera_index(selected_text)

        if self.is_camera_running:
            self.stop_camera()
            self.toggle_camera()

    def update_selected_camera_index(self, selecteion_str):
        if "Camera" in selecteion_str:
            try:
                self.camera_device = int(selecteion_str.split(" ")[1])
            except ValueError:
                self.camera_device =  0

    def toggle_camera(self):
        if not self.is_camera_running:
             self.cap = cv.VideoCapture(self.camera_device)
             cam_width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
             cam_height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
             self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)
             self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)

             if self.cap.isOpened():
                  self.is_camera_running = True
                  self.btn_capture.config(bg="lightgreen")
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

                height, width = frame.shape[:2]
                if width > 1280 or height > 720:
                    new_width = width // 2
                    new_height = height // 2
                    display_frame =  cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_AREA)
                else:
                    display_frame = frame

                cv_image = cv.cvtColor(display_frame, cv.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv_image)
                self.photo = ImageTk.PhotoImage(image=pil_image)
                self.video_label.config(image=self.photo)

            self.root.after(15, self.update_video_stream)

    def camera_thread(self):
        cam_thread = threading.Thread(target=self.capture_and_extract)
        cam_thread.start()

    def capture_and_extract(self):
        if self.current_frame is not None:
            filename = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\processed\capturedImage.png"
            cv.imwrite(filename, self.current_frame)
            self.stop_camera()

            self.camera_output.delete("1.0", tk.END)
            self.camera_output.insert(tk.END, "Captures Image! Running EasyOCR on the image. Please Wait...")

            text_extracted = easyocr_text_extraction(self.current_frame)
            self.camera_output.delete("1.0", tk.END)
            spell_corrected_text = spelling_autocorrector(text_extracted)
            self.camera_output.insert(tk.END, spell_corrected_text)
            self.raw_extracted_text.set("")
            self.raw_extracted_text.set(text_extracted)

    def copy_to_clipboard(self):
        text_to_copy = self.raw_extracted_text.get()
        if text_to_copy.strip():
            subprocess.run(["clip.exe"], input=text_to_copy.strip().encode('utf-8'), check=True)

    def stop_camera(self):
        self.is_camera_running = False
        self.btn_capture.config(bg="gray")
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