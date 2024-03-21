#convert pyml to pyDom
import re
from pyml_element import Pyml_element
from pyml_dom import Pyml_tree

#PYML INTERPRETER => From pyml code to dom object
class Pyml_to_dom:
    def load_pyml_file(path:str):
        with open(path, 'r') as file:
            pyml_code = file.read()
        return pyml_code
    
    def tokener(pyml_code:str):
        #remove comments
        pyml_code = re.sub(r"<![^>]+>", '', pyml_code)
        #return matched pyml tags with previous spaces list
        return re.findall(r" *<[^>]+>", pyml_code)

    def tag_parser(tag:str):
        #retrieve spaces
        indent = re.search(r"\s+", tag)
        if indent is not None: indent = indent.group()
        else: indent = ''
        if len(indent)%3 != 0:
            raise ValueError("\033[31mIndent error in pyml code. 3 spaces indents required.\033[0m")
        indent = len(indent)//3
        
        #retrieve tag_name
        tag_name = re.search(r"<[^: >]+", tag)
        if tag_name is not None: tag_name = tag_name.group()[1:]
        else: raise ValueError(f'pyml code error: Unrecognized tag: {tag}')
        
        #retrieve id if exists ':id'
        id = re.search(r":[^ >]+", tag)
        if id is not None: id = id.group()[1:]
        else: id=''

        #retrieve class if exists 'class="text_string'
        className = re.search(r'class="[^"]+', tag)
        if className is not None: className = className.group()[7:]
        else: className=''

        #retrieve text if exists 'txt="text_string"
        txt = re.search(r'txt="[^"]+', tag)
        if txt is not None: txt = txt.group()[5:]
        else: txt = ''

        return {
            'indent':indent,
            'tag_name':tag_name,
            'id':id,
            'txt':txt,
            'class':className
        }
        
    def dom_builder(tokens:list):
        document = Pyml_tree() #create pyml tree with pyml root node
        parent_idx = {0:0} #indent:idx
        root_initialized = False
        curr_idx = 0
        for tag in tokens:
            tag = Pyml_to_dom.tag_parser(tag)
            if tag['tag_name']!='pyml':
                if root_initialized:
                    parent_indent = tag['indent']-1
                    curr_idx = document.addElementToIdx(parent_idx[parent_indent],tag)
                    parent_idx[tag['indent']] = curr_idx
                else:
                    raise ValueError('pyml code error: Code must begin by <pyml> with indent 0')
            else:
                if root_initialized:
                    raise ValueError('pyml code error: Only one <pyml> at the top of the code allowed.')
                root_initialized = True

        return document

    def file_to_dom(path):
        pymlcode = Pyml_to_dom.load_pyml_file(path)
        tokens = Pyml_to_dom.tokener(pymlcode)
        return Pyml_to_dom.dom_builder(tokens)