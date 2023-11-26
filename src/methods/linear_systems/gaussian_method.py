import customtkinter
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
                A = coefficient_matrix
                b = constants
                n = len(A)
                for i in range(n):
                    max_row = i
                    for k in range(i + 1, n):
                        if abs(A[k][i]) > abs(A[max_row][i]):
                            max_row = k
                    A[i], A[max_row] = A[max_row], A[i]
                    b[i], b[max_row] = b[max_row], b[i]

                    pivot = A[i][i]
                    for k in range(i, n):
                        A[i][k] /= pivot
                    b[i] /= pivot

                    for k in range(n):
                        if k != i:
                            factor = A[k][i]
                            for j in range(i, n):
                                A[k][j] -= factor * A[i][j]
                            b[k] -= factor * b[i]

                    for i in range(n):
                        for j in range(n):
                            A[i][j] = round(A[i][j], 6)
                        b[i] = round(b[i], 6)

                return b

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
