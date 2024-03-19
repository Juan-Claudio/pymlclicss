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