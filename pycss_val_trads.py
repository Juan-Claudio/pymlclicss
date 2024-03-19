def border_style(style):
    if style == 'classic':
        return '' #['┌','┐','└','┘','─','│']
    elif style == 'dotted':
        return ['┌','┐','└','┘','·',':']
    elif style == 'dashed':
        return ['┌','┐','└','┘','-','¦']
    elif style == 'waved':
        return ['┌','┐','└','┘','~','{']





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