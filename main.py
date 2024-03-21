#! /usr/bin/python3.10
from Pycli import Pycli
from pyml_interpreter import Pyml_to_dom
from pycss_interpreter import Pyml_css_to_dom

Pycli.Terminal.clear()


#test pyml pycss files to pydom

document = Pyml_to_dom.file_to_dom('view/test.pyml')
Pyml_css_to_dom.file_to_dom(document, 'view/test.pycss')
document.inherit_and_draw()
#document.print_tree()
document.print_screen()
