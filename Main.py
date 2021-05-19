from tkinter import *
from Figures import Cube, Prism, Pyramid, Tetrahedron
from PIL import ImageGrab
import datetime

images_amount = 0


class Program:
    def __init__(self, root, window_width=400, window_height=540, canvas_width=400, canvas_height=350):
        self.width = window_width
        self.height = window_height
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.figure = None

        self.root_window = root
        self.root_window.geometry(f'{self.width}x{self.height}')
        self.root_window.configure(bg='white')

        self.root_canvas = Canvas(self.root_window, width=self.canvas_width, height=self.canvas_height, bg='#f3f3f3')
        self.root_canvas.pack(side=BOTTOM)
        self.widgets = []

    def render_window(self):
        self.root_canvas.delete('all')
        for el in self.widgets:
            el.destroy()
        self.widgets.clear()

        if self.figure is not None:
            self.figure.render()
            self.root_canvas.update()

        b_figure = Button(text="Change figure to:")
        b_figure.place(relwidth=0.3, relheight=0.1)
        b_figure['command'] = lambda: self.change_figure_to(figures[list_figures.get(list_figures.curselection()[0])])
        self.widgets.append(b_figure)

        list_figures = Listbox()
        for figure in figures.keys():
            list_figures.insert(END, figure)
        list_figures.place(relwidth=0.3, relheight=0.1, relx=0.31)
        self.widgets.append(list_figures)

        list_sections = Listbox()
        try:
            for section in self.figure.sections:
                list_sections.insert(END, section[0])
        except AttributeError:
            pass
        list_sections.place(relwidth=0.3, relheight=0.1, relx=0.31, rely=0.12)
        self.widgets.append(list_sections)

        b_dot = Button(text='Add dot to:')
        b_dot.place(relwidth=0.3, relheight=0.1, rely=0.12)
        b_dot['command'] = lambda: self.add_dot(list_sections.get(list_sections.curselection()[0]),
                                                prop=float(proportion.get()))
        self.widgets.append(b_dot)

        b_clear = Button(text='Clear dots')
        b_clear.place(relwidth=0.3, relheight=0.1, relx=0.62)
        b_clear['command'] = lambda: self.clear_dots()
        self.widgets.append(b_clear)

        proportion = Spinbox(values=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
        proportion.delete(0, "end")
        proportion.insert(0, '0.5')
        proportion.place(rely=0.12, relx=0.62, relwidth=0.3)
        self.widgets.append(proportion)

        scrollbar = Scrollbar()
        scrollbar.place(relwidth=0.05, relheight=0.1, relx=0.56, rely=0.12)
        list_sections.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=list_sections.yview)
        self.widgets.append(scrollbar)

        b_cross = Button(text='Cross')
        b_cross.place(relwidth=0.3, relheight=0.1, relx=0.62, rely=0.17)
        b_cross['command'] = lambda: self.cross_with_plain()
        self.widgets.append(b_cross)

        w2 = Scale(from_=0, to=90, tickinterval=30, orient=HORIZONTAL)
        try:
            w2.set(self.figure.projecting_angle)
        except AttributeError:
            w2.set(45)
        w2.place(relwidth=0.6, relheight=0.12, rely=0.22, relx=0.01)
        w2.bind("<ButtonRelease>", lambda x: self.figure.set_angle(w2.get()))
        self.widgets.append(w2)

        save_b = Button(text='↓')
        save_b.place(relx=0.75, rely=0.28, relwidth=0.05, relheight=0.05)
        save_b['command'] = lambda: self.getter()
        self.widgets.append(save_b)

    def change_figure_to(self, fig):
        if self.figure is not None:
            self.figure.parent = None
        fig.parent = self
        self.figure = fig
        self.render_window()

    def add_dot(self, section, prop=0.5):
        if self.figure is not None:
            self.figure.add_dot_on_section(section, prop)
            self.render_window()
        else:
            print('<Error> figure is not declared')

    def getter(self):
        global images_amount
        x = self.root_window.winfo_rootx() + self.root_canvas.winfo_x()
        y = self.root_window.winfo_rooty() + self.root_canvas.winfo_y()
        x1 = x + self.root_canvas.winfo_width()
        y1 = y + self.root_canvas.winfo_height()
        today = datetime.datetime.today()
        ImageGrab.grab().crop((x, y, x1, y1)).save(f"downloaded_images/{images_amount}-({today.day}-{today.month}).jpg")
        print(f"successfully loaded '{images_amount}-({today.day}-{today.month}).jpg'")
        images_amount += 1

    def clear_dots(self):
        self.figure.added_dots.clear()
        self.figure.secant_plain = None
        self.figure.plain_crossing_points.clear()
        self.figure.additional_dots.clear()
        self.render_window()

    def cross_with_plain(self):
        if self.figure is None:
            print('<Error> figure is not defined')
            return None
        self.figure.cross_figure_with_plain()
        self.render_window()


pyramid = Pyramid(None, size=220, x_move=65, y_move=240)
cube = Cube(None, size=200, x_move=65, y_move=260)
prism = Prism(None, size=140, x_move=20, y_move=200)
tetrahedron = Tetrahedron(None, size=240, x_move=70, y_move=210)

cube.added_dots = {'α': (100.0, 200.0, 200.0), 'β': (0.0, 100.0, 200.0), 'γ': (0.0, 200.0, 100.0)}

figures = {'Cube': cube, 'Pyramid': pyramid, 'Prism': prism, 'Tetrahedron': tetrahedron}


def main():
    root = Tk()
    ex = Program(root)
    ex.render_window()
    root.mainloop()


if __name__ == '__main__':
    main()
