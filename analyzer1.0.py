from tkinter import *
from tkinter import ttk
import scipy.misc
from tkinter.filedialog import askopenfilename
import pygame
from PIL import Image
import matplotlib.pyplot as plt


global d1, d2
white = (255, 255, 255)
w = 800
h = 800
black = (0, 0, 0)
b_x = 0
b_y = 0
d1 = []
d2 = []
gr = []
r = []
g = []
b = []
bl=[]




def main_menu():
    global root, screen_width, screen_height
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry('600x400'+'+'+str(int(screen_width/2)-300)+"+"+str(int(screen_height/2)-400))
    s = ttk.Style()
    s1 = ttk.Style()
    s.configure('my.TButton', font=('Arial', 30))
    s1.configure('my.TLabel', font=('Arial', 30))
    lb_h = ttk.Label(root, text="Анализатор спекстра", style='my.TLabel').place(x=100, y=20)
    upload = ttk.Button(root, text="Загрузить изображение", style='my.TButton', command=open_img).place(x=70, y=100)
    calibrate = ttk.Button(root, text="Калибровка", style='my.TButton').place(x=170, y=190)
    root.mainloop()


def move_line():
    global d1, d2
    x_m, y_m = pygame.mouse.get_pos()
    d1[1] = y_m
    d2[1] = y_m


def open_img():
    global d1, d2, root, filename
    root.withdraw()
    filename = askopenfilename()
    img = Image.open(filename)
    if img.size[0] > img.size[1]:
        new_width = 780
        new_height = int(780 * img.size[1] / img.size[0])
        b_x = 10
        b_y = int((800 - new_height) / 2)
        d1 = [b_x, 400]
        d2 = [b_x + new_width, 400]
        max_d = [b_y, b_y + new_height]
    else:
        new_height = 780
        new_width = int(780 * img.size[0] / img.size[1])
        b_y = 10
        b_x = int((800 - new_width) / 2)
        d1 = [b_x, 400]
        d2 = [b_x + new_width, 400]
        max_d = [b_y, b_y + new_height]
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    mode = img.mode
    size = img.size
    data = img.tobytes()
    img_p = pygame.image.fromstring(data, size, mode)
    screen = pygame.display.set_mode((w, h))
    screen.fill(white)
    done = False
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    if ((d1[1] - 5) < y_m < (d1[1] + 5)) and (d1[0] < x_m < d2[0]):
                        line_d = 1
                if pygame.mouse.get_pressed()[2] == 1:
                    root.deiconify()
                    pygame.quit()
                    draw_grath()
        screen.fill(white)
        x_m, y_m = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 0:
            line_d = 0
        if line_d == 1 and max_d[0] < d1[1] < max_d[1]:
            move_line()
        screen.blit(img_p, (b_x, b_y))
        if d1[1] > max_d[1] - 5:
            d1[1] = max_d[1] - 5
            d2[1] = max_d[1] - 5
        elif d1[1] < max_d[0] + 5:
            d1[1] = max_d[0] + 5
            d2[1] = max_d[0] + 5
        pygame.draw.line(screen, black, [d1[0], d1[1]], [d2[0], d2[1]], 2)
        pygame
        pygame.display.flip()
        clock.tick(60)
    root.deiconify()
    pygame.quit()


def draw_grath():      ##76845656

    im = scipy.misc.imread(filename, flatten=False, mode='RGB')
    img = Image.open(filename)
    for i in range(300):
        m= list(im[d1[0]][i*round(img.size[0]/300)])
        r.append(m[0]/100)
        g.append(m[1]/100)
        b.append(m[2]/100)
        bl.append((m[0]+m[1]+m[2])/300)
    x=[]
    for i in range(300):
        x.append(i+400)
    plt.plot(x, r, 'r')
    plt.plot(x, g, 'g')
    plt.plot(x, b, 'b')
    plt.plot(x, bl, "black")

    plt.show()

main_menu()
