from pycli_terminal import Terminal

class Unit:
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
            Unit.__round_inf = not Unit.__round_inf
            round_inf = Unit.__round_inf

        if(val_max in ['w','x','col','cols','width','column','columns']):
            val_max = Terminal.__width
        elif(val_max in ['h','y','row','rows','height']):
            val_max = Terminal.__height
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
        respCols = (Terminal.__width*nb)//12
        nbRemaining = Terminal.__width-respCols
        if(round_inf == False and (Terminal.__width*nb)%12 != 0):
            return [respCols+1,nbRemaining-1]
        return [respCols,nbRemaining]