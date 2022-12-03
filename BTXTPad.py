from tkinter import *
from tkinter import messagebox, simpledialog, filedialog, scrolledtext
import os, datetime, calendar, math
class __init__():
    def file(i):
        global filename
        if i == "n":
            filename = "New BTXTPad Document.btxt"
            editor.delete(1.0, "end")
        elif i == "o":
            filename = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
            editor.delete(1.0, "end")
            editor.insert(INSERT, open(filename, 'r', encoding='utf8').read())
        else:
            filename = filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')])
            open(filename, 'w', encoding='utf8').write(editor.get(1.0, "end"))
        root.title(filename+" - BTXTPad")
    def cut():
        editor.clipboard_clear()
        editor.delete("sel.first", "sel.last")
        editor.clipboard_append(editor.get("sel.first", "sel.last"))
    def copy(self):
        self.clipboard_clear()
        try:
            self.clipboard_append(self.get("sel.first", "sel.last"))
        except:
            self.clipboard_append(self.get(1.0, "end"))  
    def keep():
        editor.delete, editor.delete (1.0, "sel.first"), editor.delete("sel.last", "end")
    def find():
        find, pos = simpledialog.askstring("BTXTPad", "Find"), 1.0
        while True:
            try:
                chars = editor.search(find, pos, stopindex=END)
                messagebox.showinfo("BTXTPad", "Line: " + chars.replace(".", "; Column: "))
                pos = "% s+% dc" % (chars, len(find))
            except:
                break
    def replace():
        try:
            text = editor.get(1.0, "end").replace(editor.get("sel.first", "sel.last"), simpledialog.askstring("BTXTPad", "Replace"))
        except:
            text = editor.get(1.0, "end").replace(simpledialog.askstring("BTXTPad", "Find"), simpledialog.askstring("BTXTPad", "Replace"))
            editor.delete(1.0, "end")
            editor.insert(INSERT, text)
    def length():
        try:
            messagebox.showinfo("Length (selection)", str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get("sel.first", "sel.last").split(" "))-1) + " spaces\n" + str(len(editor.get("sel.first", "sel.last").split("\n"))-1) + " lines")
        except:
            messagebox.showinfo("Length (document)", str(len(editor.get("1.0", "end").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get(1.0, "end").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get(1.0, "end").split(" "))-1) + " spaces\n" + str(len(editor.get(1.0, "end").split("\n"))-1) + " lines")
    def full_screen():
        global fs
        fs = 0 if fs == 1 else 1
        root.attributes("-fullscreen", fs)
    def note():
        root = Tk()
        root.geometry("254x254")
        root.title(str(datetime.datetime.now().date()))
        root.resizable(width="False", height="False")
        root.attributes("-toolwindow", 1)
        root.attributes("-topmost", 1)
        m = Menu(root)
        root.config(menu=m)
        mTheme = Menu(root, tearoff=0)
        m.add_cascade(label="•", menu=mTheme)
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#fc5", fg="#000"), background="#fc5", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#5cf", fg="#000"), background="#5cf", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#f86", fg="#000"), background="#f86", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: note.configure(bg="#abc", fg="#000"), background="#abc", foreground="#000")
        note = Text(root, bd=8, relief=FLAT, undo=True, background="#fc5", foreground="#000", font=("", 11))
        note.pack()
        m.add_command(label="<", command=lambda: note.edit_undo())
        m.add_command(label=">", command=lambda: note.edit_redo())
        m.add_command(label="Copy", command=lambda: __init__.copy(note))
        m.add_command(label="Del", command=lambda: note.delete(1.0, "end"))
        m.add_command(label="Export", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, "end")))
        m.add_command(label="Send", command=lambda: editor.insert("end", note.get(1.0, "end")))
        m.add_command(label="+", command=__init__.note)
        root.mainloop()
    def calc():
        root = Tk()
        root.title("Calculator")
        root.resizable(width=False, height=False)
        root.attributes("-toolwindow", 1)
        root.attributes("-topmost", 1)
        bar = Entry(root, bd=8, relief=FLAT, font=("", 12), bg="#abc", fg="#000", justify="center")
        bar.grid(row=0, column=0, sticky="nsew")
        f = Frame(root)
        f.grid(row=1, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=0, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=0, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=0, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=0, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="√", command=lambda: messagebox.showinfo("Calculator", "sqrt("+bar.get()+") = "+str(math.sqrt(eval(bar.get()))))).grid(row=0, column=4, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=1, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=1, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=1, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=1, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="x²", command=lambda: messagebox.showinfo("Calculator", "("+bar.get()+")² = "+str(eval(bar.get()) * eval(bar.get())))).grid(row=1, column=4, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=2, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=2, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=2, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=2, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="bin", command=lambda: messagebox.showinfo("Calculator", "bin("+bar.get()+") = "+bin(int(eval(bar.get()))))).grid(row=2, column=4, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="C", command=lambda: bar.delete(0, "end")).grid(row=3, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=3, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="=", command=lambda: messagebox.showinfo("Calculaor", bar.get()+" = "+str(eval(bar.get())))).grid(row=3, column=4, sticky="nsew")
        Button(f, relief=FLAT, width=5, text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=3, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=3, column=2, sticky="nsew")
        root.mainloop()
    def close():
        ch = messagebox.askyesno('BTXTPad','Do you want to quit BTXTPad?')
        if ch:
             root.destroy()
    def right_click(self):
        mEdit.tk_popup(self.x_root, self.y_root)
if __name__ == "__main__":
    root, fs, filename = Tk(), 0, "New BTXTPad Document.btxt"
    root.title('BTXTPad')
    try:
        root.iconbitmap("btxtpad.ico")
    finally:
        root.rowconfigure(0, minsize=0, weight=1)
        root.columnconfigure(0, minsize=0, weight=1)
        m, mFile, mEdit, mInsert, mView, mTheme = Menu(root, tearoff=0), Menu(root, tearoff=0), Menu(root, tearoff=0), Menu(root, tearoff=0), Menu(root, tearoff=0), Menu(root, tearoff=0)
        root.configure(menu=m)
        root.protocol('WM_DELETE_WINDOW', __init__.close)
        m.add_cascade(label="File", menu=mFile)
        mFile.add_command(label="New", command=lambda: __init__.file("n"), accelerator="Ctrl+N")
        mFile.add_command(label="Open", command=lambda: __init__.file("o"), accelerator="Ctrl+O")
        mFile.add_command(label="Save", command=lambda: open(filename, 'w', encoding='utf8').write(editor.get(1.0, "end")), accelerator="Ctrl+S")
        mFile.add_command(label="Save As", command=lambda: __init__.file("s"), accelerator="F12")
        mFile.add_command(label="Print", command=lambda: os.startfile(filename, "print"), accelerator="Ctrl+P")
        mFile.add_command(label="Delete", command=lambda: os.remove(filename), accelerator="Ctrl+Q")
        mFile.add_separator()
        mFile.add_command(label="Read", command=lambda: editor.configure(state="disabled"), accelerator="Ctrl+U")
        mFile.add_command(label="Edit", command=lambda: editor.configure(state="normal"), accelerator="Ctrl+E")
        mFile.add_separator()
        mFile.add_command(label="About", command=lambda: messagebox.showinfo("About BTXTPad", "BTXTPad: A text editor\nCopyright (C) 2021-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nMIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."), accelerator="F1")
        mFile.add_command(label="Exit", command=__init__.close, accelerator="Alt+F4")
        m.add_cascade(label="Edit", menu=mEdit)
        mEdit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
        mEdit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
        mEdit.add_separator()
        mEdit.add_command(label="Cut", command=__init__.cut, accelerator="Ctrl+X")
        mEdit.add_command(label="Copy", command=lambda: __init__.copy(editor), accelerator="Ctrl+C")
        mEdit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')), accelerator="Ctrl+V")
        mEdit.add_separator()
        mEdit.add_command(label="Delete", command=lambda: editor.delete("sel.first", "sel.last"), accelerator="Del")
        mEdit.add_command(label="Delete All", command=lambda: editor.delete(1.0,"end"), accelerator="Shift+Del")
        mEdit.add_command(label="Keep", command=__init__.keep, accelerator="Ctrl+K")
        mEdit.add_separator()
        mEdit.add_command(label="Find", command=__init__.find, accelerator="Ctrl+F")
        mEdit.add_command(label="Replace", command=__init__.replace, accelerator="Ctrl+R")
        mEdit.add_separator()
        mEdit.add_command(label="Length", command=__init__.length, accelerator="Ctrl+L")
        mEdit.add_command(label="Font", command=lambda: editor.configure(font=(simpledialog.askstring("BTXTPad", "Font Name"), simpledialog.askinteger("BTXTPad", "Font Size"), simpledialog.askstring("BTXTPad", "Font Weight\n(normal/bold/italic/underline/etc.)"))), accelerator="Ctrl+T")
        m.add_cascade(label="Insert", menu=mInsert)
        mInsert.add_command(label="Calendar", command=lambda: editor.insert(INSERT, str(calendar.calendar(int(datetime.datetime.now().year)))))
        mInsert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
        mInsert.add_command(label="Finance", command=lambda: editor.insert(INSERT, "\t\tIncome\t\tCost\t\tSavings\nJanuary\t\t\t\t\t\t\nFebruary\t\t\t\t\t\t\nMarch\t\t\t\t\t\t\nApril\t\t\t\t\t\t\nMay\t\t\t\t\t\t\nJune\t\t\t\t\t\t\nJuly\t\t\t\t\t\t\nAugust\t\t\t\t\t\t\nSeptember\t\t\t\t\t\t\nOctober\t\t\t\t\t\t\nNovember\t\t\t\t\t\t\nDecember\t\t\t\t\t\t\n------------------------------------------------------------\nTotal\t\t\t\t\t\t"))
        mInsert.add_command(label="To-Do List", command=lambda: editor.insert(INSERT, ("[]\t\n") * 60))
        mInsert.add_command(label="Filename", command=lambda: editor.insert(INSERT, filename))
        m.add_cascade(label="View", menu=mView)
        mView.add_cascade(label="Theme", menu=mTheme)
        mTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#fff", fg="#000"), background="#fff", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#dcb", fg="#000"), background="#dcb", foreground="#000")
        mTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#333", fg="#fff"), background="#333", foreground="#fff")
        mTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#000", fg="#fff"), background="#000", foreground="#fff")
        mView.add_separator()
        mView.add_command(label="Note", command=__init__.note, accelerator="F6")
        mView.add_command(label="Calculator", command=__init__.calc, accelerator="F7")
        mView.add_command(label="Clipboard", command=lambda: messagebox.showinfo("BTXTPad", editor.selection_get(selection='CLIPBOARD')), accelerator="F8")
        mView.add_command(label="Full Screen", command=__init__.full_screen, accelerator="F11")
        editor = scrolledtext.ScrolledText(root, bd=16, relief=FLAT, undo=True)
        editor.grid(row=0, column=0, sticky='nsew')
        root.bind("<Control-n>", lambda a: __init__.file("n"))
        root.bind("<Control-o>", lambda a: __init__.file("o"))
        root.bind("<Control-s>", lambda a: open(filename, 'w', encoding='utf8').write(editor.get(1.0, "end")))
        root.bind("<Control-u>", lambda a: editor.configure(state="disabled"))
        root.bind("<Control-e>", lambda a: editor.configure(state="normal"))
        root.bind("<Control-p>", lambda a: os.startfile(filename, "print"))
        root.bind("<Control-q>", lambda a: os.remove(filename))
        root.bind("<Control-t>", lambda a: editor.configure(font=(simpledialog.askstring("BTXTPad", "Font Name"), simpledialog.askinteger("BTXTPad", "Font Size"), simpledialog.askstring("BTXTPad", "Font Weight\n(normal/bold/italic/underline/etc.)"))))
        root.bind("<Control-l>", lambda a: __init__.length())
        root.bind("<Control-r>", lambda a: __init__.replace())
        root.bind("<Control-f>", lambda a: __init__.find())
        root.bind("<Control-k>", lambda a: __init__.keep())
        root.bind("<Shift-Delete>", lambda a: editor.delete(1.0,"end"))
        root.bind("<F1>", lambda a: messagebox.showinfo("About BTXTPad", "BTXTPad: A text editor\nCopyright (C) 2021-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nMIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."))
        root.bind("<F6>", lambda a: __init__.note())
        root.bind("<F7>", lambda a: __init__.calc())
        root.bind("<F8>", lambda a: messagebox.showinfo("BTXTPad", editor.selection_get(selection='CLIPBOARD')))
        root.bind("<F11>", lambda a: __init__.full_screen())
        root.bind("<F12>", lambda a: __init__.file("s"))
        root.bind("<Button-3>", __init__.right_click)
        root.mainloop()
