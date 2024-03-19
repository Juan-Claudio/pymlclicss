#! /usr/bin/python3.10
from Pycli import Pycli
from pyml_interpreter import Pyml_to_dom
from pycss_interpreter import Pyml_css_to_dom

Pycli.clear()

document = Pyml_to_dom.file_to_dom('view/test.pyml')
Pyml_css_to_dom.file_to_dom(document, 'view/test.pycss')
document.print_tree()