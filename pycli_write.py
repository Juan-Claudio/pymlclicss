from pycli_style import Style

class Write:
    @staticmethod
    def piece(string, style=''):
        return style+string+Style.clearf()
    
    def leftAt(x,y, string, style=''):
        return Style.position(x,y)+style+string+Syle.clearf()

    def rightAt(x,y,w, string, style=''):
        x = x+(w-len(string))
        return Write.leftAt(x,y, string, style)

    def centerAt(x,y,w, string, style=''):
        x = x + ( (w - len(string)) // 2 )
        return Write.leftAt(x,y,string,style)

    def justifyAt(x,y,w, string, style=''):
        string = string.strip()
        #if word not fit or fit exactly
        if len(string)>w:
            raise ValueError(f"string({len(string)}) not fit in provided width({w})")
        
        #if unique word string or fit perfectly
        if string.find(' ')==-1 or len(string)==w:
            return Write.centerAt(x,y,w,string,style)
        else:
            words = string.split(" ")
            nb_of_spaces = len(words)-1
            space_to_fill = w-(len(string)-nb_of_spaces)
            newSpaces = space_to_fill // nb_of_spaces
            space_to_distribute = space_to_fill % nb_of_spaces
            curr_word_id = (len(words)//2)-1 if len(words)%2 == 0 else len(words)//2
            toSub = curr_word_id%2
            
            for i in range (0,len(words)):
                if(i%2==toSub):
                    curr_word_id -= i
                else:
                    curr_word_id += i
                
                if(curr_word_id == len(words)-1):
                    continue
                
                words[curr_word_id] = words[curr_word_id]+(' '*newSpaces)

                if(space_to_distribute>0):
                    words[curr_word_id] = words[curr_word_id]+' '
                    space_to_distribute -= 1

            return Write.leftAt(x,y,("".join(words))[0:w], style)

    def into(x,y,w,h, string, horizontal,vertical='top', style=''):
        if vertical in ['top','t']:
            pass
        elif vertical in ['bottom','b','bot']:
            y += h-1
        elif vertical in ['center','middle','c','m','cen','mid']:
            y += (h-1)//2
        else:
            raise ValueError("Vertical value incorrect try 'top', 'bottom' or 'middle'")
        
        if horizontal in ['left','l']:
            return Write.leftAt(x,y, string, style)
        elif horizontal in ['center','middle','mid','cen','c','m']:
            return Write.centerAt(x,y,w, string, style)
        elif horizontal in ['right','r']:
            return Write.rightAt(x,y,w, string, style)
        elif horizontal in ['justify','j']:
            return Write.justifyAt(x,y,w, string, style)
        else:
            raise ValueError("Horizontal value incorrect try 'left', 'center' or 'right'")

    def leftIn(x,y,h, string, vertical='top', style=''):
        return Write.into(x,y,-1,h, string, 'left', vertical, style)
    
    def centerIn(x,y,w,h, string, vertical='top', style=''):
        return Write.into(x,y,w,h, string, 'center', vertical, style)
    
    #TODO rightIn, centerIn, justifyIn short cut function to use into()

    def paragraph(x,y,w,h, string_list, horizontal,vertical='top', style=''):
        if len(string_list)>h:
            raise ValueError("Your paragraphe is larger than the text zone height")

        if vertical in ['top','t']:
            pass
        elif vertical in ['bottom','b','bot']:
            y += h-len(string_list)
        elif vertical in ['center','middle','c','m','cen','mid']:
            y += (h-len(string_list))//2
        else:
            raise ValueError("Vertical value incorrect try 'top', 'bottom' or 'middle'")

        screen = ''
        i=0
        for line in string_list:
            screen += Write.into(x,y+i,w,h, line, horizontal,'top', style)
            i += 1
        
        return screen

    

    def lnTolns(w, string, word_cut=False):
        #TODO add unbreakable space between word and punctuation
        words = string.split(' ')
        lines = []
        currWord = 0
        nextWord = words[currWord]
        l = 0
        lw = w
        end = False
        while not end:
            # Calculate remaining space in line l
            # Create line if not exists or line full
            if l < len(lines):
                lw = w-len(lines[l])
                if lw == 0:
                    l += 1

            if l >= len(lines):
                lw = w
                lines.append('')

            

            # IF word or part larger than remaining space
            # AND cut word forbidden
            if(len(nextWord) > lw and not word_cut):
                # WORD is bigger than space
                if len(nextWord)>w:
                    l += 1
                    lines.append(nextWord[0:w])
                # OR word only bigger than remaining space
                else:
                    l += 1
                    if len(nextWord)!=w:
                        lines.append(nextWord+' ')
                    else:
                        lines.append(nextWord)
                
                currWord += 1 

            # IF word or part larger than remaining space
            # AND cut word allowed
            elif(len(nextWord) > lw and word_cut):
                lines[l] += nextWord[0:lw-1]+'-'
                nextWord = nextWord[lw-1:]
                continue

            # word or part exactly fit in remainnig space
            elif(len(nextWord) == lw):
                lines[l] += nextWord
                currWord += 1

            # word fit in remaining space
            elif(len(nextWord) < lw):
                lines[l] += nextWord + ' '
                currWord += 1

            if currWord < len(words):
                nextWord = ''
                while nextWord=='':
                    nextWord = words[currWord]
                    currWord += 1 if nextWord == '' else 0
            else:
                end = True

        return lines

    # PADDING left,right,top,bottom(pl,pr,pt,pb) of parent(x,y,w,h)
    # Make child (x+1+pl, y+1+pt, w-2-pl-pr, h-2-pt-pb)
    # OR padding 0 forbidden (because remove box which have same coordidates)
    # And then child(x+pl, y+pt, w-pl-pr, h-pt-pb) and default padding = 1