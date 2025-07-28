import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import libmath

class PolyRegressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polynomial Regression Route Planner")

        self.img = None
        self.points = []
        self.degree = 2
        self.coefficients = None

        # Main container frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left: matplotlib canvas
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: controls frame with bigger buttons
        ctrl_frame = tk.Frame(main_frame, padx=20, pady=20)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y)

        font_btn = ("Arial", 16, "bold")

        tk.Button(ctrl_frame, text="Load Image", font=font_btn, command=self.load_image, width=15, height=2).pack(pady=10)
        tk.Label(ctrl_frame, text="Polynomial Degree:", font=("Arial", 14)).pack(pady=(20,5))
        self.degree_var = tk.IntVar(value=self.degree)
        self.degree_spin = tk.Spinbox(ctrl_frame, from_=1, to=10, width=5, font=("Arial", 14), textvariable=self.degree_var)
        self.degree_spin.pack(pady=5)

        tk.Button(ctrl_frame, text="Run Regression", font=font_btn, command=self.run_regression, width=15, height=2).pack(pady=10)
        tk.Button(ctrl_frame, text="Reset Points", font=font_btn, command=self.reset_points, width=15, height=2).pack(pady=10)
        tk.Button(ctrl_frame, text="Save Formula", font=font_btn, command=self.save_formula, width=15, height=2).pack(pady=10)

        # Label to show error
        self.error_label = tk.Label(ctrl_frame, text="", font=("Arial", 14), fg="red")
        self.error_label.pack(pady=(30,0))

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.redraw()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            self.img = plt.imread(file_path)
            self.reset_points()

    def reset_points(self):
        self.points.clear()
        self.coefficients = None
        self.error_label.config(text="")
        self.redraw()

    def redraw(self):
        self.ax.clear()
        if self.img is not None:
            self.ax.imshow(self.img)
        else:
            self.ax.imshow(np.ones((500, 500, 3)))
        if self.points:
            xs, ys = zip(*self.points)
            self.ax.scatter(xs, ys, c='red')
            if self.coefficients is not None:
                x_fit = np.linspace(min(xs), max(xs), 500)
                y_fit = [libmath.polynomial_value(self.coefficients, xi) for xi in x_fit]
                self.ax.plot(x_fit, y_fit, 'b-', linewidth=2, label=f'{self.degree_var.get()} Degree Polynomial Regression')
                self.ax.legend()
            else:
                self.ax.plot(xs, ys, 'b-')
        self.ax.set_title("Click to add points")
        self.canvas.draw()

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.points.append((event.xdata, event.ydata))
            self.coefficients = None
            self.error_label.config(text="")
            self.redraw()

    def run_regression(self):
        degree = self.degree_var.get()
        if len(self.points) < degree + 1:
            messagebox.showwarning("Warning", f"Need at least {degree + 1} points for degree {degree} regression")
            return
        xs, ys = zip(*self.points)
        try:
            self.coefficients = libmath.polynomial_regression(xs, ys, degree)
        except Exception as e:
            messagebox.showerror("Error", f"Regression failed:\n{e}")
            self.coefficients = None
            self.error_label.config(text="")
            return

        # Calculate mean squared error (MSE)
        y_preds = [libmath.polynomial_value(self.coefficients, xi) for xi in xs]
        mse = sum((yi - ypi)**2 for yi, ypi in zip(ys, y_preds)) / len(ys)
        self.error_label.config(text=f"Mean Squared Error: {mse:.6f}")

        self.redraw()

    def save_formula(self):
        if not self.coefficients:
            messagebox.showwarning("Warning", "No regression formula to save. Run regression first.")
            return
        formula = libmath.polynomial_formula_string(self.coefficients)
        save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if save_path:
            with open(save_path, 'w') as f:
                f.write("Polynomial regression formula:\n")
                f.write(f"y = {formula}\n")
            messagebox.showinfo("Saved", f"Formula saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PolyRegressionApp(root)
    root.mainloop()
