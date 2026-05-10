import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import PyPDF2

engine = pyttsx3.init()

# ----------------- FUNCTIONS -----------------

def speak_text():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text.")
        return
    set_voice()
    engine.say(text)
    engine.runAndWait()

def save_audio():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No text to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav")]
    )

    if file_path:
        set_voice()
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        messagebox.showinfo("Success", "Audio file saved successfully.")

def load_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    text_area.delete("1.0", tk.END)

    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text_area.insert(tk.END, page.extract_text())

def set_voice():
    voices = engine.getProperty("voices")
    engine.setProperty("rate", speed_scale.get())

    if voice_var.get() == "Male":
        engine.setProperty("voice", voices[0].id)
    else:
        engine.setProperty("voice", voices[1].id)

# ----------------- GUI -----------------

root = tk.Tk()
root.title("Offline Text-to-Speech & Audiobook Creator")
root.geometry("700x500")

tk.Label(root, text="Enter Text or Load PDF", font=("Arial", 14)).pack(pady=5)

text_area = tk.Text(root, height=15, wrap=tk.WORD)
text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

controls = tk.Frame(root)
controls.pack(pady=5)

tk.Button(controls, text="Load PDF", command=load_pdf).grid(row=0, column=0, padx=5)
tk.Button(controls, text="Speak", command=speak_text).grid(row=0, column=1, padx=5)
tk.Button(controls, text="Save Audio", command=save_audio).grid(row=0, column=2, padx=5)

voice_var = tk.StringVar(value="Male")
tk.Label(root, text="Voice").pack()
tk.OptionMenu(root, voice_var, "Male", "Female").pack()

tk.Label(root, text="Speech Speed").pack()
speed_scale = tk.Scale(root, from_=100, to=200, orient=tk.HORIZONTAL)
speed_scale.set(150)
speed_scale.pack()

root.mainloop()