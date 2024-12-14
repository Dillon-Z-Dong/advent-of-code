import numpy as np
from parse import *
from PIL import Image
import matplotlib.pyplot as plt
import os
import time

def load(file):
    """Load input as list of strings"""
    with open(file) as f:
        lines = [parse('p={},{} v={},{}',x.strip()) for x in f.readlines()]

    px, py, vx, vy = [],[],[],[]
    for line in lines: 
        a,b,c,d = [int(x) for x in line]
        px.append(a)
        py.append(b)
        vx.append(c)
        vy.append(d)

    return px,py,vx,vy


def p1(data, dims):
    """Solution for part 1"""
    px_arr,py_arr,vx_arr,vy_arr = data
    robots = []
    for i, x in enumerate(px_arr):
        y = py_arr[i]
        vx = vx_arr[i]
        vy = vy_arr[i]
        robot = (x,y,vx,vy)
        robots.append(robot)

    def evolve(robots,dims, niter = 100):
        arr = np.zeros(dims)
        by,bx = dims
        for robot in robots:
            x,y,vx,vy = robot
            for i in range(niter):
                x = (x+vx)%bx
                y = (y+vy)%by
            arr[y][x] += 1

        q1 = arr[:by//2,:bx//2]
        q2 = arr[:by//2,bx//2+1:]
        q3 = arr[by//2+1:,:bx//2]
        q4 = arr[by//2+1:,bx//2+1:]
        quadrant_product = int(np.prod([np.sum(x) for x in [q1,q2,q3,q4]]))
        print(f'(P1) Product of quadrant sums: {quadrant_product}')
        return arr, quadrant_product

    a = evolve(robots, dims = dims, niter = 100)
    return a

def p2(data, dims, niter):
    """Solution for part 2"""
    px_arr,py_arr,vx_arr,vy_arr = data
    robots = []
    for i, x in enumerate(px_arr):
        y = py_arr[i]
        vx = vx_arr[i]
        vy = vy_arr[i]
        robot = [x,y,vx,vy] #use list for mutability
        robots.append(robot)

    def evolve2(robots,dims, niter):
        os.makedirs('./frames', exist_ok = True)
        arr = np.zeros(dims)
        for robot in robots:
            x,y,vx,vy = robot
            arr[y][x] += 1

        by,bx = dims
        
        occupied = []
        #frame = np.zeros_like(arr).astype(np.uint8)
        for i in range(1,niter+1):
            for robot in robots:
                x,y,vx,vy = robot
                arr[y][x] -= 1
                x = (x+vx)%bx
                y = (y+vy)%by
                robot[0], robot[1] = x,y #update state of robots
                arr[y][x] += 1

            if i == 100:
                q1 = arr[:by//2,:bx//2]
                q2 = arr[:by//2,bx//2+1:]
                q3 = arr[by//2+1:,:bx//2]
                q4 = arr[by//2+1:,bx//2+1:]
                quadrant_product = int(np.prod([np.sum(x) for x in [q1,q2,q3,q4]]))
                #print(f'p2 index validated: {quadrant_product - 217132650 == 0}')
            
            # save np.where(arr) as image in ./frames



            #print(f'Frame {i} has {n_occupied} occupied pixels!')
            frame = arr
            frame = frame - frame.min()
            frame = (frame / frame.max() * 255).astype(np.uint8)

            bright = np.where(frame > 200)
            n_bright = len(bright[0])
            occupied.append(n_bright)

            if n_bright > 30: #500 bright in the christmas tree frame, 38 in the next highest. Illustrating the noise here.
                filepath = f'./frames/iter_{i}_nbright_{n_bright}.jpg'
                img = Image.fromarray(frame)
                img.save(filepath)

        return occupied

    occupied = evolve2(robots, dims = dims, niter = niter)

    return occupied




if __name__ == '__main__':
    # Choose appropriate load function after seeing the input
    test = load(f'test_data_day14.txt')
    real = load(f'data_day14.txt')
    test_dims = (7,11) #11 wide, 7 tall
    real_dims = (103,101) #101 wide, 103 tall

    p1(real,real_dims)
    occupied = p2(real, real_dims, niter = 103*101) # max possible is 103*101 since x and y are independent and everything repeats after this cycle by the pigeonhole principle
    print(f'(P2) Frame with the most bright pixels: {np.argmax(occupied)+1}')



"""

# Can probably make a more efficient solution using this

def compute_position_cycle(robot,dims):
    '''
    Computes the position from initial position (x0,y0) 
    with velocity (vx,vy) modulo the bounds

    Position must be periodic (repeat) in both x and y by the pigeonhole principle
    Period in both x and y is exactly 101 and 103 because both are prime
    '''
    by,bx = dims
    x,y,vx,vy = robot

    posx = []
    posy = []

    for i in range(max(dims)):
        x = (x+vx)%bx
        y = (y+vy)%by

        if i < bx:
            posx.append(x)

        if i < by:
            posy.append(y)


    return posx, posy

"""
