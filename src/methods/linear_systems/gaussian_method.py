import customtkinter
import numpy as np
from matplotlib import pyplot as plt


class GaussianMethodPage(customtkinter.CTkScrollableFrame):
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
            text="Метод Гауса (для систем лінійних рівнянь)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=2, padx=(10, 0), pady=10, sticky="w"
        )

        self.matrix_size = 2
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

        self.calculate_button = customtkinter.CTkButton(
            self, text="Розрахувати", command=self.calculate_gaussian_method
        )
        self.calculate_button.grid(
            row=3, column=0, columnspan=2, padx=(10, 0), pady=(20, 10), sticky="w"
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
            orientation="horizontal",
            height=50 * self.matrix_size,
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
            for j in range(self.matrix_size + 1):
                placeholder_text = f"c{j + 1}" if j != self.matrix_size else f"b{i + 1}"

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
                        10 if j == self.matrix_size else 0,
                    ),
                    pady=10,
                    sticky="w",
                )

                if j != self.matrix_size:
                    text = customtkinter.CTkLabel(
                        frame,
                        text=f" * x{j + 1} {'=' if j == self.matrix_size - 1 else '+'} ",
                    )
                    text.grid(
                        row=0,
                        column=1,
                        padx=0,
                        pady=10,
                        sticky="w",
                    )

                row.append(entry)
            self.matrix.append(row)

    def calculate_gaussian_method(self):
        plt.close("all")

        if hasattr(self, "result_subtitle_label"):
            self.result_subtitle_label.destroy()

        if hasattr(self, "result_label"):
            self.result_label.destroy()

        if hasattr(self, "error_subtitle_label"):
            self.error_subtitle_label.destroy()

        if hasattr(self, "error_label"):
            self.error_label.destroy()

        try:
            coefficients_matrix = []
            constants_vector = []

            for row in self.matrix:
                coefficients_row = []
                for entry in row:
                    value = entry.get()
                    if value == "":
                        raise ValueError("Всі поля мають бути заповнені.")
                    coefficients_row.append(float(value))
                coefficients_matrix.append(coefficients_row[:-1])
                constants_vector.append(coefficients_row[-1])

            def implementation(coefficient_matrix, constants):
                coefficient_matrix = np.array(coefficient_matrix, dtype=float)
                constants = np.array(constants, dtype=float)
                n = len(coefficient_matrix)
                x = np.zeros(n)

                for j in range(n):
                    if coefficient_matrix[j][j] == 0:
                        raise ValueError(
                            f"Ділення на нуль виникло під час виконання методу Гауса."
                        )

                    for k in range(j + 1, n):
                        factor = coefficient_matrix[k][j] / coefficient_matrix[j][j]
                        coefficient_matrix[k] -= factor * coefficient_matrix[j]
                        constants[k] -= factor * constants[j]

                for j in range(n - 1, -1, -1):
                    x[j] = (
                                   constants[j]
                                   - np.dot(coefficient_matrix[j][j + 1: n], x[j + 1: n])
                           ) / coefficient_matrix[j][j]

                return x

            roots = implementation(coefficients_matrix, constants_vector)

            self.result_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Результат:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.result_subtitle_label.grid(
                row=4, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            result = ""
            for i, root in enumerate(roots):
                result += f"x{i + 1} = {root:.6f}\n"
            self.result_label = customtkinter.CTkLabel(
                self, text=result, justify="left"
            )
            self.result_label.grid(
                row=5, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )

        except Exception as e:
            self.error_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Помилка:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.error_subtitle_label.grid(
                row=4, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            self.error_label = customtkinter.CTkLabel(self, text=f"{str(e)}")
            self.error_label.grid(
                row=5, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )
