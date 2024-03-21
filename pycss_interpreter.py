import re

class Pyml_css_to_dom:
   def load_pycss_file(path:str):
        with open(path, 'r') as file:
            pycss = file.read()
        return pycss

   def tokener(pycss_code):
      #remove all spaces
      tokens = re.sub(r'\s*','',pycss_code)
      
      #remove comments
      tokens = re.sub(r'\/\*[^(\*\/)]+\*\/', '', tokens)

      #find all blocks /!\ if add new units must add them in the regexp below
      tokens = re.findall(r'[#.,\-\w]+\{[;:\-\w%]+\}', tokens, re.M)

      return tokens
   
   def token_to_pycss_objects(tokens):
      #split selector(s) - properties
      blocks_tokens = {}
      for token in tokens:
         #separate selector(s) and block of properties
         token = token.split('{')
         #separate instructions
         token[1] = token[1].split(';')
         #remove empty instruction
         if token[1][-1] == '': token[1].pop()
         #different entry for all single selector
         #split selector list separate by ','
         for selector in token[0].split(','):
            #if selector exists, add properties to list
            if selector in blocks_tokens:
               blocks_tokens[selector] = blocks_tokens[selector] + token[1][:-1]
            else:
               blocks_tokens[selector] = token[1][:-1]
      
      #list of instructions to instructions dict
      for x in blocks_tokens:
         blocks_tokens[x] = Pyml_css_to_dom.instructions_list_to_dict(blocks_tokens[x])
      
      return blocks_tokens
   
   def instructions_list_to_dict(instructions_list):
      instructions = {}
      for x in instructions_list:
         key_val = x.split(':')
         instructions[key_val[0]] = key_val[1]
      return instructions

   def insert_pycss(pydom, pycss):
      pydom.setstyle(pycss)
   
   def file_to_dom(pydom, path):
      pycss = Pyml_css_to_dom.load_pycss_file(path)
      tokens = Pyml_css_to_dom.tokener(pycss)
      pycss_object = Pyml_css_to_dom.token_to_pycss_objects(tokens)
      Pyml_css_to_dom.insert_pycss(pydom, pycss_object)

"""
#tests pycss file to pycss dict of dicts
pycss = Pyml_css_to_dom.load_pycss_file('test.pycss')
tokens = Pyml_css_to_dom.tokener(pycss)
pycss_object = Pyml_css_to_dom.token_to_pycss_objects(tokens)

for x in pycss_object:
   print(x)
   for y in pycss_object[x]:
      print('  ·',y,'=',pycss_object[x][y])
   print()
"""