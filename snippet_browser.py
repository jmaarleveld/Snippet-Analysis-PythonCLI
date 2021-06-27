import collections
import json

import kivy
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'borderless', '0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.codeinput import CodeInput
from pygments.lexers.jvm import JavaLexer


OUTPUT = {'nonterminals': {}, 'results': {}}


Builder.load_string("""
<SnippetBrowser>:
    code_window: code_window
    drop_down_x: drop_down
    next_button: next_button
    prev_button: prev_button
    input_field: input_field 
    goto_btn: goto_btn 
    current: current 
    orientation: "horizontal"
    BoxLayout:
        id: code_window
        size_hint: .8, 1
    BoxLayout:
        size_hint: .2, 1
        orientation: "vertical"
        Button:
            id: drop_down
            size_hint: 1, .25
        BoxLayout:
            orientation: "horizontal"
            size_hint: 1, .25
            Button:
                id: prev_button
                size_hint: .5, 1
                text: "Previous"
            Button:
                id: next_button
                size_hint: .5, 1
                text: "Next"
        BoxLayout:
            orientation: "horizontal"
            size_hint: 1, .25
            TextInput:
                id: input_field
                size_hint: .5, 1
                multiline: False 
            Button:
                id: goto_btn
                size_hint: .5, 1
                text: "Goto"
        Label:
            id: current  
            size_hint: 1, .2
""")


class CustomCodeInput(CodeInput):
    """Make the scrolling in the code window faster"""

    SCROLL_MULTIPLIER = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__cached_scroll_y = 0

    def on_scroll_y(self, instance, value):
        if abs(self.__cached_scroll_y - value) == 20:
            dy = value - self.__cached_scroll_y
            self.__cached_scroll_y += self.SCROLL_MULTIPLIER * dy
            self.scroll_y = self.__cached_scroll_y


class SnippetBrowser(BoxLayout):
    code_window = ObjectProperty()
    drop_down_x = ObjectProperty()
    next_button = ObjectProperty()
    prev_button = ObjectProperty()
    input_field = ObjectProperty()
    goto_btn = ObjectProperty()
    current = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code_input = None
        self.__out = {}
        self.drop_down = None
        self.__index = -1
        self.__sel = -1
        self.__map = {}
        self.__rev_map = {}
        self.__info = {}

    def populate(self):
        self.code_input = CustomCodeInput(lexer=JavaLexer())
        print(self.code_input.__class__.__mro__)
        for x in self.code_input.__class__.__mro__:
            print(x, hasattr(x, 'scroll_y'))
        self.code_window.add_widget(self.code_input)
        self.__map = OUTPUT['nonterminals']
        self.__rev_map = {v: k for k, v in self.__map.items()}
        self.__out = collections.defaultdict(list)
        self.__info = collections.defaultdict(list)
        for _, obj in OUTPUT['results'].items():
            #classification, source, _ = obj.values()
            self.__out[obj['classification']].append(obj['source'])
            self.__info[obj['classification']].append(obj['uses_custom'])
        self.drop_down = DropDown(auto_dismiss=False)
        for x in sorted(self.__out, key=int):
            btn = Button(text=self.__map[x],
                         on_release=lambda b: self.drop_down.select(b.text),
                         height=44,
                         size_hint_y=None)
            self.drop_down.add_widget(btn)
        self.drop_down_x.bind(on_press=self.drop_down.open)
        self.drop_down_x.text = 'Select'
        self.drop_down.bind(on_select=lambda instance, y: self._select(y))

        self.next_button.bind(on_press=self._next)
        self.prev_button.bind(on_press=self._prev)
        self.goto_btn.bind(on_press=self._exec_goto)

    def _goto(self):
        self.code_input.text = self.__out[self.__sel][self.__index]
        info = f'(uses_custom={self.__info[self.__sel][self.__index]})'
        self.current.text = f'{self.__index + 1} / {len(self.__out[self.__sel])}\n{info}'
        self._fix_window()

    def _select(self, x):
        self.drop_down_x.text = x
        self.__sel = self.__rev_map[x]
        self.__index = 0
        self._goto()

    def _next(self, _):
        self.__index += 1
        try:
            self._goto()
        except IndexError:
            self.__index -= 1

    def _prev(self, _):
        if self.__index == 0:
            return
        self.__index -= 1
        try:
            self._goto()
        except IndexError:
            self.__index += 1

    def _exec_goto(self, _):
        if not self.input_field.text:
            return
        self.__index = int(self.input_field.text)
        self._goto()

    def _fix_window(self):
        self.code_input.cursor = (0, 0)


class SnippetBrowserApp(App):

    def build(self):
        instance = SnippetBrowser()
        instance.populate()
        return instance


def set_result(r):
    global OUTPUT
    OUTPUT = r


def run_app():
    SnippetBrowserApp().run()


