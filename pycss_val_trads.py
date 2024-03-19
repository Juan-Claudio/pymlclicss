import re
from Pycli import Pycli

class Convert:
    percent_round_inf = True

    def border_style(style):
        if style == 'classic':
            return '' #['┌','┐','└','┘','─','│']
        elif style == 'dotted':
            return ['┌','┐','└','┘','·',':']
        elif style == 'dashed':
            return ['┌','┐','└','┘','-','¦']
        elif style == 'waved':
            return ['┌','┐','└','┘','~','{']

    # to adjust better use Pycli.Unit.percent()
    # half time with roundInf=True and half time = False
    def value(perc, val_max='w'):
        if type(perc) in [int, float]:
            return int(perc)
        elif type(perc) is str:
            perc = re.sub(r"\s*",'',perc)
            if re.match(r"\d+$",perc):
                return int(perc)
            elif perc[-1] == '%':
                Convert.percent_round_inf = not Convert.percent_round_inf
        raise ValueError(f'\033[31mpycss error: no recognized value {perc}\033[0m')



"""
classic
┌───────────┐
│           │
│           │
│           │
└───────────┘

dashed
┌-----------┐
╎           ╎
╎           ╎
╎           ╎
└-----------┘

dotted
┌···········┐
:           :
:           :
:           :
└···········┘

waved
┌~~~~~~~~~~~┐
{           {
{           {
{           {
└~~~~~~~~~~~┘

"""