from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, font, filedialog, scrolledtext
from tkinter import Label as tk_Label
import os, datetime, calendar, math
class main():
    def file(i):
        global filepath, statusbar
        if i == "n":
            filepath = "New BTXTPad Document.btxt"
            editor.delete(1.0, END)
        elif i == "o":
            filepath = filedialog.askopenfilename(filetypes=[("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("Comma Separated Values", "*.csv*"), ("HyperText Markup Language", "*.html*"), ("All Files", "*.*")])
            editor.delete(1.0, END)
            if filepath.split(".")[len(filepath.split(".")) - 1] == "csv":
                editor.insert(INSERT, open(filepath, 'r', encoding='utf8').read().replace(";", "\t"))
            else:
                editor.insert(INSERT, open(filepath, 'r', encoding='utf8').read())
        elif i == "s":
            if filepath == "New BTXTPad Document.btxt":
                main.file("e")
            else:
                open(filepath, 'w', encoding='utf8').write(editor.get(1.0, END))
        else:
            path = filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')])
            try:
                open(path, 'w', encoding='utf8').write(editor.get(1.0, END))
                filepath = path
            except:
                filepath = "New BTXTPad Document.btxt"
        root.title(filepath.split("/")[len(filepath.split("/")) - 1]+" - BTXTPad")
    def delete():
        global filepath
        ch = messagebox.askyesno("BTXTPad","Do you want to delete this file permanently?")
        if ch:
            ch = messagebox.askyesno("BTXTPad","Do you want to delete this file permanently? (double check)")
            if ch:
                os.remove(filepath)
                editor.delete(1.0, END)
                filepath = "New BTXTPad Document.btxt"
                root.title("BTXTPad")
    def read_mode():
        global editable
        if editable == 1:
            editable = 0
            editor.configure(state="disabled")
        else:
            editable = 1
            editor.configure(state="normal")
        main.status_bar.refresh()
    def about():
        messagebox.showinfo("About BTXTPad", """BTXTPad - a text editor
Copyright (C) 2022-""" + str(datetime.datetime.now().year) +""": Waylon Boer

BTXTPad is a simple text editor. BTXTPad has some additional features, for example a sidebar. The default file format is .btxt, but BTXTPad can also edit other plain text files. There is also a standalone notetaking app available: BTXTPad Note.

Thanks for using BTXTPad!""")
    def license():
        messagebox.showinfo("MIT License", """Copyright (c) 2022 Waylon Boer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR a PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
    def cut():
        editor.clipboard_clear()
        editor.delete("sel.first", "sel.last")
        editor.clipboard_append(editor.get("sel.first", "sel.last"))
    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.get("sel.first", "sel.last"))
    def keep():
        editor.delete(1.0, "sel.first")
        editor.delete("sel.last", END)
    def find_next(find, ln, col):
        lc = editor.search(find, editor.index(INSERT))
        editor.mark_set(INSERT, float(str(lc).split(".")[0]+"."+str(int(str(lc).split(".")[1])+len(find))))
        editor.tag_remove(SEL, 1.0, END)
        editor.tag_add(SEL, lc, float(str(lc).split(".")[0]+"."+str(int(str(lc).split(".")[1])+len(find))))
        try:
            main.refresh_lc(ln, col)
        except:
            editor.focus_set()
        main.status_bar.refresh()
    def replace_next(find, replace, ln, col):
        lc = editor.search(find, editor.index(INSERT))
        editor.mark_set(INSERT, float(str(lc).split(".")[0]+"."+str(int(str(lc).split(".")[1])+len(find))))
        editor.delete(lc, float(str(lc).split(".")[0]+"."+str(int(str(lc).split(".")[1])+len(find))))
        editor.insert(INSERT, replace)
        main.refresh_lc(ln, col)
    def replace_all(find, replace, ln, col):
        text = editor.get(1.0, END).replace(find, replace)
        editor.delete(1.0, END)
        editor.insert(INSERT, text)
        main.refresh_lc(ln, col)
    def refresh_lc(ln, col):
        main.status_bar.refresh()
        ln.delete(0, END)
        ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
        col.delete(0, END)
        col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
    def replace():
        app = Tk()
        app.title("Replace")
        app.rowconfigure(0, weight=1)
        app.columnconfigure(0, weight=1)
        app.geometry("400x132")
        app.resizable(width=False, height=False)
        try:
            app.iconbitmap("btxtpad.ico")
        finally:
            f = Frame(app, border=16)
            f.grid(row=0, column=0, sticky="nsew")
            f.columnconfigure(1, weight=1)
            Label(f, text="Find", width=12).grid(row=0, column=0, sticky="w")
            find = Entry(f)
            find.grid(row=0, column=1, sticky="nsew")
            Button(f, text="Find", command=lambda: main.find_next(find.get(), ln, col)).grid(row=0, column=2, sticky="nsew")
            Label(f, text="Replace", width=12).grid(row=1, column=0, sticky="w")
            replace = Entry(f)
            replace.grid(row=1, column=1, sticky="nsew")
            Button(f, text="Replace", command=lambda: main.replace_next(find.get(), replace.get(), ln, col)).grid(row=1, column=2, sticky="nsew")
            Label(f, text="Line", width=12).grid(row=2, column=0, sticky="nsew")
            ln = Entry(f)
            ln.grid(row=2, column=1, sticky="nsew")
            ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
            Button(f, text="Replace All", command=lambda: main.replace_all(find.get(), replace.get(), ln, col)).grid(row=2, column=2, sticky="nsew")
            Label(f, text="Colunn", width=12).grid(row=3, column=0, sticky="nsew")
            col = Entry(f)
            col.grid(row=3, column=1, sticky="nsew")
            col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
            Button(f, text="Go To", command=lambda: editor.mark_set(INSERT, float(str(int(ln.get()))+"."+str(int(col.get()))))).grid(row=3, column=2, sticky="nsew")
            app.mainloop()  
    def go_to():
        app = Tk()
        app.title("Go To")
        app.rowconfigure(0, weight=1)
        app.columnconfigure(0, weight=1)
        app.geometry("400x80")
        app.resizable(width=False, height=False)
        try:
            app.iconbitmap("btxtpad.ico")
        finally:
            f = Frame(app, border=16)
            f.grid(row=0, column=0, sticky="nsew")
            f.columnconfigure(1, weight=1)
            Label(f, text="Line", width=12).grid(row=0, column=0, sticky="nsew")
            ln = Entry(f)
            ln.grid(row=0, column=1, sticky="nsew")
            ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
            Button(f, text="Refresh", command=lambda: main.refresh_lc(ln, col)).grid(row=0, column=2, sticky="nsew")
            Label(f, text="Colunn", width=12).grid(row=1, column=0, sticky="nsew")
            col = Entry(f)
            col.grid(row=1, column=1, sticky="nsew")
            col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
            Button(f, text="Go To", command=lambda: editor.mark_set(INSERT, float(str(int(ln.get()))+"."+str(int(col.get()))))).grid(row=1, column=2, sticky="nsew")
            app.mainloop()  
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
        if i == "h":
            frameEditor.grid(row=0, column=0, sticky="nsew")
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0)
            sidebar.grid_forget()        
        elif i == "l":
            sidebar.grid(row=0, column=0, sticky="nsew")
            frameEditor.grid(row=0, column=1, sticky="nsew")
            root.columnconfigure(0, weight=0)
            root.columnconfigure(1, weight=1)
        else:
            frameEditor.grid(row=0, column=0, sticky="nsew")
            sidebar.grid(row=0, column=1, sticky="nsew")
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0)
    def note():
        calc.grid_forget()
        note.grid(row=1, column=0, sticky="nsew")
        buttonOptions.grid(row=0, column=1, sticky="nsew")
        buttonWidgets.configure(text="Note")
    def calculator():
        note.grid_forget()
        buttonOptions.grid_forget()
        calc.grid(row=1, column=0, sticky="nsew")
        buttonWidgets.configure(text="Calculator")
    def calculate(type):
        eq = bar.get()
        if type == "bin":
            eq = str(bin(int(eval(eq))))
        elif type == "oct":
            eq = str(oct(int(eval(eq))))
        elif type == "hex":
            eq = str(hex(int(eval(eq))))
        elif type == "inv":
            eq = str(1/float(eval(eq)))
        elif type == "sq":
            eq = str(eval(eq) * eval(eq))
        elif type == "sq3":
            eq = str(eval(eq) * eval(eq) * eval(eq))
        elif type == "sqrt":
            eq = str(math.sqrt(eval(eq)))
        else:
            eq = eval(eq)
        bar.delete(0, END)
        bar.insert(INSERT, eq)
    def change_font(self, font_family, size, style):
        editor.configure(font=(font_family, size, style))
        self.destroy()
    def font():
        app = Tk()
        app.title("Font")
        app.rowconfigure(0, weight=1)
        app.columnconfigure(0, weight=1)
        app.geometry("275x125")
        app.resizable(height=False, width=False)
        try:
            app.iconbitmap("btxtpad.ico")
        finally:
            f = Frame(app, border=16)
            f.grid(row=0, column=0, sticky="nsew")
            f.rowconfigure(3, weight=1)
            f.columnconfigure(1, weight=1)
            Label(f, text="Font Family", width=12).grid(row=0, column=0, sticky="w")
            font_family = Combobox(f, values=font.families())
            font_family.grid(row=0, column=1, sticky="nsew")
            Label(f, text="Size", width=12).grid(row=1, column=0, sticky="w")
            size = Combobox(f, values=("8", "9", "10", "11", "12", "14", "16", "18", "20", "22", "24", "26", "28", "36", "48", "72"))
            size.grid(row=1, column=1, sticky="nsew")
            Label(f, text="Style", width=12).grid(row=2, column=0, sticky="w")
            style = Combobox(f, values=("normal", "bold", "italic", "bold italic", "underline", "bold underline", "italic underline", "bold italic underline"))
            style.grid(row=2, column=1, sticky="nsew")
            Label(f, text="Save", width=12).grid(row=3, column=0, sticky="w")
            action_button = Button(f, text="OK", command=lambda: main.change_font(app, font_family.get(), int(size.get()), style.get()))
            action_button.grid(row=3, column=1, sticky="nsew")
            app.bind("<Return>", lambda i: main.change_font(app, font_family.get(), int(size.get()), style.get()))
            app.mainloop()
    def align(i):
        editor.tag_add("alignment", 1.0, END)
        editor.tag_configure("alignment", justify=i)
    def theme(bg1, fg1, bg2, fg2):
        editor.configure(bg=bg1, fg=fg1)
        status_bar.configure(bg=bg2, fg=fg2)
    def switch_theme():
        global theme
        if theme == 0:
            main.theme("#dcb", "#000", "#654", "#fff")
            theme = 1
        elif theme == 1:
            main.theme("#333", "#fff", "#345", "#fff")
            theme = 2
        elif theme == 2:
            main.theme("#000", "#fff", "#000", "#0f0")
            theme = 3
        else:
            main.theme("#fff", "#000", "#f0f0f0", "#000")
            theme = 0
    def exit():
        ch = messagebox.askyesno("BTXTPad","Do you want to exit BTXTPad?")
        if ch:
             root.destroy()
    def b3_edit(self):
        menuEdit.tk_popup(self.x_root, self.y_root)
    def b3_note(self):
        menuOptions.tk_popup(self.x_root, self.y_root)
    class status_bar():
        def refresh():
            if editable == 0:
                mode = "Read Mode"
            else:
                mode = "Edit Mode"
            l = editor.index(INSERT).split(".")[0]
            c = editor.index(INSERT).split(".")[1]
            lines = str(len(editor.get(1.0, END).split("\n"))-1)
            characters = str(len(editor.get(1.0, END)) - 1)
            try:
                if len(editor.selection_get(selection="CLIPBOARD")) > 50:
                    clipboard = editor.selection_get(selection="CLIPBOARD").replace("\n", " ")[:50] + "..."
                else:
                    clipboard = editor.selection_get(selection="CLIPBOARD").replace("\n", " ")
            except:
                clipboard = "Empty"
            status_bar.configure(text=mode+" | Line " + l + "/" + lines + "; Column: " + c + " | Characters: " + characters +" | Clipboard: " + clipboard)
        def toggle():
            global statusbar
            if statusbar == 0:
                status_bar.grid(row=2, column=0, sticky="nsew")
                statusbar = 1
            else:
                status_bar.grid_forget()
                statusbar = 0
            main.status_bar.refresh()
if __name__ == "__main__":
    root = Tk()
    filepath, fs, editable, u, statusbar, theme = "New BTXTPad Document.btxt", 0, 1, 0, 0, 0
    root.title("BTXTPad")
    root.geometry("800x600")
    try:
        root.iconbitmap("btxtpad.ico")
    finally:
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.protocol('WM_DELETE_WINDOW', main.exit)
        frameEditor = Frame(root)
        frameEditor.grid(row=0, column=0, sticky="nsew")
        frameEditor.rowconfigure(1, weight=1)
        frameEditor.columnconfigure(0, weight=1)
        menu_bar_editor = Frame(frameEditor, border=5)
        menu_bar_editor.grid(row=0, column=0, sticky="nsew")
        menu_bar_editor.columnconfigure(4, weight=1)
        buttonFile = Menubutton(menu_bar_editor, text="File")
        buttonFile.grid(row=0, column=0, sticky="nsew")
        buttonEdit = Menubutton(menu_bar_editor, text="Edit")
        buttonEdit.grid(row=0, column=1, sticky="nsew")
        buttonInsert = Menubutton(menu_bar_editor, text="Insert")
        buttonInsert.grid(row=0, column=2, sticky="nsew")
        buttonView = Menubutton(menu_bar_editor, text="View")
        buttonView.grid(row=0, column=3, sticky="nsew")
        query = Entry(menu_bar_editor)
        query.grid(row=0, column=4, sticky="nsew")
        Button(menu_bar_editor, text="Search", command=lambda: main.find_next(query.get(), 0, 0)).grid(row=0, column=5, sticky="nsew")
        menuFile = Menu(buttonFile, tearoff=False)
        buttonFile.configure(menu=menuFile)
        menuFile.add_command(label="New", command=lambda: main.file("n"), accelerator="Ctrl+N")
        menuFile.add_command(label="Open", command=lambda: main.file("o"), accelerator="Ctrl+O")
        menuFile.add_command(label="Save", command=lambda: main.file("s"), accelerator="Ctrl+S")
        menuFile.add_command(label="Save As", command=lambda: main.file("e"), accelerator="Ctrl+Shift+S")
        menuFile.add_separator()
        menuFile.add_command(label="Print", command=lambda: os.startfile(filepath, "print"), accelerator="Ctrl+P")
        menuFile.add_command(label="Delete", command=main.delete, accelerator="Ctrl+Q")
        menuFile.add_separator()
        menuFile.add_command(label="Read Mode", command=main.read_mode, accelerator="F7")
        menuFile.add_separator()
        menuFile.add_command(label="About", command=main.about, accelerator="F1")
        menuFile.add_command(label="License", command=main.license, accelerator="F2")
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=root.destroy, accelerator="Alt+F4")
        menuEdit = Menu(buttonEdit, tearoff=False)
        buttonEdit.configure(menu=menuEdit)
        menuEdit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
        menuEdit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
        menuEdit.add_separator()
        menuEdit.add_command(label="Cut", command=main.cut, accelerator="Ctrl+X")
        menuEdit.add_command(label="Copy", command=lambda: main.copy(editor), accelerator="Ctrl+C")
        menuEdit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')), accelerator="Ctrl+V")
        menuEdit.add_command(label="Select All", command=lambda: editor.tag_add(SEL, 1.0, END), accelerator="Ctrl+A")
        menuEdit.add_separator()
        menuEdit.add_command(label="Delete", command=lambda: editor.delete("sel.first", "sel.last"), accelerator="Del")
        menuEdit.add_command(label="Delete All", command=lambda: editor.delete(1.0, END), accelerator="Shift+Del")
        menuEdit.add_command(label="Keep", command=main.keep, accelerator="Ctrl+K")
        menuEdit.add_separator()
        menuEdit.add_command(label="Find", command=lambda: main.find_next(query.get(), 0, 0), accelerator="Ctrl+F")
        menuEdit.add_command(label="Replace", command=main.replace, accelerator="Ctrl+R")
        menuEdit.add_command(label="Go To", command=main.go_to, accelerator="Ctrl+G")
        menuEdit.add_separator()
        menuEdit.add_command(label="Underline", command=main.underline, accelerator="Ctrl+U")
        menuInsert = Menu(buttonInsert, tearoff=False)
        buttonInsert.configure(menu=menuInsert)
        menuInsert.add_command(label="Calendar (year)", command=lambda: editor.insert(INSERT, str(calendar.calendar(int(datetime.datetime.now().year)))))
        menuInsert.add_command(label="Calendar (month)", command=lambda: editor.insert(INSERT, str(calendar.month(int(datetime.datetime.now().year), int(datetime.datetime.now().month)))))
        menuInsert.add_command(label="Bullet", command=lambda: editor.insert(INSERT, "• "))
        menuInsert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
        menuInsert.add_separator()
        menuInsert.add_command(label="Filename", command=lambda: editor.insert(INSERT, filepath.split("/")[len(filepath.split("/")) - 1]))
        menuView = Menu(buttonView, tearoff=False)
        buttonView.configure(menu=menuView)
        menuSidebar = Menu(root, tearoff=False)
        menuView.add_cascade(label="Sidebar", menu=menuSidebar)
        menuSidebar.add_command(label="Hide", command=lambda: main.sidebar("h"), accelerator="Ctrl+,")
        menuSidebar.add_command(label="Left", command=lambda: main.sidebar("l"), accelerator="Ctrl+.")
        menuSidebar.add_command(label="Right", command=lambda: main.sidebar("r"), accelerator="Ctrl+/")    
        menuView.add_command(label="Status Bar", command=main.status_bar.toggle, accelerator="F9")
        menuView.add_separator()
        menuView.add_command(label="Font", command=main.font, accelerator="F6")
        menuAlign = Menu(root, tearoff=False)
        menuView.add_cascade(label="Align", menu=menuAlign)
        menuAlign.add_command(label="Left", command=lambda: main.align("left"))
        menuAlign.add_command(label="Center", command=lambda: main.align("center"))
        menuAlign.add_command(label="Right", command=lambda: main.align("right"))
        menuView.add_separator()
        menuTheme = Menu(root, tearoff=False)
        menuView.add_cascade(label="Theme", menu=menuTheme)
        menuTheme.add_command(label="Aa", command=lambda: main.theme("#fff", "#000", "#f0f0f0", "#000"), background="#fff", foreground="#000")
        menuTheme.add_command(label="Aa", command=lambda: main.theme("#dcb", "#000", "#654", "#fff"), background="#dcb", foreground="#000")
        menuTheme.add_command(label="Aa", command=lambda: main.theme("#333", "#fff", "#345", "#fff"), background="#333", foreground="#fff")
        menuTheme.add_command(label="Aa", command=lambda: main.theme("#000", "#fff", "#000", "#0f0"), background="#000", foreground="#fff")
        menuView.add_command(label="Full Screen", command=main.full_screen, accelerator="F11")
        editor = scrolledtext.ScrolledText(frameEditor, bd=16, relief=FLAT, undo=True, font=("Consolas", 11, "normal"))
        editor.grid(row=1, column=0, sticky="nsew")
        status_bar = tk_Label(frameEditor, border=5, anchor="w")
        sidebar = Frame(root)
        sidebar.rowconfigure(1, weight=1)
        sidebar.columnconfigure(0, weight=1)
        menu_bar_sidebar = Frame(sidebar, border=5)
        menu_bar_sidebar.grid(row=0, column=0, sticky="nsew")
        buttonWidgets = Menubutton(menu_bar_sidebar, text="Note")
        buttonWidgets.grid(row=0, column=0, sticky="nsew")
        menuWidgets = Menu(buttonWidgets, tearoff=False)
        buttonWidgets.configure(menu=menuWidgets)
        menuWidgets.add_command(label="Note", command=main.note)
        menuWidgets.add_command(label="Calculator", command=main.calculator)
        buttonOptions = Menubutton(menu_bar_sidebar, text="Options")
        buttonOptions.grid(row=0, column=1, sticky="nsew")
        menuOptions = Menu(buttonOptions, tearoff=False)
        buttonOptions.configure(menu=menuOptions)
        menuOptions.add_command(label="Editor > Note", command=lambda: note.insert(END, editor.get(1.0, END)))
        menuOptions.add_command(label="Note > Editor", command=lambda: editor.insert(END, note.get(1.0, END)))
        menuOptions.add_command(label="Save As", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, END)))
        menuOptions.add_separator()
        menuColor = Menu(buttonOptions, tearoff=False)
        menuOptions.add_cascade(label="Color", menu=menuColor)
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#fc5", fg="#000"), background="#fc5", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#5cf", fg="#000"), background="#5cf", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#d8d", fg="#000"), background="#d8d", foreground="#000")
        menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#8d8", fg="#000"), background="#8d8", foreground="#000")
        menuOptions.add_separator()
        menuOptions.add_command(label="Undo", command=lambda: note.edit_undo())
        menuOptions.add_command(label="Redo", command=lambda: note.edit_redo())
        menuOptions.add_command(label="Copy", command=lambda: main.copy(note))
        menuOptions.add_command(label="Delete All", command=lambda: note.delete(1.0, END))
        note = Text(sidebar, bd=16, relief=FLAT, undo=True, background="#fc5", foreground="#000", font=("Consolas", 11), width=36, height=100)
        note.grid(row=1, column=0, sticky="nsew")
        calc = Frame(sidebar, width=36)
        calc.rowconfigure(1, weight=1)
        calc.columnconfigure(0, weight=1)
        bar = Entry(calc, font=("", 12))
        bar.grid(row=0, column=0, sticky="nsew", ipady=8)
        frameCalculator = Frame(calc)
        frameCalculator.grid(row=1, column=0, sticky="nsew")
        Button(frameCalculator, text="bin", command=lambda: main.calculate("bin")).grid(row=0, column=0, sticky="nsew")
        Button(frameCalculator, text="oct", command=lambda: main.calculate("oct")).grid(row=0, column=1, sticky="nsew")
        Button(frameCalculator, text="hex", command=lambda: main.calculate("hex")).grid(row=0, column=2, sticky="nsew")
        Button(frameCalculator, text="1/x", command=lambda: main.calculate("inv")).grid(row=0, column=3, sticky="nsew")
        Button(frameCalculator, text="x²", command=lambda: main.calculate("sq")).grid(row=1, column=0, sticky="nsew")
        Button(frameCalculator, text="x³", command=lambda: main.calculate("sq3")).grid(row=1, column=1, sticky="nsew")
        Button(frameCalculator, text="√", command=lambda: main.calculate("sqrt")).grid(row=1, column=2, sticky="nsew")
        Button(frameCalculator, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=1, column=3, sticky="nsew")
        Button(frameCalculator, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=2, column=0, sticky="nsew")
        Button(frameCalculator, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=2, column=1, sticky="nsew")
        Button(frameCalculator, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=2, column=2, sticky="nsew")
        Button(frameCalculator, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=2, column=3, sticky="nsew")
        Button(frameCalculator, text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=3, column=0, sticky="nsew")
        Button(frameCalculator, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=3, column=1, sticky="nsew")
        Button(frameCalculator, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=3, column=2, sticky="nsew")
        Button(frameCalculator, text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=3, column=3, sticky="nsew")
        Button(frameCalculator, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=4, column=0, sticky="nsew")
        Button(frameCalculator, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=4, column=1, sticky="nsew")
        Button(frameCalculator, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=4, column=2, sticky="nsew")
        Button(frameCalculator, text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=4, column=3, sticky="nsew")
        Button(frameCalculator, text="C", command=lambda: bar.delete(0, END)).grid(row=5, column=0, sticky="nsew")
        Button(frameCalculator, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=5, column=1, sticky="nsew")
        Button(frameCalculator, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=5, column=2, sticky="nsew")
        Button(frameCalculator, text="=", command=lambda: main.calculate("eq")).grid(row=5, column=3, sticky="nsew")
        for i in range(0, 6):
            frameCalculator.rowconfigure(i, weight=1)
        for j in range(0, 4):
            frameCalculator.columnconfigure(j, weight=1)
        root.bind("<Control-n>", lambda i: main.file("n"))
        root.bind("<Control-N>", lambda i: main.file("n"))
        root.bind("<Control-o>", lambda i: main.file("o"))
        root.bind("<Control-O>", lambda i: main.file("o"))
        root.bind("<Control-s>", lambda i: main.file("s"))
        root.bind("<Control-S>", lambda i: main.file("s"))
        root.bind("<Control-Shift-s>", lambda i: main.file("e"))
        root.bind("<Control-Shift-S>", lambda i: main.file("e"))
        root.bind("<Control-p>", lambda i: os.startfile(filepath, "print"))
        root.bind("<Control-P>", lambda i: os.startfile(filepath, "print"))
        root.bind("<Control-q>", lambda i: main.delete())
        root.bind("<Control-Q>", lambda i: main.delete())
        root.bind("<Control-f>", lambda i: main.find_next(query.get(), 0, 0))
        root.bind("<Control-F>", lambda i: main.find_next(query.get(), 0, 0))
        root.bind("<Control-r>", lambda i: main.replace())
        root.bind("<Control-R>", lambda i: main.replace())
        root.bind("<Control-g>", lambda i: main.go_to())
        root.bind("<Control-G>", lambda i: main.go_to())
        root.bind("<Control-k>", lambda i: main.keep())
        root.bind("<Control-K>", lambda i: main.keep())
        root.bind("<Shift-Delete>", lambda i: editor.delete(1.0,END))
        root.bind("<Control-u>", lambda i: main.underline())
        root.bind("<Control-U>", lambda i: main.underline())
        root.bind("<Control-w>", lambda i: root.destroy())
        root.bind("<Control-W>", lambda i: root.destroy())
        root.bind("<Control-,>", lambda i: main.sidebar("h"))
        root.bind("<Control-.>", lambda i: main.sidebar("l"))
        root.bind("<Control-/>", lambda i: main.sidebar("r"))
        root.bind("<Control-Insert>", lambda i: main.copy(editor))
        root.bind("<Insert>", lambda i: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')))
        root.bind("<F1>", lambda i: main.about())
        root.bind("<F2>", lambda i: main.license())
        root.bind("<F3>", lambda i: main.find_next(query.get(), 0, 0))
        root.bind("<F5>", lambda i: main.file("o"))
        root.bind("<F6>", lambda i: main.font())
        root.bind("<F7>", lambda i: main.read_mode())
        root.bind("<F8>", lambda i: main.switch_theme())
        root.bind("<F9>", lambda i: main.status_bar.toggle())
        root.bind("<F10>", lambda i: query.focus_set())
        root.bind("<F11>", lambda i: main.full_screen())
        root.bind("<F12>", lambda i: main.file("e"))
        editor.bind("<KeyRelease>", lambda i: main.status_bar.refresh())
        editor.bind("<Button-1>", lambda i: main.status_bar.refresh())
        editor.bind("<Button-3>", main.b3_edit)
        note.bind("<Button-3>", main.b3_note)
        bar.bind("<Return>", lambda i: main.calculate("eq"))
        root.mainloop()
