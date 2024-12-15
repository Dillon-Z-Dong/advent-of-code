import numpy as np

def load_map(file, movement_file):
    with open(file) as f:
        warehouse_map = np.array([list(x.strip()) for x in f.readlines()])

    with open(movement_file) as f:
        lines = [x.strip() for x in f.readlines()]
        movement = list(''.join(lines))

    return warehouse_map, movement

def p1(mp,mvmt):
    """Solution for part 1"""
    print('Initial condition:')
    _print(mp)
    print()

    robot = np.where(mp == '@')
    for i, m in enumerate(mvmt):
        nextobj, nextpos = check(robot,m,mp)
        #print(f'{i}: {nextobj = }, {nextpos = }')

        if nextobj == '#': #wall
            pass #no movement, no shift

        elif nextobj == '.': #free space
            mp[nextpos] = '@'
            mp[robot] = '.'
            robot = nextpos

        elif nextobj == 'O':
            #boxpos_list = [nextpos]
            first_boxpos = nextpos
            nextobj_is_box = True

            current_pos = (robot[0],robot[1])
            while nextobj_is_box:
                #print(f'{current_pos = }')
                nextobj, nextpos = check(current_pos,m,mp)
                #print(f'{nextpos = }')
                if nextobj == '#':
                    nextobj_is_box = False
                    #print('Hit wall')
                    break

                elif nextobj == '.': #push everything which amounts to shifting the first box to the end
                    mp[nextpos] = 'O'
                    mp[first_boxpos] = '@'
                    mp[robot] = '.'
                    robot = first_boxpos
                    nextobj_is_box = False
                    #print('Moved stack')
                    break

                elif nextobj == 'O':
                    current_pos = nextpos
                    #print(f'Setting current_pos {current_pos} to {nextpos}')

                else:
                    raise Exception(f'Could not identify {nextobj}')
                
        #print(f'Move {m}:')
        #_print(mp)
        #print()

    print('Final map: ')
    _print(mp)
    print(f'\nGPS score: {gps(mp)}')
    return

def p2(mp,mvmt):
    """Solution for part 2. 
    Pretty hacky, should really have written a class with box objects, footprint attrs, etc."""

    mp, new_walls, new_box_left, new_box_right, robot = double_map(mp)
    
    print('Initial map:')
    _print(mp)
    print()


    for i, m in enumerate(mvmt):
        nextobj, nextpos = check(robot,m,mp)
        #print()
        #print('-'*50)
        #print(f'Iteration {i}: {m = }, {nextobj = }, {robot[0],robot[1]} --> {nextpos[0],nextpos[1]}')
        #print('Current map:')
        #_print(mp)
        #print()

        if nextobj == '#': #robot directly hitting wall
            pass #no movement, no shift

        elif nextobj == '.': #robot moving into free space
            mp[nextpos] = '@'
            mp[robot] = '.'
            robot = nextpos

        elif nextobj in ['[',']']:
            box_list = [(nextobj,nextpos)]
            box_list.append(gobp(nextobj,nextpos)) #add the other box part to the list to be shifted
            
            lbpp = [] #leading box part positions to check for wall hits
            if m == '<':
                lbpp.append((nextpos[0],nextpos[1]-1)) #just the left edge
            elif m == '>':
                lbpp.append((nextpos[0],nextpos[1]+1)) #just the right edge
            else:
                lbpp = [x[1] for x in box_list] #vertical movement means leading parts are both initial box parts

            #print(f'Initialized {lbpp = }')

            nextobj_is_box = True
            while nextobj_is_box:
                clear_space_ahead = []

                for current_pos in lbpp.copy(): #check ahead of everything in leading edge
                    #print(f'{current_pos = }')
                    nextobj, nextpos = check(current_pos,m,mp)
                    #print(f'{nextpos = }')

                    if nextobj == '#': 
                        nextobj_is_box = False
                        clear_space_ahead.append(False)
                        #print('Hit wall')


                    elif nextobj in ['[',']']:
                        clear_space_ahead.append(False)

                        lbpp.remove(current_pos) #current position has been superceded
    
                        # Add both components of the next box to the box list if they are not doublecounting
                        other_part, other_pos = gobp(nextobj,nextpos)
                        for p in [(nextobj,nextpos),(other_part,other_pos)]:
                                if p not in box_list:
                                    box_list.append(p) 
                        if m in ['^','v']:
                            lbpp.append(nextpos)
                            lbpp.append(other_pos)
                            #print(f'---> Added {nextpos},{other_pos} to lbpp from {current_pos = }')

                        elif m == '<':
                            lbpp.append((current_pos[0],current_pos[1]-2))

                        elif m == '>':
                            lbpp.append((current_pos[0],current_pos[1]+2))


                    elif nextobj == '.': 
                        clear_space_ahead.append(True)

                if np.all(clear_space_ahead): #[] evaluates to True
                
                    #push everything iteratively
                    #print(f'Pushing box components: {box_list}')
                    newly_added = [] # make sure not to clear newly added components
                    for j, box in enumerate(box_list):
                        obj,pos = box
                        if j == 0:
                            mp[pos] = '@' #replace first component with robot
                            mp[robot] = '.'
                            robot = pos
                            #print(f'Moved robot to {robot}')

                        if m == '<':
                            newpos = (pos[0],pos[1]-1)
                        elif m == '>':
                            newpos = (pos[0],pos[1]+1)
                        elif m == '^':
                            newpos = (pos[0]-1,pos[1])
                            if j%2==1 and pos not in newly_added:
                                mp[pos] = '.' #clear second box component
                                #print(f'^ Cleared second box component at {pos}')
                        elif m == 'v':
                            newpos = (pos[0]+1,pos[1])
                            if j%2==1 and pos not in newly_added:
                                mp[pos] = '.' #clear second box component
                                #print(f'v Cleared second box component at {pos}')

                        mp[newpos] = obj
                        newly_added.append(newpos)
                        #print(f'Pushed {obj} from {pos} to {newpos}')

                    #print('Moved stack')
                    nextobj_is_box = False
                    break

        else:
            raise Exception(f'Could not identify {nextobj}')
                

    print('Final map: ')
    _print(mp)
    print(f'\nGPS score: {gps(mp,char='[')}')
    return

def check(pos, m, mp):
    d = {'<':(0,-1),'^':(-1,0),'>':(0,1),'v':(1,0)}
    dy,dx = d[m]
    y,x = pos
    nextpos = (y+dy,x+dx)
    return mp[nextpos][0], nextpos

def gps(mp, char = 'O'):
    by,bx = np.where(mp == char)
    return 100*np.sum(by) + np.sum(bx)

def double_map(mp):
    # Create new doubled map
    shapey,shapex = np.shape(mp)
    newmp = np.full((shapey, 2*shapex),'.')

    # Create new walls
    wally,wallx= np.where(mp == '#')
    new_walls = (np.concatenate([wally,wally]),np.concatenate([2*wallx,2*wallx+1]))
    newmp[new_walls] = '#'

    # Create new boxes
    boxy,boxx = np.where(mp == 'O')
    new_box_left = (boxy,2*boxx)
    new_box_right = (boxy,2*boxx+1)
    newmp[new_box_left] = '['
    newmp[new_box_right] = ']'

    # Put our fren back on the map
    ry,rx = np.where(mp == '@')
    robot = ((ry,2*rx))
    newmp[robot] = '@'

    return newmp, new_walls, new_box_left, new_box_right, robot


def gobp(part,pos):
    '''Get other box part'''
    if part == '[':
        return (']',(pos[0],pos[1]+1))
    else:
        return ('[',(pos[0],pos[1]-1))

def _print(mp):
    for row in mp:
        print(''.join(row))

if __name__ == '__main__':
    test_map, test_mvmt = load_map(f'test_data_day15.txt','test_movement.txt')
    real_map, real_mvmt = load_map(f'data_day15.txt','real_movement.txt')
    

    p1(real_map, real_mvmt)
    p2(real_map, real_mvmt)



