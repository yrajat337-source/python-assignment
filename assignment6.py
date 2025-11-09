import tkinter as tk
from tkinter import messagebox

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(str(screen.get()))
            screen.set(result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            screen.set("")
    elif text == "C":
        screen.set("")
    else:
        screen.set(screen.get() + text)

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")
root.resizable(False, False)

screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font="lucida 20 bold", bd=10, relief=tk.SUNKEN)
entry.pack(fill=tk.X, ipadx=8, pady=10, padx=10)

# Button layout
button_texts = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "C", "=", "+"]
]

for row in button_texts:
    frame = tk.Frame(root)
    frame.pack()
    for text in row:
        button = tk.Button(frame, text=text, font="lucida 15 bold", width=5, height=2, relief=tk.RAISED)
        button.pack(side=tk.LEFT, padx=5, pady=5)
        button.bind("<Button-1>", click)

root.mainloop()
