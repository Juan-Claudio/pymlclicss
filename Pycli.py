import os
import re
import sys
import math

class Pycli:
    #Consider TTY character with size 8x16
    __width = os.get_terminal_size()[0]
    __height = os.get_terminal_size()[1]

    @staticmethod
    def get_size():
        w = Pycli.__width
        if w < 60:
            return 'xs'
        elif w >= 60:
            return 's'
        elif w >= 120:
            return 'm'
        elif w >= 180:
            return 'l'
        elif w >= 240:
            return 'xl'
        elif w >= 300:
            return 'xxl'
        

    @staticmethod
    def get_width():
        return Pycli.__width
    
    @staticmethod
    def get_height():
        return Pycli.__height
    
    @staticmethod
    def set_width(w):
        Pycli.__width = w
    
    @staticmethod
    def set_height(h):
        Pycli.__height = h

    @staticmethod
    def refresh_size():
        Pycli.__width = os.get_terminal_size()[0]
        Pycli.__height = os.get_terminal_size()[1]

    #resize terminal emulation only
    @staticmethod
    def resize(w, h):
        Pycli.set_width(w)
        Pycli.set_height(h)
        os.system("resize -s " +str(Pycli.__height)+ " " +str(Pycli.__width))
    
    @staticmethod
    def clear():
        os.system("clear")

    @staticmethod
    def color(clr_num) -> str:
        return "\033["+str(clr_num)+"m"

    @staticmethod
    def position(x,y):
        x += 1
        y += 1
        return f"\033[{y};{x}f"

    @staticmethod
    def clearf():
        return "\033[0m"

	#returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def percent(wOrH, nb, roundInf=True):
        if(wOrH in ['w','col','cols','width','column','columns']):
            wOrH = Pycli.__width
        elif(wOrH in ['h','row','rows','height']):
            wOrH = Pycli.__height
        elif(type(wOrH) == int):
            pass
        else:
            raise ValueError('No recognise number of cols or rows to calculate percent from.')

        nbColRow = (wOrH*nb)//100
        nbRemaining = wOrH - nbColRow
        if(roundInf == False and (wOrH*nb)%100 != 0):
            return [nbColRow+1,nbRemaining-1]
        return [nbColRow,nbRemaining]

    #returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def respCol(nb, roundInf=True):
        if nb>12 or nb<0:
            raise ValueError('0 < (responsive columns: int) <= 12')
        respCols = (Pycli.__width*nb)//12
        nbRemaining = Pycli.__width-respCols
        if(roundInf == False and (Pycli.__width*nb)%12 != 0):
            return [respCols+1,nbRemaining-1]
        return [respCols,nbRemaining]


    class Color:
        base = {'BLACK': 0,
        'RED': 1,
        'GREEN': 2,
        'YELLOW': 3,
        'BLUE': 4,
        'PURPLE': 5,
        'VIOLET': 5,
        'PINK': 5,
        'CYAN': 6,
        'GRAY': 7,
        'GREY': 7,
        'WHITE':7}
        
        special = { 'L_BLACK': 90,
        'D_GRAY': 90,
        'D_GREY': 90,
        'L_RED': 91,
        'L_GREEN': 92,
        'L_YELLOW': 93,
        'L_BLUE': 94,
        'L_PURPLE': 95,
        'PINK': 95,
        'L_VIOLET': 95,
        'L_CYAN': 96,
        'L_GRAY': 97,
        'L_GREY': 97,
        'WHITE':97}

        """
        def clr(string, light_str='', fg=True):
            string = string.upper()
            if(fg == True and light_str==''):
                style = 30
            elif(fg == True and light_str!=''):
                style = 90
            else:
                style = 40

            #shortcut special color (forground only)
            if(fg == True and 
              (string.startswith('L_') or string.startswith('D_'))):
                return Pycli.color(Pycli.Color.special.get(string))
            elif(fg == True and string=='PINK'):
                return Pycli.color(Pycli.Color.special.get(string))
            elif(fg == False and string=='PINK'):
                string = 'PURPLE'
            elif(fg == True and string=='WHITE'):
                return Pycli.color(Pycli.Color.special.get(string))
            elif(fg == False and string=='WHITE'):
                string = 'GRAY'
            elif(string.startswith('D_')):
                string = 'BLACK'
            elif(string.startswith('L_')):
                string = string[2:]

            return Pycli.color(style+Pycli.Color.base.get(string))
        """
        @staticmethod
        def clr(clr_name:str, fg:bool=True) -> str:
            clr_name = clr_name.upper()
            #if bg color
            if not fg:
                clr_name = re.sub(r'[DL]_','',clr_name)
                if clr_name not in Pycli.Color.base:
                    raise ValueError(f"background color {clr_name} not available.")
                else:
                    return Pycli.color( 40+Pycli.Color.base[clr_name] )
            #if fg special color
            elif clr_name in Pycli.Color.special:
                return Pycli.color( Pycli.Color.special[clr_name] )
            #if fg base color
            elif clr_name in Pycli.Color.base:
                return Pycli.color( 30+Pycli.Color.base[clr_name] )
            else:
                raise ValueError(f"foreground color {clr_name} not available.")
            
        @staticmethod
        def fg(clr_name):
            return Pycli.Color.clr(clr_name)
        @staticmethod
        def bg(clr_name):
            return Pycli.Color.clr(clr_name,False)
        @staticmethod
        def fbg(clr_name):
            color = Pycli.Color.clr(clr_name,False)
            color += Pycli.Color.clr(clr_name)
            return color
        @staticmethod
        def fgbg(fgclr_name, bgclr_name):
            color = Pycli.Color.clr(fgclr_name)
            color += Pycli.Color.clr(bgclr_name,False)
            return color
        
    
    class Write:
        @staticmethod
        def piece(string, fg='', bg='',style=''):
            return style+fg+bg+string+Pycli.clearf()
        
        def leftAt(x,y, string, fg='', bg='', style=''):
            return Pycli.position(x,y)+style+fg+bg+string+Pycli.clearf()

        def rightAt(x,y,w, string, fg='', bg='', style=''):
            x = x+(w-len(string))
            return Pycli.Write.leftAt(x,y, string, fg, bg, style)

        def centerAt(x,y,w, string, fg='', bg='', style=''):
            x = x + ( (w - len(string)) // 2 )
            return Pycli.Write.leftAt(x,y,string,fg,bg,style)

        def justifyAt(x,y,w, string, fg='', bg='', style=''):
            string = string.strip()
            #if word not fit or fit exactly
            if len(string)>w:
                raise ValueError(f"string({len(string)}) not fit in provided width({w})")
            
            #if unique word string or fit perfectly
            if string.find(' ')==-1 or len(string)==w:
                return Pycli.Write.centerAt(x,y,w,string,fg,bg,style)
            else:
                words = string.split(" ")
                nb_of_spaces = len(words)-1
                space_to_fill = w-(len(string)-nb_of_spaces)
                newSpaces = space_to_fill // nb_of_spaces
                space_to_distribute = space_to_fill % nb_of_spaces
                curr_word_id = (len(words)//2)-1 if len(words)%2 == 0 else len(words)//2
                toSub = curr_word_id%2
                
                for i in range (0,len(words)):
                    if(i%2==toSub):
                        curr_word_id -= i
                    else:
                        curr_word_id += i
                    
                    if(curr_word_id == len(words)-1):
                        continue
                    
                    words[curr_word_id] = words[curr_word_id]+(' '*newSpaces)

                    if(space_to_distribute>0):
                        words[curr_word_id] = words[curr_word_id]+' '
                        space_to_distribute -= 1

                return Pycli.Write.leftAt(x,y,("".join(words))[0:w],fg,bg,style)

        def leftIn(x,y,h, string, vertical='top', style=''):
            return Pycli.Write.into(x,y,-1,h, string, 'left', vertical, style)
        
        def centerIn(x,y,w,h, string, vertical='top', style=''):
            return Pycli.Write.into(x,y,w,h, string, 'center', vertical, style)
        
        #TODO rightIn, centerIn, justifyIn short cut function to use into()

        def paragraph(x,y,w,h, string_list, horizontal,vertical='top', style=''):
            if len(string_list)>h:
                raise ValueError("Your paragraphe is larger than the text zone height")

            if vertical in ['top','t']:
                pass
            elif vertical in ['bottom','b','bot']:
                y += h-len(string_list)
            elif vertical in ['center','middle','c','m','cen','mid']:
                y += (h-len(string_list))//2
            else:
                raise ValueError("Vertical value incorrect try 'top', 'bottom' or 'middle'")

            screen = ''
            i=0
            for line in string_list:
                screen += Pycli.Write.into(x,y+i,w,h, line, horizontal,'top', style)
                i += 1
            
            return screen

        def into(x,y,w,h, string, horizontal,vertical='top', style=''):
            if vertical in ['top','t']:
                pass
            elif vertical in ['bottom','b','bot']:
                y += h-1
            elif vertical in ['center','middle','c','m','cen','mid']:
                y += (h-1)//2
            else:
                raise ValueError("Vertical value incorrect try 'top', 'bottom' or 'middle'")
            
            if horizontal in ['left','l']:
                return Pycli.Write.leftAt(x,y, string, style)
            elif horizontal in ['center','middle','mid','cen','c','m']:
                return Pycli.Write.centerAt(x,y,w, string, style)
            elif horizontal in ['right','r']:
                return Pycli.Write.rightAt(x,y,w, string, style)
            elif horizontal in ['justify','j']:
                return Pycli.Write.justifyAt(x,y,w, string, style)
            else:
                raise ValueError("Horizontal value incorrect try 'left', 'center' or 'right'")

        def lnTolns(w, string, word_cut=False):
            #TODO add unbreakable space between word and punctuation
            words = string.split(' ')
            lines = []
            currWord = 0
            nextWord = words[currWord]
            l = 0
            lw = w
            end = False
            while not end:
                # Calculate remaining space in line l
                # Create line if not exists or line full
                if l < len(lines):
                    lw = w-len(lines[l])
                    if lw == 0:
                        l += 1

                if l >= len(lines):
                    lw = w
                    lines.append('')

                

                # IF word or part larger than remaining space
                # AND cut word forbidden
                if(len(nextWord) > lw and not word_cut):
                    # WORD is bigger than space
                    if len(nextWord)>w:
                        l += 1
                        lines.append(nextWord[0:w])
                    # OR word only bigger than remaining space
                    else:
                        l += 1
                        if len(nextWord)!=w:
                            lines.append(nextWord+' ')
                        else:
                            lines.append(nextWord)
                    
                    currWord += 1 

                # IF word or part larger than remaining space
                # AND cut word allowed
                elif(len(nextWord) > lw and word_cut):
                    lines[l] += nextWord[0:lw-1]+'-'
                    nextWord = nextWord[lw-1:]
                    continue

                # word or part exactly fit in remainnig space
                elif(len(nextWord) == lw):
                    lines[l] += nextWord
                    currWord += 1

                # word fit in remaining space
                elif(len(nextWord) < lw):
                    lines[l] += nextWord + ' '
                    currWord += 1

                if currWord < len(words):
                    nextWord = ''
                    while nextWord=='':
                        nextWord = words[currWord]
                        currWord += 1 if nextWord == '' else 0
                else:
                    end = True

            return lines

        # PADDING left,right,top,bottom(pl,pr,pt,pb) of parent(x,y,w,h)
        # Make child (x+1+pl, y+1+pt, w-2-pl-pr, h-2-pt-pb)
        # OR padding 0 forbidden (because remove box which have same coordidates)
        # And then child(x+pl, y+pt, w-pl-pr, h-pt-pb) and default padding = 1
    
    class Draw:
        @staticmethod
        def screen(screenString):
            print(screenString, end='')

        @staticmethod
        def horizontal(x,y,w, char='─', style=''):
            line = char*w
            return Pycli.Write.leftAt(x,y,line,style)

        @staticmethod
        def vertical(x,y,h, char='│', style=''):
            line = ''
            for i in range(0,h):
                line += Pycli.position(x,y+i)
                line += Pycli.Write.piece(char, style)
            return Pycli.Write.leftAt(x,y,line,style)

        @staticmethod
        def desgonal(x,y,size, char="╲", center=False, style=''):
            line = ''
            if center == True:
                center = "╳"
            if center != False and size%2==0:
                center = False
            for i in range(0,size):
                line += Pycli.position(x+i,y+i)
                if(center is not False and
                 i == (size-1)//2):
                    line += Pycli.Write.piece(center, style)
                else:
                    line += Pycli.Write.piece(char, style)
            return Pycli.Write.leftAt(x,y,line,style)

        @staticmethod
        def asgonal(x,y,size, char="╱", center=False, style=''):
            x+=size-1
            line = ''
            if center == True:
                center = "╳"
            if center != False and size%2==0:
                center = False
            for i in range(0,size):
                line += Pycli.position(x-i,y+i)
                if(center is not False and
                 i == (size-1)//2):
                    line += Pycli.Write.piece(center, style)
                else:
                    line += Pycli.Write.piece(char, style)
            return Pycli.Write.leftAt(x,y,line,style)

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
                line += Pycli.position(curr_x,curr_y)
                line += Pycli.Write.piece(char, style)
            return line

        #TODO rectasgonal(x,y,w,h, char="*", style='')
        
        # char -> repeated char use to draw rectangle sides
        # list(topleft,topright,bottomleft,bottomright,horizontal,vertical)
        @staticmethod
        def rectangle(x, y, w, h, char:list=['┌','┐','└','┘','─','│'],fg='',bg=''):
            #TODO change fg and bg type to list, to color each line individually
            rect = ''
            if len(char)>=0 and len(char)<6:
                pattern = " " if len(char)==0 else char[0]
                char = []
                for i in range(0,6):
                    char.append(pattern)
            elif len(char)!=6:
                raise ValueError("Error in param 5, must be list(len<7) of string")
            
            horizontal = char[4]*(w-2)
            rect = Pycli.position(x,y)
            y+=1
            #top of rectangle
            rect += Pycli.Write.piece(char[0]+horizontal+char[1],fg,bg)
            #verticals of rectangles
            for i in range(0,h-2):
                #draw pattern left at position x,y
                rect += Pycli.position(x,y)
                rect += Pycli.Write.piece(char[5],fg,bg)
                #ajust position for next pattern
                x += w-1
                #draw second pattern of line
                rect += Pycli.position(x,y)
                rect += Pycli.Write.piece(char[5],fg,bg)
                #adjust coordinate for next line
                x -= w-1
                y += 1
            rect += Pycli.position(x,y)
            return rect + Pycli.Write.piece(char[2] + horizontal + char[3],fg,bg)

        @staticmethod
        def rectback(x, y, w, h, color):
            rectbg = ''
            for i in range(0,h):
                rectbg += Pycli.position(x,y+i)
                rectbg += Pycli.Write.piece(' '*w, color)
            
            return rectbg
        
        @staticmethod
        #bg:str color name like 'red', 'blue'...
        def rect(x=0,y=0,w=0,h=0, border_style=None, border_color=None, bg=None):
            #if rect has no height or no width don't draw anything
            if w == 0 or h == 0: return
            
            box = ''

            #if exists draw background
            if bg is not None:
                box += Pycli.Draw.rectback(x, y, w, h, Pycli.Color.bg(bg))
            
            #draw border if exists
            if border_style is not None:
                box += Pycli.Draw.rectangle(
                    x,y,w,h, border_style,
                    '' if border_color is None else border_color
                )
                
            
            
