from pycli_terminal import Terminal
from pycli_convert import Convert
from pycli_style import Style
from pycli_write import Write
from pycli_draw import Draw

class Pycli:
    #Consider TTY character with size 8x16
    
    #sub classes of Pycli
    class Terminal(Terminal): pass
    class Convert(Convert): pass
    class Style(Style): pass
    class Write(Write): pass
    class Draw(Draw): pass