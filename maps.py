from line import Line

def mapPrecooked():
    '''These lines are pre-calculated.  Can only be used with the manual method in the BinaryTree class.'''
    color1 = (222,0,0)
    color2 = (80, 0, 0)
    walls = [Line(160,120,240,120, color=color1),
             Line(240,120,240,200, color=color2),
             Line(240,200,160,200, color=color1),
             Line(160,200,160,120, color=color2),
             Line(560,40,40,40, color=color1),
             Line(560,120,560, 40, color=color2),
             Line(560,360,560,120, color=color2),
             Line(240,360,560,360, color=color1),
             Line(40,360,240,360, color=color1),
             Line(40,200,40,360, color=color2),
             Line(40,120,40,200, color=color2),
             Line(40,40,40,120, color=color2)]
    return walls

def mapRaw():
    '''These lines are not pre-calculated.  BinaryTree will try to perform the necessary calculations.'''
    color1 = (222,0,0)
    color2 = (80, 0, 0)
    walls = [Line(160,120,240,120, color=color1),
             Line(240,120,240,200, color=color2),
             Line(240,200,160,200, color=color1),
             Line(160,200,160,120, color=color2),
             Line(560,40,40,40, color=color1),
             Line(560,360,560, 40, color=color2),
             Line(40,360,560,360, color=color1),
             Line(40,40,40,360, color=color2)]

    return walls
