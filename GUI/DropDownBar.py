import tkinter as tk
import json

class DropDownBar:
    def __init__(self, root, json_data):
        self.root = root
        self.json_data = json_data
        self.selected_value = None
        self.option_menu = None

        # For setting the default value when booting up the drop down
        self.var = tk.StringVar(self.root)
        self.var.set(list(self.json_data.keys())[0])

    def create_dropdown(self):
        self.option_menu = tk.OptionMenu(self.root, self.var, *self.json_data.keys(), command=self._select_item)
        self.option_menu.pack()

    def _select_item(self, selected_label):
        self.selected_value = self.json_data[selected_label]

    def get_selected_value(self):
        return self.selected_value