from tkinter import *

from gui.interactive_window import InteractiveWindow
from lib.figures import Cube, Prism, Pyramid, Tetrahedron

pyramid = Pyramid(None, size=200, x_offset=40)
cube = Cube(None, size=200, x_offset=40, y_offset=240)
prism = Prism(None, size=140, x_offset=0, y_offset=180)
tetrahedron = Tetrahedron(None, size=200, x_offset=70, y_offset=210)

figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}


def main():
    root = Tk()
    ex = InteractiveWindow(root, figures)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
