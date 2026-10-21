# Vision_Digest
I had an problem of not being able to copy real life codes or mumbled text of printouts and real life images. This project helps combar that problem.
Vision Digest is a high-performance desktop application that bridges computer vision and natural language processing to extract, clean, and analyze text from static document images and live video streams. Built with Python and Tkinter, it provides a seamless user experience through a responsive, multi-threaded interface designed to handle real-world OCR workflows reliably.

-----------
<img width="1920" height="1040" alt="git_project" src="https://github.com/user-attachments/assets/72f1c6c4-ae98-49ce-a5d2-73e00a01f8f6" />


## Key Features
- **Smooth, Non-Freezing Interface**: Heavy operation including camera device discovery, file parsing, and OCR execution, run on dedicated background threads, ensuring the Tkinter interface remains fully responsive without freezing.
- **Flexible Dual-Engine OCR**: Modular pipeline supporting both Tesseract for precision static document/screenshot analysis and EasyOCR for capturing text dynamically from live camera feeds / real life images.
- **Smart Spell-Checking with Protection**: Integrates an in-memory SymSpellPy module with intelligent filters that correct standard typing errors while explicitly protecting uppercase acronyms (PG, UG), numbers, and single charater which may be interpreted as noise.
- **Automatic Display Scaling**: Automatically monitors high-resolution feeds (such as 1080p or Camo virtual streams), applying area-based downscaling (INTER_AREA) to fit the UI layout cleanly while preserving full-resolution frames for maximum OCR accuracy.
- **Seamless Camera Switching**: Features an asynchronous device-scanning loop, allowing users to hot-swap between multiple physical webcams or mobile camera streams seamlessly from a drop down menu.

## Tech Stack
| Category | Tech/Library| Purpose|
| -------- | ----------- | ------- |
| Language | Python (3.14.2) | Core application logic |
| GUI | Tkinter | Desktop GUI for easy access to hardware |
| Computer Vision | OpenCV (cv2) - PIL | Live video feed handling, image manipulation and transformation |
| NLP/Text Processing | SymSpell (1.14) | In-memory guard-railing and spell corrections for inherent misreads by OCR's |
| Concurrency | Python Threading | Basic threading for multiple tasks to ensure smooth and seamless functioning|

## Installation and Setup
### Clone the repository
```bash
git clone https://github.com/SrujanBali/Vision_Digest
cv Vision_Digest
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
**Note** - To use TesseractOCR, install it on your device through here :- https://github.com/UB-Mannheim/tesseract/wiki . After Installation add it to your environment variables.

### Run the application
```bash
python main.py
```

### Building an Executable (.exe)
```bash
pip install pyinstaller
```
```bash
pyinstaller --noconsole --onefile main.py
```
## Project Images
<img width="1920" height="1040" alt="cropped_screenshot0" src="https://github.com/user-attachments/assets/7c445cd2-3dd1-4b7c-be86-da0d5665876a" />
<img width="1920" height="1040" alt="cropped_screenshot1" src="https://github.com/user-attachments/assets/df750344-8979-4fd8-ac15-8f277d0a8948" />
<img width="1920" height="1040" alt="cropped_screenshot2" src="https://github.com/user-attachments/assets/906b3075-b88e-429d-a088-07640a31a552" />
<img width="1920" height="1040" alt="cropped_screenshot3" src="https://github.com/user-attachments/assets/ca096287-1065-4203-b7e7-4c797d0afb21" />
<img width="1920" height="1040" alt="cropped_screenshot4" src="https://github.com/user-attachments/assets/2a64549e-2c8e-41d1-a193-7177510bfe63" />
<img width="1920" height="1040" alt="cropped_screenshot5" src="https://github.com/user-attachments/assets/3367d388-c295-440c-a6a1-08c99cb7c95c" />

## Project Structure
```
Vision_Digest/
├── .gitignore
├── README.md
├── notebooks/
│   └── Feature_Testing.ipynb
├── requirements.txt
└── src/
    ├── cv_pipeline/
    │   ├── easyOCR_extraction.py
    │   ├── image_capture.py
    │   └── tesseract_extraction.py
    ├── main.py
    └── npl_pipeline/
        ├── frequency_dictionary_en_82_765.txt
        └── spellcheck.py
```

