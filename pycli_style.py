import re

class Style:
    base_color = {'BLACK': 0,
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
    
    special_color = { 'L_BLACK': 90,
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

    @staticmethod
    def position(x=None,y=None):
        if x is None and y is None: return ''
        elif x is None: return f"\033[{y+1}f"
        elif y is None: return f"\033[{x+1}G"
        return f"\033[{y+1};{x+1}f"

    @staticmethod
    def ansi_m(clr_num) -> str: return f"\033[{clr_num}m"

    @staticmethod
    def clearf(): return "\033[0m"

    @staticmethod
    def name_to_ansi_color(clr_name:str, fg:bool=True) -> str:
        clr_name = clr_name.upper()
        #if bg color
        if not fg:
            clr_name = re.sub(r'[DL]_','',clr_name)
            if clr_name not in Style.base_color:
                raise ValueError(f"background color {clr_name} not available.")
            else:
                return Style.ansi_m( 40+Style.base_color[clr_name] )
        #if fg special color
        elif clr_name in Style.special_color:
            return Style.ansi_m( Style.special_color[clr_name] )
        #if fg base color
        elif clr_name in Style.base_color:
            return Style.ansi_m( 30+Style.base_color[clr_name] )
        else:
            raise ValueError(f"foreground color {clr_name} not available.")
        
    @staticmethod
    def fg(clr_name):
        return Style.clr(clr_name)
    
    @staticmethod
    def bg(clr_name):
        return Style.clr(clr_name,False)
    
    @staticmethod
    def fbg(clr_name):
        color = Style.clr(clr_name,False)
        color += Style.clr(clr_name)
        return color
    
    @staticmethod
    def fgbg(fgclr_name, bgclr_name):
        color = Style.clr(fgclr_name)
        color += Style.clr(bgclr_name,False)
        return color