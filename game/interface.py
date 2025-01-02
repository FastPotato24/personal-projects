import keyboard
import rich
import os
import time
from rich.layout import Layout
from rich.panel import Panel
import game.mechanics as mechanics

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class ListMenu:
    def __init__(self, options, title=None, max_per_page=10):
        self.options = list(options)
        self.index = 0
        self.page = 0
        self.max_per_page = max_per_page
        self.pages = (len(self.options) + self.max_per_page - 1) // self.max_per_page
        self.title = title
        self.selected = None

    def renderable(self):
        self.optionstr = ""
        max_length = max(len(s) for s in self.options)
        for index, option in enumerate(self.options[self.page * self.max_per_page:self.page * self.max_per_page + self.max_per_page]):
            if index == self.index:
                self.optionstr += f"[reverse]{option.ljust(max_length)}[/]"
            else:
                self.optionstr += option.ljust(max_length)
            self.optionstr += "\n" if index != self.max_per_page - 1 else ""
        return Panel.fit(self.optionstr, padding=(0, 1), title=self.title, subtitle=f"Page {self.page + 1}/{self.pages}" if self.pages > 1 else None)

    def input(self, key=None):
        key = key or keyboard.read_key()
        if key == 'down':
            self.index += 1
            if self.index >= self.max_per_page or self.index >= len(self.options) - self.page * self.max_per_page:
                self.index = 0
        elif key == 'up':
            self.index -= 1
            if self.index < 0:
                self.index = min(self.max_per_page, len(self.options) - self.page * self.max_per_page) - 1
        elif key == 'right' and self.pages > 1:
            self.page += 1
            if self.page >= self.pages:
                self.page = 0
            self.index = 0
        elif key == 'left' and self.pages > 1:
            self.page -= 1
            if self.page < 0:
                self.page = self.pages - 1
            self.index = 0
        elif key in ['enter', 'space', 'right']:
            self.selected = self.index + self.page * self.max_per_page
            return 1  # Exit Code: 1 (Next)
        elif key in ['esc', 'q', 'left']:
            return -1  # Exit Code: -1 (Back)
        return self.renderable()

class Interface:
    def __init__(self, entity: mechanics.Entity):
        self.layout = Layout()
        self.entity = entity
        self.layout.split(
            Layout(name="spacer", size=1),
            Layout(name="main", ratio=2),
            Layout(name="console", ratio=1),
        )
        self.layout["main"].split_row(
            Layout(name="category"),
            Layout(name="items"),
            Layout(name="description", ratio=2),
        )
        self.dynamic = {
            "category": ListMenu(["All", "Weapons", "Apparel", "Consumables", "Junk", "Misc"], title="Category"),
            "items": NotImplementedError,
            "description": NotImplementedError,
            "console": NotImplementedError,
        }
        
        for key, value in self.dynamic.items():
            if value != NotImplementedError:
                self.layout[key].update(value.renderable())
        self.update()
        self.active = "category"
        while True:
            temp = self.dynamic[self.active].input()
            if temp not in [1, -1]:
                self.update(self.active, temp)
            elif temp == 1:
                self.active = "items"
            elif temp == -1:
                self.active = "category"
            time.sleep(0.1)
            
    def update(self, key=None, value=None):
        clear()
        if key and value:
            self.layout[key].update(value)
        rich.print(self.layout)