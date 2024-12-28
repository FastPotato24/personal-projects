import keyboard
import rich
import os
import time
from rich.layout import Layout
from rich.panel import Panel

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
       
class ListMenu:
    def __init__(self, options, title=None, max_per_page=10):
        self.options = list(options)
        self.index = 0
        self.page = 0
        self.pages = len(self.options) // max_per_page
        # Acts as a the max index for the current page
        self.max_per_page = max_per_page if len(self.options) > max_per_page else len(self.options)
        self.title = title
    def renderable(self):
        self.optionstr = ""
        for index, option in enumerate(self.options[self.page * self.max_per_page:self.page * self.max_per_page + self.max_per_page]):
            self.optionstr += f"[reverse]{option}[/]" if index == self.index else option
            self.optionstr += "\n" if index != self.max_per_page - 1 else ""
        return Panel.fit(self.optionstr, padding=(0, 1), title=self.title, subtitle=f"Page {self.page + 1}/{self.pages}" if self.pages > 1 else None)
    def input(self):
        while True:
            clear()
            rich.print(self.renderable())
            event = keyboard.read_key()
            if event == 'down':
                self.index += 1
                self.index %= self.max_per_page
            elif event == 'up':
                self.index -= 1
                self.index %= self.max_per_page
            elif event == 'right':
                self.page += 1
                self.page %= self.pages
            elif event == 'left':
                self.page -= 1
                self.page %= self.pages
            elif event in ['enter', 'space']:
                return self.index + self.page * self.max_per_page
            elif event == 'esc':
                # Exit Code: -1
                return -1
            time.sleep(0.1)

test = ListMenu([f"Option {i+1}" for i in range(10)], title="Test Menu")
print(test.options[test.input()])