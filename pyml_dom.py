from pyml_element import Pyml_element
from pycss_inheritance import default_props
from pycss_inheritance import siblings_width
from pycss_inheritance import siblings_height
from Pycli import Pycli

# PYML TREE => PYML DOM
class Pyml_tree:
    elements = []
    screen = ''

    def __init__(self):
        self.__root = Pyml_element(0,0,'pyml',style=default_props['pyml'])
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

        #define node default pycss style
        new_style = node_dict['tag_name']
        if node_dict['tag_name'] not in default_props:
            new_style = 'unrecognized'

        #add node to tree
        parent.add_child( Pyml_element(
            idx= self.__counter,
            indent= node_dict['indent'],
            tag_name= node_dict['tag_name'],
            id= node_dict['id'],
            className= node_dict['class'],
            txt= node_dict['txt'],
            style= default_props[new_style]
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
                    pycss = elmt.style.copy()
                    pycss.update(pycssdict[selector])
                    elmt.setstyle(pycss)
            else:
                pycss = elements.style.copy()
                pycss.update(pycssdict[selector])
                elements.setstyle(pycss)

    #TO TEST
    def inherit_and_draw(self, parent=None):
        #inicialization with root node (<pyml>)
        if parent is None:
            self.screen = ''
            pycss = self.__root.style.copy()
            Pycli.Convert.special_units(pycss, ('w','h'))
            pycss['x'] += pycss['margin-left']
            pycss['y'] += pycss['margin-top']
            pycss['width'] -= (pycss['margin-left'] + pycss['margin-right'])
            pycss['height'] -= (pycss['margin-top'] + pycss['margin-bottom'])
            self.__root.setprops(pycss)
            self.inherit_and_draw(self.__root)
        else:
            sib = parent.children
            prev_left = 0
            prev_top = 0
            for i in range(0, len(sib)):
                pycss = sib[i].style.copy()

                Pycli.Convert.special_units(
                    pycss,
                    (parent.props['width'], parent.props['height'])
                )

                #margin modify the element x, y, w and h itself
                pycss['x'] += pycss['margin-left']
                pycss['y'] += pycss['margin-top']
                pycss['width'] -= pycss['margin-left']
                pycss['width'] -= pycss['margin-right']
                pycss['height'] -= pycss['margin-top']
                pycss['height'] -= pycss['margin-bottom']

                #if position is relative -> x, y and text-color inherit
                #else position is absolute -> no inheritance
                if pycss['position-relative']:
                    pycss['x'] += parent.props['x']
                    pycss['x'] += parent.props['padding-left']
                    
                    pycss['y'] += parent.props['y']
                    pycss['y'] += parent.props['padding-top']
                                        
                    pycss['width'] -= parent.props['padding-left']
                    pycss['width'] -= parent.props['padding-right']

                    pycss['height'] -= parent.props['padding-left']
                    pycss['height'] -= parent.props['padding-right']

                    #apply siblings offset modifier
                    if pycss['children-row-align']:
                        pycss['x'] += prev_left
                    else:
                        pycss['y'] += prev_top

                    #text-color inherit
                    pycss['text-color'] = parent.props['text-color']
                        
                #save props changes
                sib[i].setprops(pycss)
                #save drawing props /!\ pyml no drawn /!\
                self.screen += Pycli.Draw.props(pycss, sib[i].txt)

                #calculate the siblings offset
                prev_left += pycss['width']
                prev_left += pycss['margin-left']
                prev_left += pycss['margin-right']

                prev_top += pycss['height']
                prev_top += pycss['margin-top']
                prev_top += pycss['margin-bottom']

                #recursive to children
                self.inherit_and_draw(sib[i])

    def print_tree(self, node=None, indent=0):
        if node is None:
            node = self.__root

        print('  ' * indent, end='')
        print(node)

        for child in node.children:
            self.print_tree(child, indent + 1)

    def print_screen(self):
        if self.screen != '':
            self.screen += Pycli.Style.position(0,53)
            Pycli.Draw.screen(self.screen)
        