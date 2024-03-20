import os

#shared terminal size setting
_width, _height = os.get_terminal_size()

class Terminal:

    #getters size
    @staticmethod
    def get_width(): return _width
    @staticmethod
    def get_height(): return _height
    @staticmethod
    def get_size(): return (_width, _height)

    #setters size
    @staticmethod
    def set_width(w):
        global _width
        _width = w
    @staticmethod
    def set_height(h):
        global _height
        _height = h
    @staticmethod
    def set_size(w,h):
        Terminal.set_width(w)
        Terminal.set_height(h)

    @staticmethod
    def refresh_size():
        global _width, _height
        _width, _height = os.get_terminal_size()

    #resize terminal emulation only (and not in full screen)
    @staticmethod
    def resize(w=None, h=None):
        if w is None and h is None: return
        elif w is None:
            Terminal.set_height(h)
        else:
            Terminal.set_width(w)
        
        os.system(f"resize -s {Terminal.get_height()} {Terminal.get_width()} > /dev/null 2>&1")

    @staticmethod
    def clear(): os.system("clear")