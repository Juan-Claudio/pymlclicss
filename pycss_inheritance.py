def siblings_width(silblings_node_list):
   w = 0
   for child in silblings_node_list:
      style = child.style
      w += style['width']
      w += style['margin-left']
      w += style['margin-right']
   return w

def siblings_height(silblings_node_list):
   h = 0
   for child in silblings_node_list:
      style = child.style
      h += style['height']
      h += style['margin-top']
      h += style['margin-bottom']
   return h

#x and y inherit if position-relative:False from parent and siblings(according to position into)
#text-color from parent
def update_default_props(dict_modifier=None):
    default_props = {
        'background-color':None,
        'border-style':None,
        'border-color':None,
        'border-background':None,
        'margin-top':0,
        'margin-bottom':0,
        'margin-left':0,
        'margin-right':0,
        'padding-top':0,
        'padding-bottom':0,
        'padding-left':0,
        'padding-right':0,
        'position-relative':True,
        'children-row-align':False,
        'width':0, 'height':0,
        'x':0, 'y':0,
        'text-align-x':"left",
        'text-align-y':"top",
        'text-color':None,
        'text-background':None
    }
    if dict_modifier is None: return default_props
    default_props.update(dict_modifier)
    return default_props

default_props = {
    'pyml': update_default_props(),
    'row': update_default_props({'width':"100%"}),
    'rect': update_default_props({
        'border-style': "classic",
        'padding-top': 1,
        'padding-bottom': 1,
        'padding-left': 1,
        'padding-right': 1
    }),
    'txt': update_default_props({
        'margin-top': 1,
        'margin-bottom': 1,
        'margin-left': 1,
        'margin-right': 1
    }),
    'unrecognized': update_default_props()
}

numeric_props = {
   'horizontal':[
      'margin-left',
      'margin-right',
      'padding-left',
      'padding-right',
      'width', 'x'
   ],
   'vertical':[
      'margin-top',
      'margin-bottom',
      'padding-top',
      'padding-bottom',
      'height', 'y'
   ]
}