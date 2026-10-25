import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader
import pyttsx3
import threading


def convert_pdf():
    pdf_path = filedialog.askopenfilename(
        title="Select PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not pdf_path:
        return

    try:
        reader = PdfReader(pdf_path)
        text = "\n\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()

        if not text:
            messagebox.showerror(
                "Error",
                "PDF se text nahi mila. Scanned PDF ke liye OCR chahiye."
            )
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Audiobook",
            defaultextension=".wav",
            initialfile="audiobook.wav",
            filetypes=[("WAV audio", "*.wav")]
        )
        if not output_path:
            return

        button.config(state="disabled")
        status.config(text="Audiobook ban rahi hai...")

        def create_audio():
            try:
                engine = pyttsx3.init()
                engine.save_to_file(text, output_path)
                engine.runAndWait()
                engine.stop()
                root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Completed", f"Audiobook save ho gayi:\n{output_path}"
                    )
                )
                root.after(0, lambda: status.config(text="Completed!"))
            except Exception as error:
                root.after(
                    0, lambda: messagebox.showerror("Audio Error", str(error))
                )
                root.after(0, lambda: status.config(text="Conversion failed."))
            finally:
                root.after(0, lambda: button.config(state="normal"))

        threading.Thread(target=create_audio, daemon=True).start()

    except Exception as error:
        messagebox.showerror("PDF Error", str(error))
        status.config(text="PDF read nahi ho saki.")


root = tk.Tk()
root.title("Day 91 - PDF to Audiobook")
root.geometry("450x250")
root.resizable(False, False)

tk.Label(
    root, text="PDF to Audiobook", font=("Arial", 20, "bold")
).pack(pady=(30, 10))

tk.Label(
    root, text="PDF select karein aur usay audio mein badlein."
).pack(pady=5)

button = tk.Button(
    root, text="Choose PDF and Convert", command=convert_pdf,
    font=("Arial", 12), padx=10, pady=8
)
button.pack(pady=15)

status = tk.Label(root, text="Ready")
status.pack()

root.mainloop()
