import sys

class Canvas:
    def __init__(self):
        self.rows=10
        self.columns=10
        self.cells = {(r,c):None for r in range(1,self.rows+1) for c in range(1,self.columns+1)}
        for i in range(3,6):
            self.cells[(i,5)] = 1
            self.cells[(i,8)] = 1
        for i in range(5,8):
            self.cells[(3,i)] = 1
            self.cells[(6,i)] = 1

    def display(self):
        for i in range(1,self.rows):
            for j in range(1,self.columns):
                sys.stdout.write("*" if self.cells[(i,j)] else " ")
            sys.stdout.write("\n")


    def fill(self, x, y, t):
        if not self.cells[(x,y)]:
            to_fill = [(x,y)]
            while to_fill:
                # pick a point from the queue
                x,y = to_fill.pop()
                # change color if possible
                self.cells[(x,y)] = t

                # now the neighbours x,y +- 1
                for delta_x in range(-1,2):
                    xdx = x+delta_x
                    if xdx > 0 and xdx < self.columns+1:
                        for delta_y in range(-1,2):
                            ydy = y+delta_y
                            # avoid diagonals
                            if (delta_x == 0) ^ (delta_y == 0):
                                if ydy > 0 and ydy < self.rows+1:
                                    # valid x+delta_x,y+delta_y
                                    # push in queue if no color
                                    if not self.cells[(xdx,ydy)]:
                                        to_fill.append((xdx,ydy))

c = Canvas()
c.display()
c.fill(4,6,2)
c.display()