from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, simpledialog, font, filedialog, scrolledtext
from urllib.request import urlopen
import os, shutil, datetime, calendar, math, html, re

class main():
    def new():
        global filepath
        if editor.get(1.0, END) != "\n":
            choice = messagebox.askyesnocancel("BTXTPad","Do you want to save the changes made to this file?")
            if choice == True:
                main.save()
            elif choice == False:
                editor.delete(1.0, END)
                filepath = ""
                root.title("BTXTPad")
        else: 
            editor.delete(1.0, END)
            filepath = ""
            root.title("BTXTPad")
    def open():
        global filepath
        filepath = filedialog.askopenfilename(filetypes=[("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("Comma Separated Values", "*.csv*"), ("HyperText Markup Language", "*.html*"), ("All Files", "*.*")])
        if filepath == "":
            editor.insert(INSERT, "")
        else:
            editor.delete(1.0, END)
            if filepath.split(".")[len(filepath.split(".")) - 1] == "csv":
                choice = messagebox.askokcancel("BTXTPad","Do you want to convert this file to plain text?")
                if choice == True:
                    editor.insert(INSERT, open(filepath, "r", encoding="utf8").read().replace(";", "\t"))
                else:
                    editor.insert(INSERT, open(filepath, "r", encoding="utf8").read())
            else:
                editor.insert(INSERT, open(filepath, "r", encoding="utf8").read())
            root.title(filepath.split("/")[len(filepath.split("/")) - 1]+" - BTXTPad")
    def save():
        global filepath
        if filepath == "":
            main.save_as()
        else:
            open(filepath, "w", encoding='utf8').write(editor.get(1.0, END))
        root.title(filepath.split("/")[len(filepath.split("/")) - 1]+" - BTXTPad")
    def save_as():
        global filepath
        path = filepath
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[("All Files", "*.*")])
            open(filepath, "w", encoding='utf8').write(editor.get(1.0, END))
            root.title(filepath.split("/")[len(filepath.split("/")) - 1]+" - BTXTPad")
        except FileNotFoundError:
            filepath = path
    def duplicate():
        filepath = filedialog.askopenfilename(title="Copy", filetypes=[("All Files", "*.*"), ("BTXTPad Documents", "*.btxt*"), ('Plain Text Files', "*.txt*"), ("Comma Separated Values", "*.csv*"), ("HyperText Markup Language", "*.html*")])
        shutil.copy(filepath, filedialog.askdirectory(title="Copy to")+"/"+filepath.split("/")[len(filepath.split("/")) - 1])
    def read_mode():
        editor.configure(state="disabled")
        menuFile.delete(8, 11)
        menuFile.add_command(label="Edit Mode", command=main.edit_mode, accelerator="Ctrl+E")
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=main.exit, accelerator="Alt+F4")
        root.bind("<Control-e>", lambda i: main.edit_mode())
        root.bind("<Control-E>", lambda i: main.edit_mode())
        root.bind("<F7>", lambda i: main.edit_mode())
    def edit_mode():
        editor.configure(state="normal")
        menuFile.delete(8, 11)
        menuFile.add_command(label="Read Mode", command=main.read_mode, accelerator="Ctrl+E")
        menuFile.add_separator()
        menuFile.add_command(label="Exit", command=main.exit, accelerator="Alt+F4")
        root.bind("<Control-e>", lambda i: main.read_mode())
        root.bind("<Control-E>", lambda i: main.read_mode())
        root.bind("<F7>", lambda i: main.read_mode())
    def cut():
        editor.clipboard_clear()
        editor.delete(SEL_FIRST, SEL_LAST)
        editor.clipboard_append(editor.get(SEL_FIRST, SEL_LAST))
    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.get(SEL_FIRST, SEL_LAST))
    def keep():
        editor.delete(1.0, SEL_FIRST)
        editor.delete(SEL_LAST, END)
    def find_a():
        try:
            find.delete(0, END)
            find.insert(INSERT, editor.get(SEL_FIRST, SEL_LAST))
        finally:
            if frameReplace.winfo_viewable() == 0:
                main.sidebar("r")
                main.replace()
                find.focus_set()
            else:
                main.find_next(find.get())
    def replace_a():
        if frameReplace.winfo_viewable() == 0:
            main.sidebar("r")
            main.replace()
            replace.focus_set()
        else:
            main.replace_next(find.get(), replace.get())
    def go_to_a():
        if frameReplace.winfo_viewable() == 0:
            main.sidebar("r")
            main.replace()
            ln.focus_set()
        else:
            main.go_to()
    def font_a():
        if sidebar.winfo_viewable() == 0:
            main.sidebar("r")
        main.font()
        font_family.focus_set()
    def help_a():
        if sidebar.winfo_viewable() == 0:
            main.sidebar("r")
            main.help()
        else:
            main.sidebar("h")
    def find_next(find):
        lc = editor.search(find, editor.index(INSERT))
        editor.tag_remove(SEL, 1.0, END)
        editor.tag_add(SEL, lc, "{}.{}".format(*lc.split(".")[:-1], int(lc.split(".")[-1])+len(find)))
        editor.mark_set(INSERT, "{}.{}".format(*lc.split(".")[:-1], int(lc.split(".")[-1])+len(find)))
        editor.focus_set()
    def replace_next(find, replace):
        main.find_next(find)
        text = editor.get(SEL_FIRST, SEL_LAST)
        editor.delete(SEL_FIRST, SEL_LAST)
        editor.insert(INSERT, replace)
    def replace_all(find, replace):
        text = editor.get(1.0, END).replace(find, replace)
        editor.delete(1.0, END)
        editor.insert(INSERT, text)
        editor.delete("end-1c linestart", END)
    def refresh_lc(ln, col):
        ln.delete(0, END)
        ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
        col.delete(0, END)
        col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
    def go_to():
        editor.mark_set(INSERT, float(str(int(ln.get()))+"."+str(int(col.get()))))
        editor.focus_set()
    def solve():
        try:
            ans = eval(editor.get(SEL_FIRST, SEL_LAST))
            editor.delete(SEL_FIRST, SEL_LAST)
            editor.insert(INSERT, ans)
        except:
            main.find_next(find.get())
            ans = eval(editor.get(SEL_FIRST, SEL_LAST))
            editor.delete(SEL_FIRST, SEL_LAST)
            editor.insert(INSERT, ans)        
    def capitalize():
        chars = {"a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ"}
        text = editor.get(SEL_FIRST, SEL_LAST)    
        check = 0
        for i in list(chars.keys()):
            if i in text:
                check = 1
        if check == 1:
            for i in chars:
                text = text.replace(i, chars[i])
        else:
            for i in chars:
                text = text.replace(chars[i], i)
        editor.delete(SEL_FIRST, SEL_LAST)
        editor.insert(INSERT, text)
    def font():
        for i in [note, calc, help_tabs, frameReplace]:
            i.grid_forget()
        frameFont.grid(row=0, column=0, sticky=NSEW)
    def list():
        try:
            text = editor.get(SEL_FIRST, SEL_LAST)
            editor.delete(SEL_FIRST, SEL_LAST)
            if "• " in text:
                editor.insert(INSERT, text.replace("• ", ""))
            else:    
                editor.insert(INSERT, "• " + text.replace("\n", "\n• "))
        except:
            editor.insert(INSERT, "\n• ")
    def line(chars):
        try:
            text = editor.get(SEL_FIRST, SEL_LAST)
            editor.delete(SEL_FIRST, SEL_LAST)
            if chars in text:
                editor.insert(INSERT, text.replace(chars, ""))
            else:    
                for i in text:
                    if chars == "̶":
                        editor.insert(INSERT, chars + i)
                    else:
                        if i == " " or i == "\n" or i == "\t" or i == "\r":
                            editor.insert(INSERT, i)
                        else:
                            editor.insert(INSERT, i + chars)
        except:
            editor.insert(INSERT, chars)
    def sidebar(i):
        menubar.delete(4, 5)
        if i == "h":
            editor.grid(row=0, column=0, sticky=NSEW)
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0, minsize=0)
            sidebar.grid_forget()
            editor.focus_set()
            root.unbind("<Double-Button-1>")
        elif i == "l":
            sidebar.grid(row=0, column=0, sticky=NSEW)
            editor.grid(row=0, column=1, sticky=NSEW)
            root.columnconfigure(0, weight=0, minsize=320)
            root.columnconfigure(1, weight=1)
            root.unbind("<Double-Button-1>")
            menubar.add_cascade(label="Widgets", menu=menuWidgets)
        elif i == "r":
            editor.grid(row=0, column=0, sticky=NSEW)
            sidebar.grid(row=0, column=1, sticky=NSEW)
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0, minsize=320)
            root.unbind("<Double-Button-1>")
            menubar.add_cascade(label="Widgets", menu=menuWidgets)
        else:
            editor.grid_forget()
            sidebar.grid(row=0, column=0, sticky=NSEW)
            root.columnconfigure(0, weight=1)
            root.columnconfigure(1, weight=0, minsize=0)
            root.bind("<Double-Button-1>", lambda i: main.sidebar("h"))
            menubar.add_cascade(label="Widgets", menu=menuWidgets)
    def note():
        for i in [calc, help_tabs, frameReplace, frameFont]:
            i.grid_forget()
        note.grid(row=0, column=0, sticky=NSEW)
        note.focus_set()
    def calculate(option):
        bar.delete(0, END)
        bar.insert(INSERT, option)
    def calculator():
        for i in [note, help_tabs, frameReplace, frameFont]:
            i.grid_forget()
        calc.grid(row=0, column=0, sticky=NSEW)
        bar.focus_set()
    def help():
        for i in [note, calc, frameReplace, frameFont]:
            i.grid_forget()
        help_tabs.grid(row=0, column=0, sticky=NSEW)
    def replace():
        for i in [note, calc, help_tabs, frameFont]:
            i.grid_forget()
        frameReplace.grid(row=0, column=0, sticky=NSEW)
        find.focus_set()
    def length():
        try:
            messagebox.showinfo("Length (selection)", str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get("sel.first", "sel.last").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get("sel.first", "sel.last").split(" "))-1) + " spaces\n" + str(len(editor.get("sel.first", "sel.last").split("\n"))-1) + " lines")
        except:
            messagebox.showinfo("Length (document)", str(len(editor.get("1.0", "end").replace("\n", "").replace("\r", ""))) + " characters\n" + str(len(editor.get(1.0, "end").replace("\n", "").replace("\r", "").replace(" ", ""))) + " characters (no spaces)\n" +str(len(editor.get(1.0, "end").split(" "))-1) + " spaces\n" + str(len(editor.get(1.0, "end").split("\n"))-1) + " lines")

    def theme(bg0, bg1, bg2, fg, abg, afg):
        editor.configure(bg=bg0, fg=fg, insertbackground=fg)
        editor.tag_configure(SEL, background=bg2, foreground=fg)
        for i in ["TButton", "TCombobox", "TEntry", "TFrame", "TLabel", "TNotebook", "TScrollbar"]:
            a.configure(i, background=bg1)
        for i in [menuFile, menuEdit, menuDelete, menuFormat, menuInsert, menuView, menuSidebar, menuWrap, menuWidgets]:
            i.configure(background=bg1, foreground=afg, activebackground=abg, activeforeground=afg)
            a.configure("TLabel", foreground=afg)
    def full_screen():
        global fs
        fs = not fs
        root.attributes("-fullscreen", fs)
    def exit():
        if editor.get(1.0, END) != "\n":
            choice = messagebox.askyesnocancel("BTXTPad","Do you want to save the changes made to this file?")
            if choice == True:
                main.save()
                root.destroy()
            elif choice == False:
                root.destroy()
        else: 
             root.destroy()
    def b3_edit(event):
        menuEdit.tk_popup(event.x_root, event.y_root)
    def b3_options(event):
        menuOptions.tk_popup(event.x_root, event.y_root)
if __name__ == "__main__":
    root = Tk()
    filepath, fs = "", 0
    root.title("BTXTPad")
    root.geometry("800x600")
    a = Style(root)
    try:
        root.iconbitmap("btxtpad.ico")
    except:
        root.iconbitmap("")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.protocol('WM_DELETE_WINDOW', lambda: main.exit())
    menuFile = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuFile.add_command(label="New", command=main.new, accelerator="Ctrl+N")
    menuFile.add_command(label="Open", command=main.open, accelerator="Ctrl+O")
    menuFile.add_command(label="Save", command=main.save, accelerator="Ctrl+S")
    menuFile.add_command(label="Save As", command=main.save_as, accelerator="Ctrl+Shift+S")
    menuFile.add_separator()
    menuFile.add_command(label="Print", command=lambda: os.startfile(filepath, "print"), accelerator="Ctrl+P")
    menuFile.add_command(label="Duplicate", command=main.duplicate, accelerator="Ctrl+D")
    menuFile.add_separator()
    menuFile.add_command(label="Read Mode", command=main.read_mode, accelerator="Ctrl+E")
    menuFile.add_separator()
    menuFile.add_command(label="Exit", command=main.exit, accelerator="Alt+F4")
    menuEdit = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_command(label="Undo", command=lambda: editor.edit_undo(), accelerator="Ctrl+Z")
    menuEdit.add_command(label="Redo", command=lambda: editor.edit_redo(), accelerator="Ctrl+Y")
    menuEdit.add_separator()
    menuEdit.add_command(label="Cut", command=lambda: main.cut(), accelerator="Ctrl+X")
    menuEdit.add_command(label="Copy", command=lambda: main.copy(editor), accelerator="Ctrl+C")
    menuEdit.add_command(label="Paste", command=lambda: editor.insert(INSERT, editor.selection_get(selection='CLIPBOARD')), accelerator="Ctrl+V")
    menuEdit.add_command(label="Select All", command=lambda: editor.tag_add(SEL, 1.0, END), accelerator="Ctrl+A")
    menuEdit.add_separator()
    menuDelete = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_cascade(label="Delete", menu=menuDelete, accelerator="Del")
    menuDelete.add_command(label="Delete", command=lambda: editor.delete(SEL_FIRST, SEL_LAST), accelerator="Del")
    menuDelete.add_command(label="Delete All", command=lambda: editor.delete(1.0, END), accelerator="Shift+Del")
    menuDelete.add_command(label="Keep", command=main.keep, accelerator="Ctrl+K")
    menuDelete.add_separator()
    menuDelete.add_command(label="Before", command=lambda: editor.delete(1.0, editor.index(INSERT)), accelerator="Ctrl+BS")
    menuDelete.add_command(label="After", command=lambda: editor.delete(editor.index(INSERT), END), accelerator="Ctrl+Del")
    menuEdit.add_separator()
    menuEdit.add_command(label="Find", command=main.find_a, accelerator="Ctrl+F")
    menuEdit.add_command(label="Replace", command=main.replace_a, accelerator="Ctrl+R")
    menuEdit.add_command(label="Go To", command=main.go_to_a, accelerator="Ctrl+G")
    menuEdit.add_separator()
    menuFormat = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuEdit.add_cascade(label="Format", menu=menuFormat, accelerator="F10")
    menuFormat.add_command(label="Capitalize", command=main.capitalize, accelerator="Ctrl+B")
    menuFormat.add_command(label="Font", command=main.font_a, accelerator="Ctrl+T")
    menuFormat.add_separator()
    menuFormat.add_command(label="List", command=main.list, accelerator="F9")
    menuFormat.add_command(label="Underline", command=lambda: main.line("̲"), accelerator="Ctrl+U")
    menuFormat.add_command(label="Double Underline", command=lambda: main.line("̳"), accelerator="Ctrl+Shift+U")
    menuFormat.add_command(label="Strikethrough", command=lambda: main.line("̶"), accelerator="Ctrl+Shift+X")
    menuInsert = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuInsert.add_command(label="Calendar (year)", command=lambda: editor.insert(INSERT, str(calendar.calendar(int(datetime.datetime.now().year)))))
    menuInsert.add_command(label="Calendar (month)", command=lambda: editor.insert(INSERT, str(calendar.month(int(datetime.datetime.now().year), int(datetime.datetime.now().month)))))
    menuInsert.add_separator()
    menuInsert.add_command(label="Date & Time", command=lambda: editor.insert(INSERT, datetime.datetime.now()))
    menuInsert.add_command(label="Week Number", command=lambda: editor.insert(INSERT, "Week " + str(int(datetime.datetime.now().isocalendar().week))))
    menuInsert.add_separator()
    menuInsert.add_command(label="Finance", command=lambda: editor.insert(INSERT, "\t\tIncome\t\tCost\t\tSavings\nJanuary\t\t\t\t\t\t\nFebruary\t\t\t\t\t\t\nMarch\t\t\t\t\t\t\nApril\t\t\t\t\t\t\nMay\t\t\t\t\t\t\nJune\t\t\t\t\t\t\nJuly\t\t\t\t\t\t\nAugust\t\t\t\t\t\t\nSeptember\t\t\t\t\t\t\nOctober\t\t\t\t\t\t\nNovember\t\t\t\t\t\t\nDecember\t\t\t\t\t\t\n------------------------------------------------------------\nTotal\t\t\t\t\t\t"))
    menuInsert.add_command(label="RSS Feed", command=lambda: editor.insert(INSERT, html.unescape("\n".join(re.findall(r'<title>(.*?)</title>', urlopen(simpledialog.askstring("BTXTPad", "Feed URL")).read().decode("utf8")))).replace("<![CDATA[", "").replace("]]>", "")))
    menuView = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuSidebar = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuView.add_cascade(label="Sidebar", menu=menuSidebar)
    menuSidebar.add_command(label="Hide", command=lambda: main.sidebar("h"), accelerator="Ctrl+,")
    menuSidebar.add_command(label="Left", command=lambda: main.sidebar("l"), accelerator="Ctrl+.")
    menuSidebar.add_command(label="Right", command=lambda: main.sidebar("r"), accelerator="Ctrl+/")
    menuSidebar.add_separator()
    menuSidebar.add_command(label="Maximize", command=lambda: main.sidebar("m"), accelerator="Ctrl+M")
    menuView.add_separator()
    menuView.add_command(label="Length", command=main.length, accelerator="F2")
    menuView.add_command(label="Clipboard", command=lambda: messagebox.showinfo("Clipboard", editor.selection_get(selection="CLIPBOARD")), accelerator="F8")
    menuWrap = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuView.add_cascade(label="Wrap", menu=menuWrap)
    menuWrap.add_command(label="Disabled", command=lambda: editor.configure(wrap=NONE))
    menuWrap.add_command(label="Word", command=lambda: editor.configure(wrap=WORD))
    menuWrap.add_command(label="Character", command=lambda: editor.configure(wrap=CHAR))
    menuView.add_separator()
    menuTheme = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuView.add_cascade(label="Theme", menu=menuTheme)
    menuTheme.add_command(label="Aa", command=lambda: main.theme("#fff", "#f0f0f0", "#e0e0e0", "#000", "#e0e0e0", "#000"), background="#fff", foreground="#000", activebackground="#080", activeforeground="#fff")
    menuTheme.add_command(label="Aa", command=lambda: main.theme("#dcb", "#f0f0f0", "#bead9c", "#000", "#e0e0e0", "#000"), background="#dcb", foreground="#000", activebackground="#080", activeforeground="#fff")
    menuTheme.add_command(label="Aa", command=lambda: main.theme("#222", "#222", "#505050", "#fff", "#444", "#fff"), background="#222", foreground="#fff", activebackground="#080", activeforeground="#fff")
    menuTheme.add_command(label="Aa", command=lambda: main.theme("#000", "#222", "#2e2e2e", "#fff", "#444", "#fff"), background="#000", foreground="#fff", activebackground="#080", activeforeground="#fff")
    menuView.add_command(label="Full Screen", command=main.full_screen, accelerator="F11")
    menubar = Menu(root, tearoff=False)
    root.config(menu=menubar)
    menubar.add_cascade(label="File", menu=menuFile)
    menubar.add_cascade(label="Edit", menu=menuEdit)
    menubar.add_cascade(label="Insert", menu=menuInsert)
    menubar.add_cascade(label="View", menu=menuView)
    editor = scrolledtext.ScrolledText(root, bd=16, relief=FLAT, undo=True, wrap=WORD, font=("Consolas", 11, "normal"))
    editor.grid(row=0, column=0, sticky=NSEW)
    menuWidgets = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuWidgets.add_command(label="Note", command=main.note)
    menuWidgets.add_command(label="Calculator", command=main.calculator)
    menuWidgets.add_separator()
    menuWidgets.add_command(label="Replace", command=main.replace)
    menuWidgets.add_command(label="Font", command=main.font)
    menuWidgets.add_separator()
    menuWidgets.add_command(label="Help", command=main.help)
    sidebar = Frame(root)
    sidebar.rowconfigure(0, weight=1)
    sidebar.columnconfigure(0, weight=1)
    note = Text(sidebar, bd=16, relief=FLAT, undo=True, background="#fc5", foreground="#000", font=("Consolas", 11), width=36)
    menuOptions = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuOptions.add_command(label="Editor >> Note", command=lambda: note.insert(END, editor.get(1.0, END)))
    menuOptions.add_command(label="Note >> Editor", command=lambda: editor.insert(END, note.get(1.0, END)))
    menuOptions.add_command(label="Save As", command=lambda: open(filedialog.asksaveasfilename(defaultextension=".btxt", filetypes=[("All Files", "*.*")]), "w").write(str(datetime.datetime.now().date())+"\n\n"+note.get(1.0, END)))
    menuOptions.add_separator()
    menuOptions.add_command(label="Undo", command=note.edit_undo)
    menuOptions.add_command(label="Redo", command=note.edit_redo)
    menuOptions.add_command(label="Copy", command=lambda: main.copy(note))
    menuOptions.add_command(label="Delete All", command=lambda: note.delete(1.0, END))
    menuOptions.add_separator()
    menuColor = Menu(root, tearoff=False, activeborderwidth=2.5)
    menuOptions.add_cascade(label="Color", menu=menuColor)
    menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#fc5"), background="#fc5", foreground="#000", activebackground="#000", activeforeground="#fff")
    menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#5cf"), background="#5cf", foreground="#000", activebackground="#000", activeforeground="#fff")
    menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#d8d"), background="#d8d", foreground="#000", activebackground="#000", activeforeground="#fff")
    menuColor.add_command(label="Aa", command=lambda: note.configure(bg="#8d8"), background="#8d8", foreground="#000", activebackground="#000", activeforeground="#fff")
    calc = Frame(sidebar, width=36)
    calc.rowconfigure(1, weight=1)
    calc.columnconfigure(0, weight=1, minsize=320)
    bar = Entry(calc, font=("", 12))
    bar.grid(row=0, column=0, sticky=NSEW, ipady=8)
    frameCalculator = Frame(calc)
    frameCalculator.grid(row=1, column=0, sticky=NSEW)
    for i in range(0, 6):
        frameCalculator.rowconfigure(i, weight=1)
    for j in range(0, 4):
        frameCalculator.columnconfigure(j, weight=1)
    Button(frameCalculator, text="bin", command=lambda: main.calculate(str(bin(int(eval(bar.get())))))).grid(row=0, column=0, sticky=NSEW)
    Button(frameCalculator, text="oct", command=lambda: main.calculate(str(oct(int(eval(bar.get())))))).grid(row=0, column=1, sticky=NSEW)
    Button(frameCalculator, text="hex", command=lambda: main.calculate(str(hex(int(eval(bar.get())))))).grid(row=0, column=2, sticky=NSEW)
    Button(frameCalculator, text="^", command=lambda: bar.insert(INSERT, " ** ")).grid(row=0, column=3, sticky=NSEW)
    Button(frameCalculator, text="x²", command=lambda: main.calculate(str(eval(bar.get()) ** 2))).grid(row=1, column=0, sticky=NSEW)
    Button(frameCalculator, text="√", command=lambda: main.calculate(str(math.sqrt(eval(bar.get()))))).grid(row=1, column=1, sticky=NSEW)
    Button(frameCalculator, text="1/x", command=lambda: main.calculate(str(1/float(eval(bar.get()))))).grid(row=1, column=2, sticky=NSEW)
    Button(frameCalculator, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=1, column=3, sticky=NSEW)
    Button(frameCalculator, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=2, column=0, sticky=NSEW)
    Button(frameCalculator, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=2, column=1, sticky=NSEW)
    Button(frameCalculator, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=2, column=2, sticky=NSEW)
    Button(frameCalculator, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=2, column=3, sticky=NSEW)
    Button(frameCalculator, text="4", command=lambda: bar.insert(INSERT, "4")).grid(row=3, column=0, sticky=NSEW)
    Button(frameCalculator, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=3, column=1, sticky=NSEW)
    Button(frameCalculator, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=3, column=2, sticky=NSEW)
    Button(frameCalculator, text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=3, column=3, sticky=NSEW)
    Button(frameCalculator, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=4, column=0, sticky=NSEW)
    Button(frameCalculator, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=4, column=1, sticky=NSEW)
    Button(frameCalculator, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=4, column=2, sticky=NSEW)
    Button(frameCalculator, text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=4, column=3, sticky=NSEW)
    Button(frameCalculator, text="C", command=lambda: bar.delete(0, END)).grid(row=5, column=0, sticky=NSEW)
    Button(frameCalculator, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=5, column=1, sticky=NSEW)
    Button(frameCalculator, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=5, column=2, sticky=NSEW)
    Button(frameCalculator, text="=", command=lambda: main.calculate(eval(bar.get()))).grid(row=5, column=3, sticky=NSEW)
    frameReplace = Frame(sidebar, width=36)
    for i in range(1, 7):
        frameReplace.rowconfigure(i, weight=1)
    frameReplace.columnconfigure(0, weight=1)
    f = Frame(frameReplace, border=16)
    f.grid(row=0, column=0, sticky=NSEW)
    f.columnconfigure(1, weight=1)
    Label(f, text="Find", width=12).grid(row=0, column=0, sticky=EW, ipady=5)
    find = Entry(f)
    find.grid(row=0, column=1, sticky=NSEW)
    Label(f, text="Replace", width=12).grid(row=1, column=0, sticky=EW, ipady=5)
    replace = Entry(f)
    replace.grid(row=1, column=1, sticky=NSEW)
    Label(f, text="Line", width=12).grid(row=2, column=0, sticky=EW, ipady=5)
    ln = Entry(f)
    ln.grid(row=2, column=1, sticky=NSEW)
    ln.insert(INSERT, str(editor.index(INSERT)).split(".")[0])
    Label(f, text="Colunn", width=12).grid(row=3, column=0, sticky=EW, ipady=5)
    col = Entry(f)
    col.grid(row=3, column=1, sticky=NSEW)
    col.insert(INSERT, str(editor.index(INSERT)).split(".")[1])
    Button(frameReplace, text="Find", command=lambda: main.find_next(find.get())).grid(row=1, column=0, sticky=NSEW)
    Button(frameReplace, text="Replace", command=lambda: main.replace_next(find.get(), replace.get())).grid(row=2, column=0, sticky=NSEW)
    Button(frameReplace, text="Replace All", command=lambda: main.replace_all(find.get(), replace.get())).grid(row=3, column=0, sticky=NSEW)
    Button(frameReplace, text="Delete", command=lambda: main.replace_next(find.get(), "")).grid(row=4, column=0, sticky=NSEW)
    Button(frameReplace, text="Solve", command=main.solve).grid(row=5, column=0, sticky=NSEW)
    Button(frameReplace, text="Go To", command=main.go_to).grid(row=6, column=0, sticky=NSEW)
    frameFont = Frame(sidebar, width=36, border=16)
    frameFont.columnconfigure(0, weight=1)
    Label(frameFont, font=("Segoe UI", 12), text="Font Family").grid(row=0, column=0, sticky="nsew")
    font_family = Combobox(frameFont, values=font.families())
    font_family.grid(row=1, column=0, sticky="ew")
    font_family.insert(INSERT, "Consolas")
    Label(frameFont, font=("Segoe UI", 12), text="\nSize").grid(row=2, column=0, sticky="nsew")
    size = Combobox(frameFont, values=("8", "9", "10", "11", "12", "14", "16", "18", "20", "22", "24", "26", "28", "36", "48", "72"))
    size.grid(row=3, column=0, sticky="ew")
    size.insert(INSERT, "11")
    Label(frameFont, font=("Segoe UI", 12), text="\nStyle").grid(row=4, column=0, sticky="nsew")
    style = Combobox(frameFont, values=("normal", "bold", "italic", "bold italic", "underline", "bold underline", "italic underline", "bold italic underline", "overstrike", "bold overstrike", "italic overstrike", "bold italic overstrike", "underline overstrike", "bold underline overstrike", "italic underline overstrike", "bold italic underline overstrike"))
    style.grid(row=5, column=0, sticky="ew")
    style.insert(INSERT, "normal")
    Label(frameFont, font=("Segoe UI", 12)).grid(row=6, column=0, sticky="nsew")
    action_button = Button(frameFont, text="OK", command=lambda: editor.configure(font=(font_family.get(), int(size.get()), style.get())))
    action_button.grid(row=7, column=0, sticky=NSEW)
    help_tabs = Notebook(sidebar, width=320)
    about = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
    about.insert(INSERT, f"BTXTPad - A text editor\nCopyright (C) 2022-{str(datetime.datetime.now().year)}: Waylon Boer\n\nBTXTPad is a simple text editor. BTXTPad has some additional features, for example a sidebar. The default file format is .btxt, but BTXTPad can also edit other plain text files. There is also a standalone notetaking app available: BTXTPad Note.\n\nThank you for using BTXTPad!")
    about.configure(state=DISABLED)
    help_tabs.add(about, text="About")
    mit_license = Text(help_tabs, relief=FLAT, border=16, font=("Consolas", 11), wrap=WORD, background="#dcb")
    mit_license.insert(INSERT, """Copyright (c) 2022 Waylon Boer\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR a PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.""")
    mit_license.configure(state=DISABLED)
    help_tabs.add(mit_license, text="License")
    main.theme("#fff", "#f0f0f0", "#e0e0e0", "#000", "#e0e0e0", "#000")
    main.note()
    editor.focus_set()
    editor.bind("<Control-b>", lambda i: main.capitalize())
    editor.bind("<Control-B>", lambda i: main.capitalize())
    editor.bind("<Control-d>", lambda i: main.duplicate())
    editor.bind("<Control-D>", lambda i: main.duplicate())
    editor.bind("<Control-e>", lambda i: main.read_mode())
    editor.bind("<Control-E>", lambda i: main.read_mode())
    root.bind("<Control-f>", lambda i: main.find_a())
    root.bind("<Control-F>", lambda i: main.find_a())
    root.bind("<Control-g>", lambda i: main.go_to_a())
    root.bind("<Control-G>", lambda i: main.go_to_a())
    editor.bind("<Control-k>", lambda i: main.keep())
    editor.bind("<Control-K>", lambda i: main.keep())
    editor.bind("<Control-l>", lambda i: main.length())
    editor.bind("<Control-L>", lambda i: main.length())
    root.bind("<Control-m>", lambda i: main.sidebar("m"))
    root.bind("<Control-M>", lambda i: main.sidebar("m"))
    editor.bind("<Control-n>", lambda i: main.new())
    editor.bind("<Control-N>", lambda i: main.new())
    editor.bind("<Control-o>", lambda i: main.open())
    editor.bind("<Control-O>", lambda i: main.open())
    editor.bind("<Control-s>", lambda i: main.save())
    editor.bind("<Control-S>", lambda i: main.save())
    editor.bind("<Control-Shift-s>", lambda i: main.save_as())
    editor.bind("<Control-Shift-S>", lambda i: main.save_as())
    root.bind("<Control-t>", lambda i: main.font_a())
    root.bind("<Control-T>", lambda i: main.font_a())
    editor.bind("<Control-p>", lambda i: os.startfile(filepath, "print"))
    editor.bind("<Control-P>", lambda i: os.startfile(filepath, "print"))
    root.bind("<Control-r>", lambda i: main.replace_a())
    root.bind("<Control-R>", lambda i: main.replace_a())
    editor.bind("<Control-u>", lambda i: main.line("̲"))
    editor.bind("<Control-U>", lambda i: main.line("̲"))
    editor.bind("<Control-Shift-u>", lambda i: main.line("̳"))
    editor.bind("<Control-Shift-U>", lambda i: main.line("̳"))
    root.bind("<Control-w>", lambda i: main.exit())
    root.bind("<Control-W>", lambda i: main.exit())
    editor.bind("<Control-Shift-x>", lambda i: main.line("̶"))
    editor.bind("<Control-Shift-X>", lambda i: main.line("̶"))
    root.bind("<Control-,>", lambda i: main.sidebar("h"))
    root.bind("<Control-.>", lambda i: main.sidebar("l"))
    root.bind("<Control-/>", lambda i: main.sidebar("r"))
    editor.bind("<Shift-Delete>", lambda i: editor.delete(1.0, END))
    editor.bind("<Control-BackSpace>", lambda i: editor.delete(1.0, editor.index(INSERT)))
    editor.bind("<Control-Delete>", lambda i: editor.delete(editor.index(INSERT), END))
    root.bind("<Insert>", lambda i: editor.insert(INSERT, editor.selection_get(selection="CLIPBOARD")))
    root.bind("<F1>", lambda i: main.help_a())
    root.bind("<F2>", lambda i: main.length())
    root.bind("<F3>", lambda i: main.find_a())
    root.bind("<F5>", lambda i: main.open())
    root.bind("<F6>", lambda i: main.font())
    editor.bind("<F7>", lambda i: main.read_mode())
    root.bind("<F8>", lambda i: messagebox.showinfo("Clipboard", editor.selection_get(selection="CLIPBOARD")))
    root.bind("<F9>", lambda i: main.list())
    editor.bind("<F10>", lambda i: menuFormat.tk_popup(editor.winfo_rootx()+16, editor.winfo_rooty()+16))
    note.bind("<F10>", lambda i: menuOptions.tk_popup(note.winfo_rootx()+16, note.winfo_rooty()+16))
    root.bind("<F11>", lambda i: main.full_screen())
    root.bind("<F12>", lambda i: main.save_as())
    root.bind("<Control-[>", lambda i: main.theme("#fff", "#f0f0f0", "#ddd", "#000", "#e0e0e0", "#000"))
    root.bind("<Control-]>", lambda i: main.theme("#dcb", "#f0f0f0", "#bead9c", "#000", "#e0e0e0", "#000"))
    root.bind("<Control-;>", lambda i: main.theme("#222", "#222", "#505050", "#fff", "#444", "#fff"))
    root.bind("<Control-'>", lambda i: main.theme("#000", "#222", "#2e2e2e", "#fff", "#444", "#fff"))
    editor.bind("<KeyPress>", lambda i: main.refresh_lc(ln, col))
    editor.bind("<ButtonRelease>", lambda i: main.refresh_lc(ln, col))
    editor.bind("<Button-3>", main.b3_edit)
    note.bind("<Button-3>", main.b3_options)
    bar.bind("<Return>", lambda i: main.calculate(eval(bar.get())))
    font_family.bind("<Return>", lambda i: editor.configure(font=(font_family.get(), int(size.get()), style.get())))
    size.bind("<Return>", lambda i: editor.configure(font=(font_family.get(), int(size.get()), style.get())))
    style.bind("<Return>", lambda i: editor.configure(font=(font_family.get(), int(size.get()), style.get())))
    root.mainloop()
