from pyelement import Pyml_element

# PYML TREE => PYML DOM
class Pyml_tree:
    elements = []

    def __init__(self):
        self.__root = Pyml_element(0,0,'pyml')
        self.__counter = 1

    def getroot(self): return self.__root

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