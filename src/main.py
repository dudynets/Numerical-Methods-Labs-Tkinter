import tkinter

import customtkinter
import matplotlib
import seaborn
from matplotlib import pyplot as plt

from methods.interpolation.lagrange_interpolation import LagrangeInterpolationPage
from methods.interpolation.newtons_interpolation import NewtonsInterpolationPage
from methods.linear_systems.fixed_point_system import FixedPointSystemPage
from methods.linear_systems.gaussian_method import GaussianMethodPage
from methods.linear_systems.least_squares import LeastSquaresPage
from methods.non_linear.fixed_point_iteration_method import (
    FixedPointIterationMethodPage,
)
from methods.non_linear.newtons_method import NewtonsMethodPage
from methods.non_linear.secant_method import SecantMethodPage
from src.methods.integration.rectangles import RectanglesMethodPage
from src.methods.integration.simpsons import SimpsonsMethodPage
from src.methods.integration.trapezoidal import TrapezoidalMethodPage

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def init_matplotlib():
    matplotlib.use("QtAgg")
    seaborn.set_style("whitegrid")


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Чисельні методи")
        self.geometry("1000x600")
        self.minsize(1000, 600)

        init_matplotlib()
        center_window(self, 1000, 600)

        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True)

        self.right_panel = RightSidePanel(main_container)
        self.right_panel.pack(
            side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True, padx=(0, 10), pady=10
        )

        self.left_panel = NavigationPanel(main_container, self.right_panel)
        self.left_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=10, pady=10)

        self.left_panel.show_newtons_page()


class NavigationPanel(customtkinter.CTkScrollableFrame):
    def __init__(self, master, right_panel):
        super().__init__(master, corner_radius=10, width=240)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.right_panel = right_panel
        self.active_button = None

        self.title_label = customtkinter.CTkLabel(
            self,
            text="Чисельні методи",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(row=0, padx=10, pady=10)
        self.title_label.grid_configure(sticky="w")

        # Non-linear equations

        self.non_linear_label = customtkinter.CTkLabel(
            self,
            text="Нелінійні рівняння:",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.non_linear_label.grid(row=1, padx=10, pady=10)
        self.non_linear_label.grid_configure(sticky="w")

        self.newtons_button = customtkinter.CTkButton(
            self, text="Метод Ньютона", command=self.show_newtons_page
        )
        self.newtons_button.grid(row=2, padx=10, pady=10)
        self.newtons_button.grid_configure(sticky="we")

        self.secant_button = customtkinter.CTkButton(
            self, text="Метод хорд", command=self.show_secant_page
        )
        self.secant_button.grid(row=3, padx=10, pady=10)
        self.secant_button.grid_configure(sticky="we")

        self.fixed_point_button = customtkinter.CTkButton(
            self, text="Метод простої ітерації", command=self.show_fixed_point_page
        )
        self.fixed_point_button.grid(row=4, padx=10, pady=10)
        self.fixed_point_button.grid_configure(sticky="we")

        # Linear systems

        self.linear_systems_label = customtkinter.CTkLabel(
            self,
            text="Системи лінійних рівнянь:",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.linear_systems_label.grid(row=5, padx=10, pady=10)
        self.linear_systems_label.grid_configure(sticky="w")

        self.gaussian_button = customtkinter.CTkButton(
            self, text="Метод Гауса", command=self.show_gaussian_page
        )
        self.gaussian_button.grid(row=6, padx=10, pady=10)
        self.gaussian_button.grid_configure(sticky="we")

        self.least_squares_button = customtkinter.CTkButton(
            self, text="Метод найменших квадратів", command=self.show_least_squares_page
        )
        self.least_squares_button.grid(row=7, padx=10, pady=10)
        self.least_squares_button.grid_configure(sticky="we")

        self.fixed_point_system_button = customtkinter.CTkButton(
            self,
            text="Метод простої ітерації",
            command=self.show_fixed_point_system_page,
        )
        self.fixed_point_system_button.grid(row=8, padx=10, pady=10)
        self.fixed_point_system_button.grid_configure(sticky="we")

        # Interpolation

        self.interpolation_label = customtkinter.CTkLabel(
            self,
            text="Інтерполяція:",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.interpolation_label.grid(row=9, padx=10, pady=10)
        self.interpolation_label.grid_configure(sticky="w")

        self.newtons_interpolation_button = customtkinter.CTkButton(
            self, text="Метод Ньютона", command=self.show_newtons_interpolation_page
        )
        self.newtons_interpolation_button.grid(row=10, padx=10, pady=10)
        self.newtons_interpolation_button.grid_configure(sticky="we")

        self.lagrange_interpolation_button = customtkinter.CTkButton(
            self, text="Метод Лагранжа", command=self.show_lagrange_interpolation_page
        )
        self.lagrange_interpolation_button.grid(row=11, padx=10, pady=10)
        self.lagrange_interpolation_button.grid_configure(sticky="we")

        # Integration

        self.integration_label = customtkinter.CTkLabel(
            self,
            text="Інтегрування:",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.integration_label.grid(row=12, padx=10, pady=10)
        self.integration_label.grid_configure(sticky="w")

        self.rectangles_button = customtkinter.CTkButton(
            self, text="Метод прямокутників", command=self.show_rectangles_page
        )
        self.rectangles_button.grid(row=13, padx=10, pady=10)
        self.rectangles_button.grid_configure(sticky="we")

        self.trapezoidal_button = customtkinter.CTkButton(
            self, text="Метод трапецій", command=self.show_trapezoidal_page
        )
        self.trapezoidal_button.grid(row=14, padx=10, pady=10)
        self.trapezoidal_button.grid_configure(sticky="we")

        self.simpsons_button = customtkinter.CTkButton(
            self, text="Метод Сімпсона", command=self.show_simpsons_page
        )
        self.simpsons_button.grid(row=15, padx=10, pady=10)
        self.simpsons_button.grid_configure(sticky="we")

        self.quit_button = customtkinter.CTkButton(
            self,
            text="Вийти",
            fg_color="#EA0000",
            hover_color="#B20000",
            command=master.quit,
        )
        self.quit_button.grid(row=16, padx=10, pady=10)
        self.quit_button.grid_configure(sticky="we")

    def show_newtons_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.newtons_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_newtons_page()

    def show_secant_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.secant_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_secant_page()

    def show_fixed_point_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.fixed_point_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_fixed_point_page()

    def show_gaussian_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.gaussian_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_gaussian_page()

    def show_least_squares_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.least_squares_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_least_squares_page()

    def show_fixed_point_system_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.fixed_point_system_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_fixed_point_system_page()

    def show_newtons_interpolation_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.newtons_interpolation_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_newtons_interpolation_page()

    def show_lagrange_interpolation_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.lagrange_interpolation_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_lagrange_interpolation_page()

    def show_rectangles_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.rectangles_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_rectangles_page()

    def show_trapezoidal_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.trapezoidal_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_trapezoidal_page()

    def show_simpsons_page(self):
        plt.close("all")

        if self.active_button:
            self.active_button.configure(state="normal")

        self.active_button = self.simpsons_button
        self.active_button.configure(state="disabled")
        self.right_panel.show_simpsons_page()


class RightSidePanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color="#000811")
        self.current_page = None

    def show_newtons_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = NewtonsMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_secant_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = SecantMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_fixed_point_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = FixedPointIterationMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_gaussian_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = GaussianMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_least_squares_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = LeastSquaresPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_fixed_point_system_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = FixedPointSystemPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_newtons_interpolation_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = NewtonsInterpolationPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_lagrange_interpolation_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = LagrangeInterpolationPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_rectangles_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = RectanglesMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_trapezoidal_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = TrapezoidalMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

    def show_simpsons_page(self):
        if self.current_page:
            self.current_page.destroy()
            self.current_page.pack_forget()

        self.current_page = SimpsonsMethodPage(self)
        self.current_page.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
