from pycli_terminal import Terminal
from pycss_inheritance import numeric_props

import re

class Convert:
    __round_inf = False

    @staticmethod
    def get_size():
        w = Terminal.get_width()
        if w >=300: return 'xxl'
        elif w >= 240: return 'xl'
        elif w >= 180: return 'l'
        elif w >= 120: return 'm'
        elif w >= 60:  return 's'
        else: return 'xs'
        
    #    x      perc           perc × val_max
    # ------- = ----  <=>  x = --------------
    # val_max   100                100

    #if 100% separate in various even smaller percents
    #round_inf_auto permit use all rows/cols of console
    #if 100% separate in various even smaller percents
    #round_inf_auto permit to be closer to 100% of cols/rows

    #returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def percent(perc, val_max='w', round_inf=True, round_inf_auto=False):
        
        if round_inf_auto:
            Convert.__round_inf = not Convert.__round_inf
            round_inf = Convert.__round_inf

        if(val_max in ['w','x','col','cols','width','column','columns']):
            val_max = Terminal.get_width()
        elif(val_max in ['h','y','row','rows','height']):
            val_max = Terminal.get_height()
        elif(type(val_max) != int):
            raise ValueError(f'max value {val_max} is not a valid value.')

        valColRow = (val_max*perc)//100
        valRemaining = val_max - valColRow
        if(round_inf == False and (val_max*perc)%100 != 0):
            return [valColRow+1,valRemaining-1]
        return [valColRow,valRemaining]

    #returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def respCol(nb, round_inf=True):
        if nb>12 or nb<0:
            raise ValueError('0 < (responsive columns: int) <= 12')
        respCols = (Terminal.get_width()*nb)//12
        nbRemaining = Terminal.get_width()-respCols
        if(round_inf == False and (Terminal.get_width()*nb)%12 != 0):
            return [respCols+1,nbRemaining-1]
        return [respCols,nbRemaining]

    def border_style(style):
        if style == 'classic':
            return ['┌','┐','└','┘','─','│']
        elif style == 'dotted':
            return ['┌','┐','└','┘','·',':']
        elif style == 'dashed':
            return ['┌','┐','└','┘','-','¦']
        elif style == 'waved':
            return ['┌','┐','└','┘','~','{']

    # to adjust better use Convert.percent()
    # half time with roundInf=True and half time = False
    # available: % TODO => px, responsive cols
    # default unit -> terminal row/col
    def value(val, val_max='w'):
        if type(val) in [int, float]:
            return int(val)
        elif type(val) is str:
            val = re.sub(r"\s*",'',val)
            if re.match(r"\d+$",val):
                return int(val)
            elif val[-1] == '%':
                return Convert.percent(int(val[0:-1]), val_max, round_inf_auto=True)[0]
        raise ValueError(f'\033[31mpycss error: not recognized value {val}\033[0m')

    #pycss: dict {str: str|int}
    #parent: tuple (width:int, height:int) unit= terminal row/col
    def special_units(pycss, parent_size):

        for oriented_props in numeric_props:

            if oriented_props == "horizontal":
                parent_base = parent_size[0]
            else:
                parent_base = parent_size[1]
            
            for prop in numeric_props[oriented_props]:
                pycss[prop] = Convert.value(pycss[prop], parent_base)
        
        return 'end'