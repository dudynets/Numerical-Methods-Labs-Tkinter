import customtkinter
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class SimpsonsMethodPage(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#000811",
            scrollbar_button_color="#000811",
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self,
            text="Метод Сімпсона (для інтегрування)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="w"
        )

        default_fx = "x**2 - 4"
        default_a = 0
        default_b = 10
        default_n = 100

        self.fx_label = customtkinter.CTkLabel(self, text="f(x):", anchor="w")
        self.fx_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.fx_entry = customtkinter.CTkEntry(self)
        self.fx_entry.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.fx_entry.insert(0, default_fx)

        self.a_label = customtkinter.CTkLabel(
            self, text="Нижня межа інтегрування (a):", anchor="w"
        )
        self.a_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.a_entry = customtkinter.CTkEntry(self)
        self.a_entry.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.a_entry.insert(0, default_a)

        self.b_label = customtkinter.CTkLabel(
            self, text="Верхня межа інтегрування (b):", anchor="w"
        )
        self.b_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.b_entry = customtkinter.CTkEntry(self)
        self.b_entry.grid(row=3, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.b_entry.insert(0, default_b)

        self.n_label = customtkinter.CTkLabel(
            self, text="Кількість розбиттів інтервалу (n):", anchor="w"
        )
        self.n_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.n_entry = customtkinter.CTkEntry(self)
        self.n_entry.grid(row=4, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.n_entry.insert(0, default_n)

        self.calculate_button = customtkinter.CTkButton(
            self, text="Розрахувати", command=self.calculate_simpsons_method
        )
        self.calculate_button.grid(
            row=5, column=0, columnspan=2, padx=(10, 0), pady=(20, 10), sticky="w"
        )

    def calculate_simpsons_method(self):
        plt.close("all")

        f_string = self.fx_entry.get()
        a_str = self.a_entry.get()
        b_str = self.b_entry.get()
        n_str = self.n_entry.get()

        if hasattr(self, "result_subtitle_label"):
            self.result_subtitle_label.destroy()

        if hasattr(self, "result_label"):
            self.result_label.destroy()

        if hasattr(self, "error_subtitle_label"):
            self.error_subtitle_label.destroy()

        if hasattr(self, "error_label"):
            self.error_label.destroy()

        try:
            if not (f_string and a_str and b_str and n_str):
                raise ValueError("Всі поля мають бути заповнені.")

            try:
                float(a_str)
                float(b_str)
                int(n_str)
            except ValueError:
                raise ValueError(
                    "Нижня межа інтегрування, верхня межа інтегрування та кількість розбиттів інтервалу мають бути числами."
                )

            x = sp.symbols("x")
            f = sp.sympify(f_string)

            f_np = sp.lambdify(x, f, "numpy")

            a = float(a_str)
            b = float(b_str)
            n = int(n_str)

            if b < a:
                raise ValueError("Верхня межа інтегрування має бути більшою за нижню.")

            h = (b - a) / n
            x = np.linspace(a, b, n + 1)
            y = f_np(x)
            result = h / 3 * (y[0] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-1:2]) + y[-1])

            self.result_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Результат:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.result_subtitle_label.grid(
                row=6, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.result_label = customtkinter.CTkLabel(self, text=f"x = {result:.6f}")
            self.result_label.grid(
                row=7, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )
        except Exception as e:
            self.error_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Помилка:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.error_subtitle_label.grid(
                row=6, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.error_label = customtkinter.CTkLabel(self, text=f"{str(e)}")
            self.error_label.grid(
                row=7, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )
