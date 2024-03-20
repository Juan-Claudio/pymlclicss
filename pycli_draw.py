from pycli_write import Write
from pycli_style import Style

import math

class Draw:
    @staticmethod
    def screen(screenString): print(screenString, end='')

    @staticmethod
    def horizontal(x,y,w, char='─', style=''):
        line = char*w
        return Write.leftAt(x,y,line,style)

    @staticmethod
    def vertical(x,y,h, char='│', style=''):
        line = ''
        for i in range(0,h):
            line += Style.position(x,y+i)
            line += Write.piece(char, style)
        return Write.leftAt(x,y,line,style)

    @staticmethod
    def desgonal(x,y,size, char="╲", center=False, style=''):
        line = ''
        if center == True:
            center = "╳"
        if center != False and size%2==0:
            center = False
        for i in range(0,size):
            line += Style.position(x+i,y+i)
            if(center is not False and i == (size-1)//2):
                line += Write.piece(center, style)
            else:
                line += Write.piece(char, style)
        return Write.leftAt(x,y,line,style)

    @staticmethod
    def asgonal(x,y,size, char="╱", center=False, style=''):
        x+=size-1
        line = ''
        if center == True:
            center = "╳"
        if center != False and size%2==0:
            center = False
        for i in range(0,size):
            line += Style.position(x-i,y+i)
            if(center is not False and
                i == (size-1)//2):
                line += Write.piece(center, style)
            else:
                line += Write.piece(char, style)
        return Write.leftAt(x,y,line,style)

    def rectdesgonal(x,y,w,h, char="●", style=''):
        def roundSup(number):
            decPart = number-math.floor(number)
            if(decPart>=0.5):
                return math.ceil(number)
            return math.floor(number)
        
        stepY = w/h if h>w else 1
        stepX = h/w if w>h else 1
        step = stepY if h>w else stepX
        maxi = h if h>w else w
        line = ''
        for i in range(0,maxi):
            curr_x = x+roundSup(stepY*i)
            curr_y = y+roundSup(stepX*i)
            if curr_x >= x+w or curr_y>= y+h:
                break
            line += Style.position(curr_x,curr_y)
            line += Write.piece(char, style)
        return line

    #TODO rectasgonal(x,y,w,h, char="*", style='')
    
    # char -> repeated char use to draw rectangle sides
    # list(topleft,topright,bottomleft,bottomright,horizontal,vertical)
    @staticmethod
    def rectangle(x, y, w, h, char:list=['┌','┐','└','┘','─','│'],style=''):
        rect = ''
        if len(char)>=0 and len(char)<6:
            pattern = " " if len(char)==0 else char[0]
            char = []
            for i in range(0,6):
                char.append(pattern)
        elif len(char)!=6:
            raise ValueError("Error in param 5, must be list(len<7) of string")
        
        horizontal = char[4]*(w-2)
        rect = Style.position(x,y)
        y+=1
        #top of rectangle
        rect += Write.piece(char[0]+horizontal+char[1],style)
        #verticals of rectangles
        for i in range(0,h-2):
            #draw pattern left at position x,y
            rect += Style.position(x,y)
            rect += Write.piece(char[5],style)
            #ajust position for next pattern
            x += w-1
            #draw second pattern of line
            rect += Style.position(x,y)
            rect += Write.piece(char[5],style)
            #adjust coordinate for next line
            x -= w-1
            y += 1
        rect += Style.position(x,y)
        return rect + Write.piece(char[2] + horizontal + char[3],style)

    @staticmethod
    def rectback(x, y, w, h, color):
        rectbg = ''
        for i in range(0,h):
            rectbg += Style.position(x,y+i)
            rectbg += Write.piece(' '*w, color)
        
        return rectbg
    
    @staticmethod
    #border-fg/bg and bg:str color name like 'red', 'blue'...
    def rect(x=0,y=0,w=0,h=0, border_style=None, border_fg=None, border_bg=None, bg=None):
        #if rect has no height or no width don't draw anything
        if w == 0 or h == 0: return
        
        box = ''

        #if exists draw background
        if bg is not None:
            box += Draw.rectback(x, y, w, h, Style.bg(bg))
        
        #draw border if exists
        if border_style is not None:
            style = '' if border_fg is None else Style.fg(border_fg)
            style = style if border_bg is None else style + Style.fg(border_bg)
            box += Draw.rectangle(x, y, w, h, border_style, style)