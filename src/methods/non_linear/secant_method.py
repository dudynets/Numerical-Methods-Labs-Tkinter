import customtkinter
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class SecantMethodPage(customtkinter.CTkScrollableFrame):
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
            text="Метод хорд (для нелінійних рівнянь)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="w"
        )

        default_fx = "x**2 - 4"
        default_x0 = 0
        default_x1 = 4
        default_eps = 1e-6
        default_max_iter = 100

        self.fx_label = customtkinter.CTkLabel(self, text="f(x):", anchor="w")
        self.fx_label.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.fx_entry = customtkinter.CTkEntry(self)
        self.fx_entry.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.fx_entry.insert(0, default_fx)

        self.x0_label = customtkinter.CTkLabel(self, text="a:", anchor="w")
        self.x0_label.grid(row=2, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.x0_entry = customtkinter.CTkEntry(self)
        self.x0_entry.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.x0_entry.insert(0, default_x0)

        self.x1_label = customtkinter.CTkLabel(self, text="b:", anchor="w")
        self.x1_label.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.x1_entry = customtkinter.CTkEntry(self)
        self.x1_entry.grid(row=3, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.x1_entry.insert(0, default_x1)

        self.eps_label = customtkinter.CTkLabel(
            self, text="Критерій зупинки (eps):", anchor="w"
        )
        self.eps_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.eps_entry = customtkinter.CTkEntry(self)
        self.eps_entry.grid(row=4, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.eps_entry.insert(0, default_eps)

        self.max_iter_label = customtkinter.CTkLabel(
            self, text="Макс. ітерацій:", anchor="w"
        )
        self.max_iter_label.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.max_iter_entry = customtkinter.CTkEntry(self)
        self.max_iter_entry.grid(row=5, column=1, padx=(10, 0), pady=10, sticky="ew")
        self.max_iter_entry.insert(0, default_max_iter)

        self.calculate_button = customtkinter.CTkButton(
            self, text="Розрахувати", command=self.calculate_secant_method
        )
        self.calculate_button.grid(
            row=6, column=0, columnspan=2, padx=(10, 0), pady=(20, 10), sticky="w"
        )

    def calculate_secant_method(self):
        plt.close("all")

        f_string = self.fx_entry.get()
        x0_str = self.x0_entry.get()
        x1_str = self.x1_entry.get()
        eps_str = self.eps_entry.get()
        max_iter_str = self.max_iter_entry.get()

        if hasattr(self, "result_subtitle_label"):
            self.result_subtitle_label.destroy()

        if hasattr(self, "result_label"):
            self.result_label.destroy()

        if hasattr(self, "error_subtitle_label"):
            self.error_subtitle_label.destroy()

        if hasattr(self, "error_label"):
            self.error_label.destroy()

        try:
            if not (f_string and x0_str and x1_str and eps_str and max_iter_str):
                raise ValueError("Всі поля мають бути заповнені.")

            try:
                float(x0_str)
                float(x1_str)
                float(eps_str)
                int(max_iter_str)
            except ValueError:
                raise ValueError(
                    "a, b,  критерій зупинки та макс. ітерацій мають бути числами."
                )

            x = sp.symbols("x")
            f = sp.sympify(f_string)

            f_np = sp.lambdify(x, f, "numpy")

            x0 = float(x0_str)
            x1 = float(x1_str)
            eps = float(eps_str)
            max_iter = int(max_iter_str)

            def implementation(f, x0, x1, eps, max_iter):
                for i in range(max_iter):
                    f_x0 = f(x0)
                    f_x1 = f(x1)

                    if abs(f_x1) < eps:
                        return x1, i

                    if f_x1 - f_x0 == 0:
                        raise ValueError(
                            f"Ділення на нуль виникло під час виконання методу січних. Ітерація: {i}"
                        )

                    x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

                    if abs(x_next - x1) < eps:
                        return x_next, i

                    x0, x1 = x1, x_next

                raise ValueError(
                    f"Максимальна кількість ітерацій ({max_iter}) була досягнута без збіжності. Останнє значення: {x1}"
                )

            result, iterations = implementation(f_np, x0, x1, eps, max_iter)

            self.result_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Результат:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.result_subtitle_label.grid(
                row=7, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.result_label = customtkinter.CTkLabel(self, text=f"x = {result:.6f}")
            self.result_label.grid(
                row=8, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )

            self.plot_function(result, f_np, x0, x1)
        except Exception as e:
            self.error_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Помилка:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.error_subtitle_label.grid(
                row=7, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.error_label = customtkinter.CTkLabel(self, text=f"{str(e)}")
            self.error_label.grid(
                row=8, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )

    def plot_function(self, root, f_np, x0, x1):
        try:
            root_to_x0_distance = abs(root - x0)
            x_values = np.linspace(
                root - (root_to_x0_distance * 2),
                root + (root_to_x0_distance * 2),
                10000,
            )
            if root_to_x0_distance == 0:
                x_values = np.linspace(
                    root - 10,
                    root + 10,
                    10000,
                )

            for i in range(len(x_values) - 1):
                if (
                        x_values[i] < 0 < x_values[i + 1]
                        or x_values[i] > 0 > x_values[i + 1]
                ):
                    x_values = np.insert(x_values, i + 1, 0)
                    break

            y_values = f_np(x_values)

            plt.figure(
                num="Графік функції",
            )
            plt.margins(0)

            plt.plot(x_values, y_values, label="f(x)")
            plt.axvline(0, color="black", linewidth=0.5)
            plt.axhline(0, color="black", linewidth=0.5)

            plt.scatter(
                root,
                0,
                color="red",
                marker="o",
                label=f"Корінь ({str(round(root, 2)).rstrip('0').rstrip('.')})",
                zorder=3,
            )

            plt.axvline(
                x0,
                color="blue",
                linestyle=":",
                linewidth=1,
                label=f"a ({str(round(x0, 2)).rstrip('0').rstrip('.')})",
            )
            plt.axvline(
                x1,
                color="blue",
                linestyle=":",
                linewidth=1,
                label=f"b ({str(round(x1, 2)).rstrip('0').rstrip('.')})",
            )

            plt.grid(True, linestyle="--", alpha=0.7)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.legend()

            plt.tight_layout()
            plt.show(block=False)

        except Exception as e:
            print(e)
