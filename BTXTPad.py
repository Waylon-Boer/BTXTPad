from tkinter import *
from tkinter import messagebox, simpledialog, filedialog, scrolledtext
import os, datetime, calendar, math
class program():
    def file(i):
        global filename
        if i == "n":
            filename = "New BTXTPad Document.btxt"
            editor.delete(1.0, "end")
        elif i == "o":
            filename = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
            editor.delete(1.0, "end")
            editor.insert(INSERT, open(filename, 'r', encoding='utf8').read())
        elif i == "s":
            if filename == "":
                program.file("e")
            else:
                open(filename, 'w', encoding='utf8').write(editor.get(1.0, "end"))
        else:
            filename = filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')])
            open(filename, 'w', encoding='utf8').write(editor.get(1.0, "end"))
        root.title(filename+" - BTXTPad")
    def delete():
        global filename
        ch = messagebox.askyesno("BTXTPad","Do you want to delete "+ filename +" permanently?")
        if ch:
            ch = messagebox.askyesno("BTXTPad","Do you want to delete this file permanently? (double check)")
            if ch:
                os.remove(filename)
                editor.delete(1.0, "end")
                filename = ""
                root.title("BTXTPad")
    def read_mode():
        global editable
        if editable == 1:
            editable = 0
            editor.configure(state="disabled")
        else:
            editable = 1
            editor.configure(state="normal")
    def about():
        messagebox.showinfo("About BTXTPad", """BTXTPad - A text editor
Copyright (C) 2022-""" + str(datetime.datetime.now().year) +""": Waylon Boer

BTXTPad is a free and simple text editor. BTXTPad also has some additional features, such as a sidebar and a calculator. The default file format is .btxt, but BTXTPad can also edit other plain text files. BTXTPad was developed for use on Windows, but the source code also works on Linux. Some features do not work on Linux. You can also run BTXTPad in the Windows recovery environment.

Thanks for using BTXTPad!""")
    def license():
        messagebox.showinfo("MIT License", """Copyright (c) 2022 Waylon Boer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
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
        editor.delete(1.0, "sel.first")
        editor.delete("sel.last", "end")
    def find(index):
        editor.mark_set("insert", editor.search(simpledialog.askstring("Find", "Query"), index, stopindex=END))
    def replace():
        try:
            text = editor.get(1.0, "end").replace(editor.get("sel.first", "sel.last"), simpledialog.askstring("Replace All", "Replace"))
        except:
            text = editor.get(1.0, "end").replace(simpledialog.askstring("Replace All", "Find"), simpledialog.askstring("Replace All", "Replace"))
            editor.delete(1.0, "end")
            editor.insert(INSERT, text)
    def goto():
        editor.mark_set("insert", simpledialog.askfloat("Go To", editor.index(INSERT)))
    def underline():
        global u
        if u == 0:
            root.bind("<Right>", lambda i: editor.insert(INSERT, "̲"))
            u = 1
        else:
            root.bind("<Right>", lambda i: editor.insert(INSERT, ""))
            u = 0
    def full_screen():
        global fs
        if fs == 1:
            fs = 0
        else:
            fs = 1
        root.attributes("-fullscreen", fs)
    def sidebar(i):
        global noteMenu
        if i == "h":
            editor.grid(row=0, column=0, sticky="nsew")
            root.columnconfigure(0, minsize=0, weight=1)
            root.columnconfigure(1, minsize=0, weight=0)
            note.grid_forget()
            menubar.delete(4, 5)
            noteMenu = 0            
        elif i == "l":
            note.grid(row=0, column=0, sticky="nsew")
            editor.grid(row=0, column=1, sticky="nsew")
            root.columnconfigure(0, minsize=0, weight=0)
            root.columnconfigure(1, minsize=0, weight=1)
            if noteMenu == 0:
                menubar.add_cascade(label="Note", menu=menuNote)
                noteMenu = 1
        else:
            editor.grid(row=0, column=0, sticky="nsew")
            note.grid(row=0, column=1, sticky="nsew")
            root.columnconfigure(0, minsize=0, weight=1)
            root.columnconfigure(1, minsize=0, weight=0)
            if noteMenu == 0:
                menubar.add_cascade(label="Note", menu=menuNote)
                noteMenu = 1
    def font():
        editor.configure(font=(simpledialog.askstring("Font", "Font Family"), simpledialog.askinteger("Font", "Size"), simpledialog.askstring("Font", "Style")))
    def justify(i):
        editor.tag_add("justify", 1.0, "end")
        if i == "l":
            editor.tag_configure("justify", justify="left")
        elif i == "c":
            editor.tag_configure("justify", justify="center")
        else:
            editor.tag_configure("justify", justify="right")
    def calculator():
        root = Tk()
        root.title("Calculator")
        root.rowconfigure(1, minsize=0, weight=1)
        root.columnconfigure(0, minsize=0, weight=1)
        root.attributes("-toolwindow", 1)
        root.attributes("-topmost", 1)
        root.geometry("200x300")
        root.minsize(200, 300)
        bar = Entry(root, bd=8, font=("", 12), bg="#444", fg="#fff", justify="right")
        bar.grid(row=0, column=0, sticky="nsew")
        f = Frame(root)
        f.grid(row=1, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="x²", command=lambda: messagebox.showinfo("Calculator", "("+bar.get()+")² = "+str(eval(bar.get()) * eval(bar.get())))).grid(row=0, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="√", command=lambda: messagebox.showinfo("Calculator", "sqrt("+bar.get()+") = "+str(math.sqrt(eval(bar.get()))))).grid(row=0, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="bin", command=lambda: messagebox.showinfo("Calculator", "bin("+bar.get()+") = "+bin(int(eval(bar.get()))))).grid(row=0, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=0, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=1, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=1, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=1, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=1, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=2, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=2, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=2, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=2, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=3, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=3, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=3, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=3, column=3, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="C", command=lambda: bar.delete(0, "end")).grid(row=4, column=0, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=4, column=1, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=4, column=2, sticky="nsew")
        Button(f, relief=FLAT, width=5, font=("", 16), text="=", background="#f80", foreground="#fff", command=lambda: messagebox.showinfo("Calculator", bar.get()+" = "+str(eval(bar.get())))).grid(row=4, column=3, sticky="nsew")
        f.rowconfigure(0, minsize=0, weight=1)
        f.rowconfigure(1, minsize=0, weight=1)
        f.rowconfigure(2, minsize=0, weight=1)
        f.rowconfigure(3, minsize=0, weight=1)
        f.rowconfigure(4, minsize=0, weight=1)
        f.columnconfigure(0, minsize=0, weight=1)
        f.columnconfigure(1, minsize=0, weight=1)
        f.columnconfigure(2, minsize=0, weight=1)
        f.columnconfigure(3, minsize=0, weight=1)
        root.mainloop()
    def length():
        try:
            messagebox.showinfo("Length (selection)", str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get("sel.first", "sel.last").split(" "))-1) + " spaces\n" + str(len(editor.get("sel.first", "sel.last").split("\n"))-1) + " lines")
        except:
            messagebox.showinfo("Length (document)", str(len(editor.get("1.0", "end").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get(1.0, "end").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get(1.0, "end").split(" "))-1) + " spaces\n" + str(len(editor.get(1.0, "end").split("\n"))-1) + " lines")
    def close():
        ch = messagebox.askyesno("BTXTPad","Do you want to quit BTXTPad?")
        if ch:
             root.destroy()
    def b3_edit(self):
        menuEdit.tk_popup(self.x_root, self.y_root)
    def b3_note(self):
        menuNote.tk_popup(self.x_root, self.y_root)
if __name__ == "__main__":
    root = Tk()
    fs = 0
    editable = 1
    noteMenu = 0
    filename = ""
    u = 0
    root.title("BTXTPad")
    root.geometry("800x600")
    try:
        root.iconbitmap("btxtpad.ico")
    finally:
        root.rowconfigure(0, minsize=0, weight=1)
        root.columnconfigure(0, minsize=0, weight=1)
        root.protocol('WM_DELETE_WINDOW', program.close)
        menubar = Menu(root, tearoff=0)
        root.configure(menu=menubar)
        menuFile = Menu(root, tearoff=0)
        menubar.add_cascade(label="File", menu=menuFile)
        menuFile.add_command(label="New", command=lambda: program.file("n"), accelerator="Ctrl+N")
        menuFile.add_command(label="Open", command=lambda: program.file("o"), accelerator="Ctrl+O")
        menuFile.add_command(label="Save", command=lambda: program.file("s"), accelerator="Ctrl+S")
        menuFile.add_command(label="Save As", command=lambda: program.file("e"), accelerator="Ctrl+Shift+S")
        menuFile.add_separator()
        menuFile.add_command(label="Print", command=lambda: os.startfile(filename, "print"), accelerator="Ctrl+P")
        menuFile.add_command(label="Delete", command=program.delete, accelerator="Ctrl+Q")
        menuFile.add_separator()
        menuFile.add_command(label="Read Mode", command=program.read_mode, accelerator="F7")
        menuFile.add_separator()
        menuHelp = Menu(root, tearoff=0)
        menuFile.add_cascade(label="Help", menu=menuHelp)
        menuHelp.add_command(label="About", command=program.about, accelerator="F1")
        menuHelp.add_command(label="License", command=program.license, accelerator="F2")
        menuFile.add_command(label="Exit", command=program.close, accelerator="Alt+F4")
        menuEdit = Menu(root, tearoff=0)
        menubar.add_cascade(label="Edit", menu=menuEdit)
        menuEdit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
        menuEdit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
        menuEdit.add_separator()
        menuEdit.add_command(label="Cut", command=program.cut, accelerator="Ctrl+X")
        menuEdit.add_command(label="Copy", command=lambda: program.copy(editor), accelerator="Ctrl+C")
        menuEdit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')), accelerator="Ctrl+V")
        menuEdit.add_command(label="Select All", command=lambda: editor.tag_add(SEL, "1.0", END), accelerator="Ctrl+A")
        menuEdit.add_separator()
        menuEdit.add_command(label="Delete", command=lambda: editor.delete("sel.first", "sel.last"), accelerator="Del")
        menuEdit.add_command(label="Delete All", command=lambda: editor.delete(1.0, "end"), accelerator="Shift+Del")
        menuEdit.add_command(label="Keep", command=program.keep, accelerator="Ctrl+K")
        menuEdit.add_separator()
        menuEdit.add_command(label="Find", command=lambda: program.find(1.0), accelerator="Ctrl+F")
        menuEdit.add_command(label="Find Next", command=lambda: program.find(editor.index(INSERT)), accelerator="Ctrl+Shift+F")
        menuEdit.add_command(label="Replace All", command=program.replace, accelerator="Ctrl+R")
        menuEdit.add_command(label="Go To", command=program.goto, accelerator="Ctrl+G")
        menuEdit.add_separator()
        menuEdit.add_command(label="Underline", command=program.underline, accelerator="Ctrl+U")
        menuInsert = Menu(root, tearoff=0)
        menubar.add_cascade(label="Insert", menu=menuInsert)
        menuInsert.add_command(label="Calendar (year)", command=lambda: editor.insert(INSERT, str(calendar.calendar(int(datetime.datetime.now().year)))))
        menuInsert.add_command(label="Calendar (month)", command=lambda: editor.insert(INSERT, str(calendar.month(int(datetime.datetime.now().year), int(datetime.datetime.now().month)))))
        menuInsert.add_command(label="Bullet", command=lambda: editor.insert(INSERT, "• "))
        menuInsert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
        menuInsert.add_separator()
        menuInsert.add_command(label="Filename", command=lambda: editor.insert(INSERT, filename))
        menuView = Menu(root, tearoff=0)
        menubar.add_cascade(label="View", menu=menuView)
        menuSidebar = Menu(root, tearoff=0)
        menuView.add_cascade(label="Sidebar", menu=menuSidebar)
        menuSidebar.add_command(label="Hide", command=lambda: program.sidebar("h"))
        menuSidebar.add_command(label="Left", command=lambda: program.sidebar("l"))
        menuSidebar.add_command(label="Right", command=lambda: program.sidebar("r"))
        menuView.add_command(label="Clipboard", command=lambda: messagebox.showinfo("Clipboard", editor.selection_get(selection='CLIPBOARD')), accelerator="F6")
        menuView.add_command(label="Calculator", command=program.calculator, accelerator="F8")
        menuView.add_command(label="Length", command=program.length, accelerator="F9")
        menuView.add_separator()
        menuView.add_command(label="Font", command=program.font, accelerator="Ctrl+T")
        menuJustify = Menu(root, tearoff=0)
        menuView.add_cascade(label="Justify", menu=menuJustify)
        menuJustify.add_command(label="Left", command=lambda: program.justify("l"))
        menuJustify.add_command(label="Center", command=lambda: program.justify("c"))
        menuJustify.add_command(label="Right", command=lambda: program.justify("r"))
        menuView.add_separator()
        menuTheme = Menu(root, tearoff=0)
        menuView.add_cascade(label="Theme", menu=menuTheme)
        menuTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#fff", fg="#000"), background="#fff", foreground="#000")
        menuTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#dcb", fg="#000"), background="#dcb", foreground="#000")
        menuTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#333", fg="#fff"), background="#333", foreground="#fff")
        menuTheme.add_command(label="Aa", command=lambda: editor.configure(bg="#000", fg="#fff"), background="#000", foreground="#fff")
        menuView.add_command(label="Full Screen", command=program.full_screen, accelerator="F11")
        menuNote = Menu(root, tearoff=0)
        menuNote.add_command(label="Editor > Note", command=lambda: note.insert("end", editor.get(1.0, "end")))
        menuNote.add_command(label="Note > Editor", command=lambda: editor.insert("end", note.get(1.0, "end")))
        menuNote.add_command(label="Save As", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, "end")))
        menuNote.add_separator()
        menuColor = Menu(root, tearoff=0)
        menuNote.add_cascade(label="Color", menu=menuColor)
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#fc5", fg="#000"), background="#fc5", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#5cf", fg="#000"), background="#5cf", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#d8d", fg="#000"), background="#d8d", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#8d8", fg="#000"), background="#8d8", foreground="#000")
        menuNote.add_separator()
        menuNote.add_command(label="Undo", command=lambda: note.edit_undo())
        menuNote.add_command(label="Redo", command=lambda: note.edit_redo())
        menuNote.add_command(label="Copy", command=lambda: program.copy(note))
        menuNote.add_command(label="Delete All", command=lambda: note.delete(1.0, "end"))
        editor = scrolledtext.ScrolledText(root, bd=16, relief=FLAT, undo=True, font=("Consolas", 11, "normal"))
        editor.grid(row=0, column=0, sticky="nsew")
        note = Text(root, bd=16, relief=FLAT, undo=True, background="#fc5", foreground="#000", font=("Consolas", 11), width=36, height=100)
        root.bind("<Control-n>", lambda i: program.file("n"))
        root.bind("<Control-N>", lambda i: program.file("n"))
        root.bind("<Control-o>", lambda i: program.file("o"))
        root.bind("<Control-O>", lambda i: program.file("o"))
        root.bind("<Control-s>", lambda i: program.file("s"))
        root.bind("<Control-S>", lambda i: program.file("s"))
        root.bind("<Control-Shift-s>", lambda i: program.file("e"))
        root.bind("<Control-Shift-S>", lambda i: program.file("e"))
        root.bind("<Control-p>", lambda i: os.startfile(filename, "print"))
        root.bind("<Control-P>", lambda i: os.startfile(filename, "print"))
        root.bind("<Control-q>", lambda i: program.delete())
        root.bind("<Control-Q>", lambda i: program.delete())
        root.bind("<Control-f>", lambda i: program.find(1.0))
        root.bind("<Control-F>", lambda i: program.find(1.0))
        root.bind("<Control-Shift-f>", lambda i: program.find(editor.index(INSERT)))
        root.bind("<Control-Shift-F>", lambda i: program.find(editor.index(INSERT)))
        root.bind("<Control-r>", lambda i: program.replace())
        root.bind("<Control-R>", lambda i: program.replace())
        root.bind("<Control-g>", lambda i: program.goto())
        root.bind("<Control-G>", lambda i: program.goto())
        root.bind("<Control-k>", lambda i: program.keep())
        root.bind("<Control-K>", lambda i: program.keep())
        root.bind("<Shift-Delete>", lambda i: editor.delete(1.0,"end"))
        root.bind("<Control-t>", lambda i: program.font())
        root.bind("<Control-T>", lambda i: program.font())
        root.bind("<Control-u>", lambda i: program.underline())
        root.bind("<Control-U>", lambda i: program.underline())
        root.bind("<Control-w>", lambda i: program.close())
        root.bind("<Control-W>", lambda i: program.close())
        root.bind("<Control-Insert>", lambda i: program.copy(editor))
        root.bind("<Insert>", lambda i: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')))
        root.bind("<F1>", lambda i: program.about())
        root.bind("<F2>", lambda i: program.license())
        root.bind("<F3>", lambda i: program.find())
        root.bind("<F5>", lambda i: program.file("o"))
        root.bind("<F6>", lambda i: program.clipboard())
        root.bind("<F7>", lambda i: program.read_mode())
        root.bind("<F8>", lambda i: program.calculator())
        root.bind("<F9>", lambda i: program.length())
        root.bind("<F11>", lambda i: program.full_screen())
        root.bind("<F12>", lambda i: program.file("e"))
        editor.bind("<Button-3>", program.b3_edit)
        note.bind("<Button-3>", program.b3_note)
        root.mainloop()
