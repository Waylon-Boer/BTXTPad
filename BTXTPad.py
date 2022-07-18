from tkinter import *
from tkinter import messagebox, simpledialog, filedialog, scrolledtext
from tkinter.ttk import *
import os, datetime, calendar, math, platform
class __init__():
    def open():
        editor.delete(1.0, "end")
        editor.insert(INSERT, open(filedialog.askopenfilename(filetypes=[('All Files', '*.*')]), 'r', encoding='utf8').read())
    def read():
        __init__.open() 
        editor.configure(state="disabled")
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
            text = editor.get(1.0, "end").replace(editor.get("sel.first", "sel.last") , simpledialog.askstring("BTXTPad", "Replace"))
        except:
            text = editor.get(1.0, "end").replace(simpledialog.askstring("BTXTPad", "Find") , simpledialog.askstring("BTXTPad", "Replace"))
        editor.delete(1.0, "end")
        editor.insert(INSERT, text)
    def caps():
        try:
            before, text, after = editor.get(1.0, "sel.first"), editor.get("sel.first", "sel.last").upper(), editor.get("sel.last", "end")
            editor.delete(1.0, "end")
            editor.insert(INSERT, before + text + after)
        except:
            text = editor.get(1.0, "end").upper()
            editor.delete(1.0, "end")
            editor.insert(INSERT, text)
    def length():
        try:
            messagebox.showinfo("BTXTPad", str(len(editor.get("sel.first", "sel.last")) - 1) + " Characters Selected\n" + str(len(editor.get("sel.first", "sel.last").replace(" ", "")) - 1) + " Characters Selected (no spaces)\n" + str(len(editor.get("sel.first", "sel.last").split(" ")) - 1) + " Words Selected")
        except:
            messagebox.showinfo("BTXTPad", str(len(editor.get("1.0", "end")) - 1) + " Characters\n" + str(len(editor.get(1.0, "end").replace(" ", "")) - 1) + " Characters\n" +  str(len(editor.get(1.0, "end").split(" ")) - 1) + " Words")        
    def full_screen():
        global fs
        if fs == True:
            fs = False
        elif fs == False:
            fs = True
        root.attributes("-fullscreen", fs)
    def note():
        root = Tk()
        root.geometry("254x254")
        root.title(str(datetime.datetime.now().date()))
        try:
            root.iconbitmap("btxtpad.ico")
        finally:
            root.resizable(width="False", height="False")
            menu = Menu(root)
            root.config(menu=menu)
            menu.add_command(label="<", command=lambda: note.edit_undo())
            menu.add_command(label=">", command=lambda: note.edit_redo())
            menu.add_command(label="Copy", command=lambda: __init__.copy(note))
            menu.add_command(label="Del", command=lambda: note.delete(1.0, "end"))
            menu.add_command(label="Export", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(note.get(1.0, "end")))
            menu.add_command(label="Send", command=lambda: editor.insert("end", note.get(1.0, "end")))
            menu.add_command(label="+", command=__init__.note)
            note = Text(root, borderwidth=8, relief=FLAT, undo=True, bg="#fc0", fg="#000", font=(None, 11))
            note.pack()
            root.mainloop()
    def calc():
        root = Tk()
        root.title("BTXTPad")
        root.resizable(width=False, height=False)
        try:
            root.iconbitmap("btxtpad.ico")
        finally:
            bar = Entry(root, width=41)
            bar.grid(row=0, column=0)
            f0 = Frame(root)
            f0.grid(row=1, column=0)
            Button(f0, width=10, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=0, column=0)
            Button(f0, width=10, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=0, column=1)
            Button(f0, width=10, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=0, column=2)
            Button(f0, width=2, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=0, column=3)
            Button(f0, width=2, text="√", command=lambda: messagebox.showinfo("BTXTPad", math.sqrt(float(bar.get())))).grid(row=0, column=4)
            Button(f0, width=10, text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=1, column=0)
            Button(f0, width=10, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=1, column=1)
            Button(f0, width=10, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=1, column=2)
            Button(f0, width=2, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=1, column=3)
            Button(f0, width=2, text="x²", command=lambda: messagebox.showinfo("BTXTPad", float(bar.get()) * float(bar.get()))).grid(row=1, column=4)
            Button(f0, width=10, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=2, column=0)
            Button(f0, width=10, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=2, column=1)
            Button(f0, width=10, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=2, column=2)
            Button(f0, width=2, text="*", command=lambda: bar.insert(INSERT, " * ")).grid(row=2, column=3)
            Button(f0, width=2, text="x³", command=lambda: messagebox.showinfo("BTXTPad", float(bar.get()) * float(bar.get()) * float(bar.get()))).grid(row=2, column=4)
            Button(f0, width=10, text="clear", command=lambda: bar.delete(0, "end")).grid(row=3, column=0)
            Button(f0, width=10, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=3, column=1)
            Button(f0, width=10, text="enter", command=lambda: messagebox.showinfo("BTXTPad", eval(bar.get()))).grid(row=3, column=2)
            Button(f0, width=2, text="/", command=lambda: bar.insert(INSERT, " / ")).grid(row=3, column=3)
            Button(f0, width=2, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=3, column=4)
            f1 = Frame(root)
            f1.grid(row=2, column=0)
            Button(f1, text="sin", command=lambda: messagebox.showinfo("BTXTPad", math.sin(float(bar.get())))).grid(row=0, column=0, sticky="nsew")
            Button(f1, text="cos", command=lambda: messagebox.showinfo("BTXTPad", math.cos(float(bar.get())))).grid(row=0, column=1, sticky="nsew")
            Button(f1, text="tan", command=lambda: messagebox.showinfo("BTXTPad", math.tan(float(bar.get())))).grid(row=0, column=2, sticky="nsew")
        root.mainloop()
    def close():
        ch = messagebox.askyesno('BTXTPad','Do you want to quit BTXTPad?')
        if ch:
            root.destroy()
    def right_click(self):
        Menu_Edit.tk_popup(self.x_root, self.y_root)
if __name__ == "__main__":
    root = Tk()
    root.title('BTXTPad')
    try:
        root.iconbitmap("btxtpad.ico")
    finally:
        root.rowconfigure(0, minsize=0, weight=1)
        root.columnconfigure(0, minsize=0, weight=1)
        fs = False
        menu = Menu(root, tearoff=0)
        root.config(menu=menu)
        root.protocol('WM_DELETE_WINDOW', __init__.close)
        Menu_File = Menu(root, tearoff=0)
        menu.add_cascade(label="File", menu=Menu_File)
        Menu_File.add_command(label="New", command=lambda: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(""), accelerator="Ctrl+N")
        Menu_File.add_command(label="Open", command=__init__.open, accelerator="Ctrl+O")
        Menu_File.add_command(label="Save As", command=lambda: open(filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')]), 'w', encoding='utf8').write(editor.get(1.0, "end")), accelerator="Ctrl+S")
        Menu_File.add_command(label="Print", command=lambda: os.startfile(filedialog.askopenfile(filetypes=[('All Files', '*.*')]).name, "print"), accelerator="Ctrl+P")
        Menu_File.add_command(label="Delete", command=lambda: os.remove(filedialog.askopenfile(filetypes=[('All Files', '*.*')]).name), accelerator="Ctrl+Q")
        Menu_File.add_separator()
        Menu_File.add_command(label="Read", command=__init__.read, accelerator="Ctrl+R")
        Menu_File.add_command(label="Edit", command=lambda: editor.configure(state="normal"), accelerator="Ctrl+E")
        Menu_File.add_separator()
        Menu_File.add_command(label="About", command=lambda: messagebox.showinfo("About BTXTPad", "BTXTPad: A text editor\nCopyright (C) 2021-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nMIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n" + "\nOS: " +platform.platform() + "\nCPU: " + platform.processor()), accelerator="F1")
        Menu_File.add_command(label="Exit", command=__init__.close, accelerator="Alt+F4")
        Menu_Edit = Menu(root, tearoff=0)
        menu.add_cascade(label="Edit", menu=Menu_Edit)
        Menu_Edit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
        Menu_Edit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
        Menu_Edit.add_separator()
        Menu_Edit.add_command(label="Cut", command=__init__.cut, accelerator="Ctrl+X")
        Menu_Edit.add_command(label="Copy", command=lambda: __init__.copy(editor), accelerator="Ctrl+C")
        Menu_Edit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')), accelerator="Ctrl+V")
        Menu_Edit.add_separator()
        Menu_Edit.add_command(label="Delete", command=lambda: editor.delete("sel.first", "sel.last"), accelerator="Del")
        Menu_Edit.add_command(label="Keep", command=__init__.keep, accelerator="F6")
        Menu_Edit.add_command(label="Clear", command=lambda: editor.delete(1.0,"end"), accelerator="Shift+Del")
        Menu_Edit.add_separator()
        Menu_Edit.add_command(label="Find", command=__init__.find, accelerator="F3")
        Menu_Edit.add_command(label="Replace", command=__init__.replace, accelerator="F2")
        Menu_Edit.add_command(label="Caps", command=__init__.caps, accelerator="Ctrl+B")
        Menu_Edit.add_separator()
        Menu_Edit.add_command(label="Text Length", command=__init__.length, accelerator="Ctrl+L")
        Menu_Edit.add_command(label="Font", command=lambda: editor.configure(font=(simpledialog.askstring("BTXTPad", "Font Name"), simpledialog.askinteger("BTXTPad", "Font Size"))), accelerator="Ctrl+F")
        Menu_Insert = Menu(root, tearoff=0)
        menu.add_cascade(label="Insert", menu=Menu_Insert)
        Menu_Insert.add_command(label="Calendar", command=lambda: editor.insert(1.0, str(calendar.calendar(int(datetime.datetime.now().year)))))
        Menu_Insert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
        Menu_Insert.add_command(label="To-Do List", command=lambda: editor.insert(INSERT, ("[]\t\n") * 60))
        Menu_Insert.add_command(label="TOC", command=lambda: editor.insert(1.0, "Table Of Contents\n\nChapter\tPage\n" + ("Name\t7\n") * 16))
        Menu_Insert.add_command(label="Greeting", command=lambda: editor.insert("end", "\n\nWith kind regards, John Doe"))
        Menu_Insert.add_command(label="Local Files", command=lambda: editor.insert(1.0, "------------------Local-Directory------------------\n\n-----------------------Start-----------------------\n"+str(os.listdir()).replace("'", "").replace("\"", "").replace("[", "").replace("]", "").replace(", ", "\n")+"\n------------------------End------------------------\n"))
        Menu_Insert.add_command(label="Return", command=lambda: editor.insert(INSERT, "\r"))
        Menu_View = Menu(root, tearoff=0)
        menu.add_cascade(label="View", menu=Menu_View)
        Menu_Theme = Menu(root, tearoff=0)
        Menu_View.add_cascade(label="Theme", menu=Menu_Theme)
        Menu_Theme.add_command(label="Aa", command=lambda: editor.configure(bg="#fff", fg="#000"), background="#fff", foreground="#000")
        Menu_Theme.add_command(label="Aa", command=lambda: editor.configure(bg="#fec", fg="#000"), background="#fec", foreground="#000")
        Menu_Theme.add_command(label="Aa", command=lambda: editor.configure(bg="#345", fg="#fff"), background="#345", foreground="#fff")
        Menu_Theme.add_command(label="Aa", command=lambda: editor.configure(bg="#272727", fg="#fff"), background="#272727", foreground="#fff")
        Menu_Theme.add_command(label="Aa", command=lambda: editor.configure(bg="#000", fg="#fff"), background="#000", foreground="#fff")
        Menu_View.add_separator()
        Menu_View.add_command(label="Note", command=__init__.note, accelerator="F7")
        Menu_View.add_command(label="Calculator", command=__init__.calc, accelerator="F8")
        Menu_View.add_command(label="Clipboard", command=lambda: messagebox.showinfo("BTXTPad", editor.selection_get(selection='CLIPBOARD')), accelerator="F9")
        Menu_View.add_command(label="Full Screen", command=__init__.full_screen, accelerator="F11")
        editor = scrolledtext.ScrolledText(root, borderwidth=16, relief=FLAT, undo=True)
        editor.grid(row=0, column=0, sticky='nsew')
        root.bind("<Control-n>", lambda a: open(filedialog.asksaveasfilename(defaultextension='.btxt', filetypes=[('All Files', '*.*')]), 'w').write(""))
        root.bind("<Control-o>", lambda a: __init__.open())
        root.bind("<Control-s>", lambda a: open(filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')]), 'w', encoding='utf8').write(editor.get(1.0, "end")))
        root.bind("<Control-r>", lambda a: __init__.read())
        root.bind("<Control-e>", lambda a: editor.configure(state="normal"))
        root.bind("<Control-p>", lambda a: os.startfile(filedialog.askopenfile(filetypes=[('All Files', '*.*')]).name, "print"))
        root.bind("<Control-q>", lambda a: os.remove(filedialog.askopenfile(filetypes=[('All Files', '*.*')]).name))
        root.bind("<Control-b>", lambda a: __init__.caps())
        root.bind("<Control-f>", lambda a: editor.configure(font=(simpledialog.askstring("BTXTPad", "Font Name"), simpledialog.askinteger("BTXTPad", "Font Size"))))
        root.bind("<Control-l>", lambda a: __init__.length())
        root.bind("<Shift-Delete>", lambda a: editor.delete(1.0,"end"))
        root.bind("<F1>", lambda a: messagebox.showinfo("About BTXTPad", "BTXTPad: A text editor\nCopyright (C) 2021-" + str(datetime.datetime.now().year) +": Waylon Boer\n\nMIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n" + "\nOS: " +platform.platform() + "\nCPU: " + platform.processor()))
        root.bind("<F2>", lambda a: __init__.replace())
        root.bind("<F3>", lambda a: __init__.find())
        root.bind("<F5>", lambda a: __init__.open())
        root.bind("<F6>", lambda a: __init__.keep())
        root.bind("<F7>", lambda a: __init__.note())
        root.bind("<F8>", lambda a: __init__.calc())
        root.bind("<F9>", lambda a: messagebox.showinfo("BTXTPad", editor.selection_get(selection='CLIPBOARD')))
        root.bind("<F11>", lambda a: __init__.full_screen())
        root.bind("<F12>", lambda a: open(filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[('All Files', '*.*')]), 'w', encoding='utf8').write(editor.get(1.0, "end")))
        root.bind("<Button-3>", __init__.right_click)
        root.bind("<Shift-F10>", lambda a: menu.tk_popup(16, 16))
        root.mainloop()
