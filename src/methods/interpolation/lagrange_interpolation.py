import customtkinter
import numpy as np
from matplotlib import pyplot as plt


class LagrangeInterpolationPage(customtkinter.CTkScrollableFrame):
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
            text="Метод Лагранжа (для інтерполяції)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="w"
        )

        self.matrix_size = 4
        self.default_number_of_points = 100
        self.matrix = []
        self.matrix_frame = None

        customtkinter.CTkLabel(self, text="Розмір матриці:", anchor="w").grid(
            row=1, column=0, padx=(10, 20), pady=10, sticky="we", columnspan=2
        )
        self.size_entry = customtkinter.CTkEntry(self)
        self.size_entry.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        self.size_entry.insert(0, str(self.matrix_size))

        update_size_button = customtkinter.CTkButton(
            self, text="Змінити розмір", command=self.update_size
        )
        update_size_button.grid(row=1, column=2, sticky="e")

        self.create_matrix()

        self.number_of_points_label = customtkinter.CTkLabel(
            self, text="Кількість точок:", anchor="w"
        )
        self.number_of_points_label.grid(
            row=3, column=0, padx=(10, 0), pady=10, sticky="ew"
        )
        self.number_of_points_entry = customtkinter.CTkEntry(self)
        self.number_of_points_entry.grid(row=3, column=2, padx=0, pady=10, sticky="ew")
        self.number_of_points_entry.insert(0, self.default_number_of_points)

        self.calculate_button = customtkinter.CTkButton(
            self, text="Розрахувати", command=self.calculate_lagrange_interpolation
        )
        self.calculate_button.grid(
            row=4, column=0, columnspan=2, padx=(10, 0), pady=(20, 10), sticky="w"
        )

    def update_size(self):
        try:
            new_size = int(self.size_entry.get())
        except ValueError:
            new_size = 2

        if new_size < 2:
            new_size = 2

        if new_size > 20:
            new_size = 20

        self.size_entry.delete(0, "end")
        self.size_entry.insert(0, str(new_size))
        self.matrix_size = new_size
        self.create_matrix()

    def create_matrix(self):
        if hasattr(self, "result_subtitle_label"):
            self.result_subtitle_label.destroy()

        if hasattr(self, "result_label"):
            self.result_label.destroy()

        if hasattr(self, "error_subtitle_label"):
            self.error_subtitle_label.destroy()

        if hasattr(self, "error_label"):
            self.error_label.destroy()

        if self.matrix_frame:
            self.matrix_frame.destroy()
            self.grid_slaves(2, 0)[0].destroy()

        self.matrix = []

        self.matrix_frame = customtkinter.CTkScrollableFrame(
            self,
            height=50 * self.matrix_size,
            orientation="horizontal",
        )

        self.matrix_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=(10, 0),
            pady=10,
            sticky="we",
        )

        for i in range(self.matrix_size):
            row = []
            for j in range(2):
                placeholder_text = f"x{i + 1}" if j == 0 else f"y{i + 1}"

                frame = customtkinter.CTkFrame(
                    self.matrix_frame,
                    width=50,
                    height=30,
                    corner_radius=0,
                    bg_color="transparent",
                )
                frame.grid(
                    row=i,
                    column=j,
                    padx=(0 if j != 0 else 10, 0),
                    pady=0,
                    sticky="w",
                )

                entry = customtkinter.CTkEntry(
                    frame,
                    height=30,
                    width=50,
                    placeholder_text=placeholder_text,
                )
                entry.grid(
                    row=0,
                    column=0,
                    padx=(
                        0,
                        20 if j == 0 else 0,
                    ),
                    pady=10,
                    sticky="w",
                )

                row.append(entry)
            self.matrix.append(row)

    def calculate_lagrange_interpolation(self):
        plt.close("all")

        if hasattr(self, "error_subtitle_label"):
            self.error_subtitle_label.destroy()

        if hasattr(self, "error_label"):
            self.error_label.destroy()

        try:
            x_values = []
            y_values = []

            for row in self.matrix:
                x_value = row[0].get()
                y_value = row[1].get()

                if x_value == "" or y_value == "":
                    raise ValueError("Всі поля мають бути заповнені.")

                x_values.append(float(x_value))
                y_values.append(float(y_value))

            def implementation(x_values, y_values):
                x_values = np.array(x_values, dtype=float)
                y_values = np.array(y_values, dtype=float)

                number_of_points = self.number_of_points_entry.get()

                try:
                    number_of_points = int(number_of_points)
                except ValueError:
                    self.number_of_points_entry.delete(0, "end")
                    self.number_of_points_entry.insert(0, self.default_number_of_points)
                    number_of_points = self.default_number_of_points

                if number_of_points < 2:
                    self.number_of_points_entry.delete(0, "end")
                    self.number_of_points_entry.insert(0, self.default_number_of_points)
                    number_of_points = self.default_number_of_points

                if len(x_values) != len(set(x_values)):
                    raise RuntimeWarning("Значення x повинні бути унікальними.")

                def lagrange_polynomial(x_values, y_values):
                    n = len(x_values)

                    def interpolate(x):
                        result = 0
                        for i in range(n):
                            partial_product = y_values[i]
                            for j in range(n):
                                if j != i:
                                    partial_product *= (x - x_values[j]) / (
                                            x_values[i] - x_values[j]
                                    )
                            result += partial_product
                        return result

                    return interpolate

                polynomial = lagrange_polynomial(x_values, y_values)
                x_interpolation = np.linspace(
                    x_values.min(), x_values.max(), number_of_points
                )
                y_interpolation = polynomial(x_interpolation)

                return x_interpolation, y_interpolation

            x_interpolation, y_interpolation = implementation(x_values, y_values)
            self.plot_interpolation(
                x_values, y_values, x_interpolation, y_interpolation
            )

        except Exception as e:
            self.error_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Помилка:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.error_subtitle_label.grid(
                row=5, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.error_label = customtkinter.CTkLabel(self, text=f"{str(e)}")
            self.error_label.grid(
                row=6, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )

    def plot_interpolation(self, x_values, y_values, x_interpolation, y_interpolation):
        try:
            plt.figure(
                num="Графік інтерполяції Лагранжа",
            )

            plt.plot(x_interpolation, y_interpolation)
            plt.plot(x_values, y_values, "bo")

            plt.axvline(0, color="black", linewidth=0.5)
            plt.axhline(0, color="black", linewidth=0.5)

            plt.grid(True, linestyle="--", alpha=0.7)
            plt.xlabel("x")
            plt.ylabel("y")

            plt.tight_layout()
            plt.show(block=False)

        except Exception as e:
            print(e)
