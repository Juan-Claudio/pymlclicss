from pycli_terminal import Terminal

class Unit:
    @staticmethod
    def get_size():
        w = Terminal.__width
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
    
    #returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def percent(val, val_max='w', roundInf=True):
        if(val_max in ['w','x','col','cols','width','column','columns']):
            val_max = Terminal.__width
        elif(val_max in ['h','y','row','rows','height']):
            val_max = Terminal.__height
        elif(type(val_max) != int):
            raise ValueError(f'max value {val_max} is not a valid value.')

        valColRow = (val_max*val)//100
        valRemaining = val_max - valColRow
        if(roundInf == False and (val_max*val)%100 != 0):
            return [valColRow+1,valRemaining-1]
        return [valColRow,valRemaining]

    #returns list [number of cols/rows, remaining cols/rows]
    @staticmethod
    def respCol(nb, roundInf=True):
        if nb>12 or nb<0:
            raise ValueError('0 < (responsive columns: int) <= 12')
        respCols = (Terminal.__width*nb)//12
        nbRemaining = Terminal.__width-respCols
        if(roundInf == False and (Terminal.__width*nb)%12 != 0):
            return [respCols+1,nbRemaining-1]
        return [respCols,nbRemaining]