import customtkinter
import numpy as np
from matplotlib import pyplot as plt


class FixedPointSystemPage(customtkinter.CTkScrollableFrame):
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
            text="Метод простої ітерації (для систем лінійних рівнянь)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=3, padx=(10, 0), pady=10, sticky="w"
        )

        self.matrix_rows = 2
        self.matrix_columns = 2
        self.default_eps = 10
        self.default_max_iter = 100
        self.matrix = []
        self.matrix_frame = None

        customtkinter.CTkLabel(self, text="Кількість рядків матриці:", anchor="w").grid(
            row=1, column=0, padx=(10, 20), pady=10, sticky="we", columnspan=2
        )
        self.rows_entry = customtkinter.CTkEntry(self)
        self.rows_entry.grid(row=1, column=1, padx=20, pady=10, sticky="e")
        self.rows_entry.insert(0, str(self.matrix_rows))

        customtkinter.CTkLabel(
            self, text="Кількість стовпців матриці:", anchor="w"
        ).grid(row=2, column=0, padx=(10, 20), pady=10, sticky="we", columnspan=2)
        self.columns_entry = customtkinter.CTkEntry(self)
        self.columns_entry.grid(row=2, column=1, padx=20, pady=10, sticky="e")
        self.columns_entry.insert(0, str(self.matrix_columns))

        update_size_button = customtkinter.CTkButton(
            self, text="Змінити розмір", command=self.update_size
        )
        update_size_button.grid(row=2, column=2, sticky="e")

        self.create_matrix()

        self.eps_label = customtkinter.CTkLabel(
            self, text="Критерій зупинки (eps):", anchor="w"
        )
        self.eps_label.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.eps_entry = customtkinter.CTkEntry(self)
        self.eps_entry.grid(row=4, column=2, padx=0, pady=10, sticky="ew")
        self.eps_entry.insert(0, self.default_eps)

        self.max_iter_label = customtkinter.CTkLabel(
            self, text="Макс. ітерацій:", anchor="w"
        )
        self.max_iter_label.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="ew")
        self.max_iter_entry = customtkinter.CTkEntry(self)
        self.max_iter_entry.grid(row=5, column=2, padx=0, pady=10, sticky="ew")
        self.max_iter_entry.insert(0, self.default_max_iter)

        self.calculate_button = customtkinter.CTkButton(
            self, text="Розрахувати", command=self.calculate_fixed_point_system
        )
        self.calculate_button.grid(
            row=6, column=0, columnspan=2, padx=(10, 0), pady=(20, 10), sticky="w"
        )

    def update_size(self):
        try:
            new_rows = int(self.rows_entry.get())
            new_columns = int(self.columns_entry.get())
        except ValueError:
            new_rows = 2
            new_columns = 2

        if new_rows < 2:
            new_rows = 2

        if new_rows > 20:
            new_rows = 20

        if new_columns < 2:
            new_columns = 2

        if new_columns > 20:
            new_columns = 20

        self.rows_entry.delete(0, "end")
        self.rows_entry.insert(0, str(new_rows))
        self.columns_entry.delete(0, "end")
        self.columns_entry.insert(0, str(new_columns))

        self.matrix_rows = new_rows
        self.matrix_columns = new_columns

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
            self.grid_slaves(3, 0)[0].destroy()

        self.matrix = []
        self.matrix_frame = customtkinter.CTkScrollableFrame(
            self,
            orientation="horizontal",
            height=50 * self.matrix_rows,
        )
        self.matrix_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=(10, 0),
            pady=10,
            sticky="we",
        )

        for i in range(self.matrix_rows):
            row = []
            for j in range(self.matrix_columns + 1):
                placeholder_text = (
                    f"c{j + 1}" if j != self.matrix_columns else f"b{i + 1}"
                )

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
                        10 if j == self.matrix_columns else 0,
                    ),
                    pady=10,
                    sticky="w",
                )

                if j != self.matrix_columns:
                    text = customtkinter.CTkLabel(
                        frame,
                        text=f" * x{j + 1} {'=' if j == self.matrix_columns - 1 else '+'} ",
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

    def calculate_fixed_point_system(self):
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

            eps_str = self.eps_entry.get()
            max_iter_str = self.max_iter_entry.get()

            if not (eps_str and max_iter_str):
                raise ValueError("Всі поля мають бути заповнені.")

            try:
                float(eps_str)
                int(max_iter_str)
            except ValueError:
                raise ValueError(
                    "Критерій зупинки та макс. ітерацій мають бути числами."
                )

            for row in self.matrix:
                coefficients_row = []
                for entry in row:
                    value = entry.get()
                    if value == "":
                        raise ValueError("Всі поля мають бути заповнені.")
                    coefficients_row.append(float(value))
                coefficients_matrix.append(coefficients_row[:-1])
                constants_vector.append(coefficients_row[-1])

            def implementation(coefficient_matrix, constants, eps, max_iter):
                A = np.array(coefficient_matrix, dtype=float)
                b = np.array(constants, dtype=float)

                x = np.zeros_like(b)

                for iteration in range(max_iter):
                    x_new = np.linalg.inv(A) @ (b - (A @ x))

                    if np.linalg.norm(x_new - x) < eps:
                        return x_new

                    x = x_new

                raise Exception(
                    f"Метод простої ітерації не збігся після {max_iter} ітерацій."
                )

            eps = float(eps_str)
            max_iter = int(max_iter_str)
            roots = implementation(coefficients_matrix, constants_vector, eps, max_iter)

            self.result_subtitle_label = customtkinter.CTkLabel(
                self,
                text="Результат:",
                font=customtkinter.CTkFont(size=16, weight="bold"),
            )
            self.result_subtitle_label.grid(
                row=7, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky="w"
            )

            result = ""
            for i, root in enumerate(roots):
                result += f"x{i + 1} = {root:.6f}\n"
            self.result_label = customtkinter.CTkLabel(
                self, text=result, justify="left"
            )
            self.result_label.grid(
                row=8, column=0, columnspan=2, padx=(10, 0), pady=0, sticky="w"
            )

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
