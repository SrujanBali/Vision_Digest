# Vision_Digest
I had an problem of not being able to copy real life codes or mumbled text of printouts and real life images. This project helps combar that problem.
Vision Digest is a high-performance desktop application that bridges computer vision and natural language processing to extract, clean, and analyze text from static document images and live video streams. Built with Python and Tkinter, it provides a seamless user experience through a responsive, multi-threaded interface designed to handle real-world OCR workflows reliably.

## Features
- **Smooth, Non-Freezing Interface**: Heavy operation including camera device discovery, file parsing, and OCR execution, run on dedicated background threads, ensuring the Tkinter interface remains fully responsive without freezing.
- **Flexible Dual-Engine OCR**: Modular pipeline supporting both Tesseract for precision static document/screenshot analysis and EasyOCR for capturing text dynamically from live camera feeds / real life images.
- **Smart Spell-Checking with Protection**: Integrates an in-memory SymSpellPy module with intelligent filters that correct standard typing errors while explicitly protecting uppercase acronyms (PG, UG), numbers, and single charater which may be interpreted as noise.
- **Automatic Display Scaling**: Automatically monitors high-resolution feeds (such as 1080p or Camo virtual streams), applying area-based downscaling (INTER_AREA) to fit the UI layout cleanly while preserving full-resolution frames for maximum OCR accuracy.
- **Seamless Camera Switching**: Features an asynchronous device-scanning loop, allowing users to hot-swap between multiple physical webcams or mobile camera streams seamlessly from a drop down menu.
