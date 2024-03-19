import os

class Terminal:
    __width = os.get_terminal_size()[0]
    __height = os.get_terminal_size()[1]

    @staticmethod
    def get_width(): return Terminal.__width
    
    @staticmethod
    def get_height(): return Terminal.__height
    
    @staticmethod
    def set_width(w): Terminal.__width = w
    
    @staticmethod
    def set_height(h): Terminal.__height = h

    @staticmethod
    def refresh_size():
        Terminal.__width = os.get_terminal_size()[0]
        Terminal.__height = os.get_terminal_size()[1]

    #resize terminal emulation only
    @staticmethod
    def resize(w, h):
        Terminal.set_width(w)
        Terminal.set_height(h)
        os.system("resize -s " +str(Terminal.__height)+ " " +str(Terminal.__width))

    @staticmethod
    def clear(): os.system("clear")