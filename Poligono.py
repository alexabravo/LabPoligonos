import struct 

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(red, green, blue):
     return bytes([round(blue * 255), round(green * 255), round(red * 255)])

class Render(object):

    def glinit(self, width, height):
        self.width = width
        self.height = height
        self.wVP = width
        self.hVP = height
        self.xVP = 0
        self.yVP = 0
        self.clear_color = color(1,1,1)
        self.framebuffer = []
        self.glClear()

    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewPort(self, xVP, yVP,  wVP, hVP):
        self.xVP = xVP
        self.yVP = yVP
        self.hVP = hVP
        self.wVP = wVP

    def glClearColor(self, red,blue,green):
        self.clear_color = color(red,blue,green)

    def glColor(self, red, green, blue):
        self.clear_color = color(red, green, blue)

    def glpoint(self, x, y):
        self.framebuffer[y][x] = self.clear_color

    def glVertex(self, x, y):
        xVer = round((x + 1) * (self.wVP/ 2) + self.xVP)
        yVer = round((y + 1) * (self.hVP/2) + self.yVP)
        self.glpoint(round(xVer), round(yVer))

    def glLine(self, x1, y1, x2, y2):
        x1 = round((x1 + 1) * (self.wVP * 0.5) + self.xVP)
        y1 = round((y1 + 1) * (self.hVP * 0.5) + self.yVP)
        x2 = round((x2 + 1) * (self.wVP * 0.5) + self.xVP)
        y2 = round((y2 + 1) * (self.hVP * 0.5) + self.yVP)
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dy = abs(y2 - y1)
            dx = abs(x2 - x1)
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            
        offset = 0
        threshold = 1
        y = y1
        for x in range(x1, x2):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx

    def glInside(self, x,y,points):
        long  = len(points)
        a = 0
        b = long - 1
        Inside = False

        for a in range(long):
            if ((points[a][1] > y) != (points[b][1] >y )) and (x < points[a][0] + (points[b][0] - points[a][0]) * (y - points[a][1])/(points[b][1] - points[a][1])):
                Inside = not Inside
            b = a
        return Inside

    
    def glPolygon(self, points):
        for x in range(self.width):
            for y in range(self.height):
                if(self.glInside(x,y,points)):
                    self.glpoint(x,y)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
          for y in range(self.width):
            f.write(self.framebuffer[x][y])

        f.close()
        
#Poligonos        
un = [(165, 380),(185, 360),(180, 330),(207, 345),(233, 330),(230, 360),(250, 380),(220, 385),(205, 410),(193, 383)]
deux = [(321, 335),(288, 286),(339, 251),(374, 302)]
trois = [(377, 249),(411, 197),(436, 249)]
quatre = [(413, 177), (448, 159),(502, 88),(553, 53),(535, 36),(676, 37),(660, 52),(750, 145),(761, 179),(672, 192),(659, 214),(615, 214),(632, 230),(580, 230),(597, 215),(552, 214),(517, 144),(466, 180)]
cinq = [(682, 175),(708, 120),(735, 148),(739, 170)]       

bitmap = Render()
bitmap.glCreateWindow(800, 800)
bitmap.glClearColor(0, 0, 0)
bitmap.glClear()

bitmap.glColor(0.6, 0.250, 0.5)
bitmap.glPolygon(un)

bitmap.glColor(0.97,0.56,0)
bitmap.glPolygon(deux)

bitmap.glColor(0.19,0.76,0.84)
bitmap.glPolygon(trois)

bitmap.glColor(0.75, 0.250, 0.5)
bitmap.glPolygon(quatre)

bitmap.glColor(0,0,0)
bitmap.glPolygon(cinq)

bitmap.glFinish('Poligonooo.bmp')

    
