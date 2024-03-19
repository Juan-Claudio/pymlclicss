#convert pyml to pyDom
import re

# PYML NODE => PYML ELEMENT
class Pyml_element:
    def __init__(self, idx, indent, tag_name, id='', className='', txt='', style={}):
        self.__idx = idx
        self.__indent = indent
        self.__tag_name = tag_name
        self.__id = id
        self.__class = className
        self.__txt = txt
        self.__style = style
        self.__children = []

    def __str__(self):
        return f'<{self.tag_name}:{self.id} class="{self.className}" txt="{self.txt}" idx="{self.idx}" style="{self.style}">'
    
    @property
    def idx(self): return self.__idx
    @property
    def indent(self): return self.__indent
    @property
    def tag_name(self): return self.__tag_name
    @property
    def id(self): return self.__id
    @property
    def className(self): return self.__class
    @property
    def txt(self): return self.__txt
    @property
    def style(self): return self.__style
    @property
    def children(self): return self.__children

    def get(self, propName):
        if propName == "idx": return self.__idx
        elif propName == "indent": return self.__indent
        elif propName == "tag_name": return self.__tag_name
        elif propName == "id": return self.__id
        elif propName == "class": return self.__class
        elif propName == "txt": return self.__txt
        elif propName == "style": return self.__style
        elif propName == "children": return self.__children
        else: raise ValueError(f'\033[31mPyml_element has no property {propName}\033[0m')

    def add_child(self, node):
        self.children.append(node)
        return node #to test
    
    #def remove_child
    #def update_child
    def setstyle(self, new_style): self.__style = new_style
    def setclass(self, new_class): self.__class = new_class

# PYML TREE => PYML DOM
class Pyml_tree:
    elements = []

    def __init__(self):
        self.__root = Pyml_element(0,0,'pyml')
        self.__counter = 1

    def get_root(self): return self.__root

    def getElement(self, target, target_type, search_func, node):
        if node is None: node = self.__root
        if node.get(target_type) == target: return node
        for child in node.children:
            res = search_func(target, child)
            if res: return res
    
    def getElements(self, target, target_type, search_func, node=None):
        if node is None:
            self.elements = []
            node = self.__root
        if node.get(target_type) == target:
            self.elements.append(node)
        
        for child in node.children:
            res = search_func(target, child)

        return self.elements

    """
    def getElementByIdx(self, target_idx, node=None):
        if node is None:
            node = self.__root
        
        if node.idx == target_idx:
            return node
        
        for child in node.children:
            res = self.getElementByIdx(target_idx, child)
            if res: return res
    
    def getElementById(self, target_id, node=None):
        if node is None:
            node = self.__root
        elif node.id == target_id:
            return node
        
        for child in node.children:
            res = self.getElementById(target_id, child)
            if res: return res
    """
    def getElementByIdx(self, target_idx, node=None):
        return self.getElement(target_idx, 'idx', self.getElementByIdx, node)

    def getElementById(self, target_id, node=None):
        return self.getElement(target_id, 'id', self.getElementById, node)

    def getElementsByTagName(self, target_tag_name, node=None):
        return self.getElements(target_tag_name, 'tag_name', self.getElementsByTagName, node)

    def getElementsByClass(self, target_class, node=None):
        return self.getElements(target_class, 'class', self.getElementsByClass, node)
    
    def query(self, selector):
        if selector.startswith('#'):
            return self.getElementById(selector[1:])
        elif selector.startswith('.'):
            return self.getElementsByClass(selector[1:])
        else:
            return self.getElementsByTagName(selector)
    
    def addElementToIdx(self, parent_idx, node_dict):
        #get parent node
        parent = self.getElementByIdx(parent_idx)

        #add node to tree
        parent.add_child( Pyml_element(
            idx=self.__counter,
            indent=node_dict['indent'],
            tag_name=node_dict['tag_name'],
            id=node_dict['id'],
            className=node_dict['class'],
            txt=node_dict['txt']
        ) )

        #increment idx counter
        self.__counter += 1

        return self.__counter-1

    def setstyle(self, pycssdict):
        #print(pycssdict)
        for selector in pycssdict:
            elements = self.query(selector)
            if type(elements)==list:
                for elmt in elements:
                    elmt.setstyle(pycssdict[selector])
            else:
                elements.setstyle(pycssdict[selector])

    def print_tree(self, node=None, indent=0):
        if node is None:
            node = self.__root

        print('  ' * indent, end='')
        print(node)

        for child in node.children:
            self.print_tree(child, indent + 1)


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