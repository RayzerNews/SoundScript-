import tkinter as tk
from tkinter import filedialog, messagebox
import winsound
import time
import re

# Define the initial PL code
pl_code = """
SoundSystem() = {
    channels = [5.1]
    subwoofer1 = [Static]
    pass
    subwoofer2 = [Static]
    pass
    left_speaker = [Static]
    pass
    right_speaker = [Static]
    pass
    back_speaker = [Static]
    pass
    front_speaker = [Static]
}
SoundSystem(end)
"""

# Function to interpret the PL code, play a sound, and flash the corresponding speaker
def play_sound_test(pl_code):
    lines = pl_code.strip().splitlines()
    for line in lines:
        line = line.strip().lower()
        if "subwoofer1" in line:
            flash_speaker("subwoofer1")
            winsound.Beep(37, 500)
        elif "subwoofer2" in line:
            flash_speaker("subwoofer2")
            winsound.Beep(37, 500)
        elif "left_speaker" in line:
            flash_speaker("left_speaker")
            winsound.Beep(500, 500)
        elif "right_speaker" in line:
            flash_speaker("right_speaker")
            winsound.Beep(600, 500)
        elif "back_speaker" in line:
            flash_speaker("back_speaker")
            winsound.Beep(400, 500)
        elif "front_speaker" in line:
            flash_speaker("front_speaker")
            winsound.Beep(700, 500)

# Flash a speaker by turning it red, then back to original color
def flash_speaker(speaker):
    speaker_map = {
        "subwoofer1": subwoofer1,
        "subwoofer2": subwoofer2,
        "left_speaker": left_speaker,
        "right_speaker": right_speaker,
        "back_speaker": back_speaker,
        "front_speaker": front_speaker
    }
    canvas.itemconfig(speaker_map[speaker], fill="red")
    root.update()  # Update to show color change
    time.sleep(0.5)  # Flash duration
    canvas.itemconfig(speaker_map[speaker], fill="grey")  # Revert to original color
    root.update()

# Function to apply syntax highlighting
def apply_syntax_highlighting():
    code = editor.get("1.0", tk.END)
    
    # Define the syntax patterns (keywords, speakers, etc.)
    keywords = r"(SoundSystem|end|Static|pass|channels)"
    speakers = r"(subwoofer1|subwoofer2|left_speaker|right_speaker|back_speaker|front_speaker)"
    function_calls = r"(\(\))"
    
    # Clear existing tags
    editor.tag_delete("keyword")
    editor.tag_delete("speaker")
    editor.tag_delete("function")

    # Apply tags for keywords
    for match in re.finditer(keywords, code):
        editor.tag_add("keyword", f"1.{match.start()}", f"1.{match.end()}")
    
    # Apply tags for speakers
    for match in re.finditer(speakers, code):
        editor.tag_add("speaker", f"1.{match.start()}", f"1.{match.end()}")
    
    # Apply tags for function calls
    for match in re.finditer(function_calls, code):
        editor.tag_add("function", f"1.{match.start()}", f"1.{match.end()}")
    
    # Configure tag colors
    editor.tag_configure("keyword", foreground="blue", font=("Consolas", 12, "bold"))
    editor.tag_configure("speaker", foreground="green", font=("Consolas", 12))
    editor.tag_configure("function", foreground="purple", font=("Consolas", 12))

# GUI for the editor
def UI():
    global root, canvas, subwoofer1, subwoofer2, left_speaker, right_speaker, back_speaker, front_speaker
    root = tk.Tk()
    root.title("SoundScript Editor")

    # Text editor for code input
    global editor
    editor = tk.Text(root, wrap="word", font=("Consolas", 12), undo=True)
    editor.insert("1.0", pl_code)  # Insert example code into the editor
    editor.pack(expand=1, fill="both")
    
    # Apply syntax highlighting to the initial code
    apply_syntax_highlighting()

    # Speaker layout canvas
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()

    # Draw each speaker as a rectangle
    subwoofer1 = canvas.create_rectangle(70, 250, 110, 290, fill="grey", tags="subwoofer1")
    subwoofer2 = canvas.create_rectangle(190, 250, 230, 290, fill="grey", tags="subwoofer2")
    left_speaker = canvas.create_rectangle(20, 150, 60, 190, fill="grey", tags="left_speaker")
    right_speaker = canvas.create_rectangle(240, 150, 280, 190, fill="grey", tags="right_speaker")
    back_speaker = canvas.create_rectangle(130, 20, 170, 60, fill="grey", tags="back_speaker")
    front_speaker = canvas.create_rectangle(130, 150, 170, 190, fill="grey", tags="front_speaker")

    # Menu functions
    def run_code():
        code = editor.get("1.0", tk.END)
        play_sound_test(code)
        messagebox.showinfo("Run Code", "Sound test executed.")

    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(editor.get("1.0", tk.END))
            messagebox.showinfo("File Saved", "Your file has been saved.")

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            editor.delete("1.0", tk.END)  # Clear the editor
            editor.insert("1.0", content)  # Load file content into the editor
            messagebox.showinfo("File Opened", "Your file has been loaded.")
            apply_syntax_highlighting()  # Reapply syntax highlighting when a file is opened

    # Menu bar for file operations
    menu_bar = tk.Menu(root)
    
    # File menu with Open and Save options
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    menu_bar.add_cascade(label="File", menu=file_menu)
    
    # Run menu
    run_menu = tk.Menu(menu_bar, tearoff=0)
    run_menu.add_command(label="Run Sound Test", command=run_code)
    menu_bar.add_cascade(label="Run", menu=run_menu)
    
    root.config(menu=menu_bar)
    root.mainloop()

UI()
