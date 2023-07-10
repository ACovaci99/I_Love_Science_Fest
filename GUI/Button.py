import tkinter as tk



DEFAULT_FONT_NAME = "َAndale Mono"
DEFAULT_FONT_SIZE = 15
DEFAULT_FONT_STYLE = ""

DEFAULT_WIDTH = 7
DEFAULT_HIGHT = 1
class myButton:

    def __init__(self, father, btnRow, btnColumn, btnAction, btnText = None, rowSpan = None,
                 columnspan = None, btnFont = (DEFAULT_FONT_NAME,DEFAULT_FONT_SIZE,DEFAULT_FONT_STYLE),
                 bgColor = "#ffffff", fgColor = "#000000", width = DEFAULT_WIDTH):
        myButton = tk.Button(father, text=btnText, font = btnFont, bg=bgColor, fg=fgColor, width = width, height = DEFAULT_HIGHT, command=btnAction)
        myButton.grid(row = btnRow, column=btnColumn, columnspan = columnspan, padx= 0, pady= 0)
        myButton.bind("<Enter>", lambda x: myButton.config(bg="#FF6E14"))
        myButton.bind("<Leave>", lambda x: myButton.config(bg=bgColor))
        




