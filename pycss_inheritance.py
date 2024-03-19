from pycss_val_trads import Convert
from default_values import default_values

screen = ""

def dom_to_cli(pydom, node=None):
   #inicialization
   if node is None:
      node = pydom.getroot()

   #define the final pycss rules of the current node
   pycss = {}
   pycss.update(default_values[node.tag_name])
   pycss.update(node.getstyle())
   
   #css to cli
   #if border or/and background fill/stroke rect
   screen += Pycli.rect(
      Convert.value(pycss['x'], 'x'),
      Convert.value(pycss['y'], 'y'),
      Convert.value(pycss['w'], 'w'),
      Convert.value(pycss['h'], 'h'),
      Convert.border_style(pycss['bo-s']),
      pycss['bo-c'],
      pycss['bg']
   )

   #loop recursively through pydom
   for child in node:
      pass
