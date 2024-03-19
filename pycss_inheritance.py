from default_values import default_values
def pyml_to_pycli(pydom):
    #get root pycss info
    curr_pycss = {}
    curr_pycss.update(default_values['pyml'])
    curr_pycss.update(pydom.get_root().getstyle())
