# Pycli elements

## Elements list
- <row>
zone with default x=0 and default w=100%
- <rect> stroke and/or fill rectangle
- <txt> text

## Attributs available
`pycss`
**bg** background-color:none|red|green|yellow|blue|purple|cyan|gray;

**bo-s** border-style:classic|dashed|dotted|waved
**bo-fg** border-fg-color:[l]red|[l]green|[l]yellow|[l]blue|[l]purple|[l]cyan|[l]gray;
**bo-bg** border-bg-color:red|green|yellow|blue|purple|cyan|gray;

## margin
**m-t** margin-top:size;
**m-b** margin-bottom:size;
**m-l** margin-left:size;
**m-r** margin-right:size;

**p-t** padding-top:size;
**p-b** padding-bottom:size;
**p-l** padding-left:size;
**p-r** padding-right:size;

**w**   width:size;
**h**   height:size;
**x**   position-x:size;
**y**   position-y:size;

**t-a-h** text-align-horizontal:left|middle|justify|right
**t-a-v** text-align-vertical:top|middle|bottom
**tfg** text-color:[l]red|[l]green|[l]yellow|[l]blue|[l]purple|[l]cyan|[l]gray;
**tbg** text-background:red|green|yellow|blue|purple|cyan|gray;

### not created
**tbold** text-bold:bold|none;


## Attributs detail
- position:
    - ~ · ·  · Relative position according to the parent
    - [~]%%n - -  - n percent rounded to greatest
    - [~]%n - - - n percent rounded to smallest
    - [~][@]@n - -  - n th responsive col
    - [~]n - - - - n col/row
    - [~]center - center
    
    
## Screen example

<pyml>
    <!--ROW1-->
    <row:speChar>
        <rect:speCharTitle>
            <txt:speCharTitle_bold txt="Question nº">
            <txt:speCharTitle_bold_red txt="$variable">
        <rect:speCharCont>
            <txt:speCharCont>
     <!--ROW2-->
    <row:question>
        <back:qtitle>
            <txt:qtitle>
        <rect:qcont>
            <txt:qcont>
    <!--ROW3-->
    <row:answer>
        <back:atitle>
            <txt:atitle>
        <rect:acont>
            <txt:acont>

## pycss operation
- margin change x, y of element itself
- margin include in width (margin left and right removed from width pycss property)
- margin include in height (margin top and bottom removed from height pycss property)
- padding change x,y of children elements
- padding change width, height of children elements (like margin change w,h of element itself)

## Last version
    pyml_interpreter.py
        contains
            Pyml_element
            Pyml_tree
            Pyml_to_dom
        transform pyml code (string or from file)
        to Pyml_tree of nodes
    
    pycss_interpreter.py