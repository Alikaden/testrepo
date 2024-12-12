import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
#add background
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys  # For exiting the application
from tkinter import *
from PIL import Image, ImageTk  # Use Pillow for handling images


import os
import sys

from numpy.ma.core import left_shift

if getattr(sys, "frozen", False):  # If running from an .exe
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
background_image_path = os.path.join(base_path, "ronaldopic.jpg")




# Constants
M = 1000000000  # big M
entries = []  # To hold the matrix entry widgets
m = []  # Placeholder for the matrix
n = 0  # Matrix size

# Example matrices
matrix1 = [
    [M, 5, 14, 6, M, M, M],
    [M, M, 6, M, 12, M, M],
    [M, M, M, 7, 2, 12, M],
    [M, M, 3, M, M, 9, M],
    [M, M, M, M, M, M, 4],
    [M, M, M, M, M, M, 4],
    [M, M, M, M, M, M, M],
]

matrix2 = [
    [M, 7, 8, 5, M, M, M],
    [M, M, M, M, 12, M, M],
    [M, M, M, M, 8, 9, M],
    [M, M, M, M, 7, 13, M],
    [M, M, M, M, M, M, 9],
    [M, M, M, M, M, M, 6],
    [M, M, M, M, M, M, M],
]

matrix3 = [
    [M, 5, 3, M, M, M, M],
    [5, M, 1, 5, 2, M, M],
    [3, 1, M, 7, M, M, 12],
    [M, 5, 7, M, 3, 1, 3],
    [M, 2, M, 3, M, 1, M],
    [M, M, M, 1, 1, M, 4],
    [M, M, 12, 3, M, 4, M],
]
matrix4 = [
    [M, 4000, 5400, 9800, M],
    [M, M, 4300, 6200, 8700],
    [M, M, M, 4800, 7100],
    [M, M, M, M, 4900],
    [M, M, M, M, M]
]

# hàm, tạo graph
def create_directed_graph(matrix):
    G = nx.DiGraph()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != M:
                G.add_edge(i + 1, j + 1, weight=matrix[i][j])
    return G


# hàm vẽ graph
def draw_graph():
    G = create_directed_graph(m)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=900, node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


# hàm chạy quy hoạch động
def run_algorithm():
    global m
    n = len(m)
    f = [M] * n
    path = [-1] * n
    f[-1] = 0  # Base case

    for i in range(n - 2, -1, -1):
        for j in range(n):
            if m[i][j] != M:
                cost = m[i][j] + f[j]
                if cost < f[i]:
                    f[i] = cost
                    path[i] = j

    # Build the path
    current = 0
    path_traversed = [current + 1]
    while path[current] != -1:
        current = path[current]
        path_traversed.append(current + 1)

    messagebox.showinfo("Result", f"Minimum cost: {f[0]}\nPath: {' -> '.join(map(str, path_traversed))}")


# Function to create a matrix entry form dynamically
def create_matrix_form():
    global n, entries
    try:
        n = int(matrix_size_entry.get())
        if n <= 0:
            raise ValueError("Matrix size must be a positive integer.")
    except ValueError:
        messagebox.showerror("Error", "Matrix size must be a positive integer.")
        return

    cell_width = 104  # Width of each cell in pixels
    cell_height = 40  # Height of each cell in pixels
    button_height = 50  # Space for buttons
    margin = 20  # Additional margin

    window_width = n * cell_width + margin
    window_height = n * cell_height + button_height + margin

    # Get screen dimensions to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position to center the window
    position_top = (screen_height // 2) - (window_height // 2)
    position_left = (screen_width // 2) - (window_width // 2)

    # Create a new window for matrix entry
    matrix_window = tk.Toplevel(root)
    matrix_window.title(f"Enter Matrix ({n}x{n})")
    matrix_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")


    # Create grid entries
    entries.clear()
    for i in range(n):
        row_entries = []
        for j in range(n):
            entry = tk.Entry(matrix_window, width=10,font=("Arial",12))
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # Buttons for Show Graph and Run Algorithm
    tk.Button(matrix_window, text="Show Graph", command=lambda: [get_matrix_from_form(), draw_graph()], font=("Arial",12)).grid(
        row=n, column=0, columnspan=n // 2, pady=10
    )
    tk.Button(matrix_window, text="Run Algorithm", command=lambda: [get_matrix_from_form(), run_algorithm()], font=("Arial",12)).grid(
        row=n, column=n // 2, columnspan=n // 2, pady=10
    )


# Function to retrieve the matrix from the form
def get_matrix_from_form():
    global m
    m.clear()
    for i in range(n):
        row = []
        for j in range(n):
            try:
                value = int(entries[i][j].get())
                row.append(value if value != M else M)
            except ValueError:
                row.append(M)  # Default to M (Infinity) if no input
        m.append(row)


# Functions to use predefined matrices
def use_matrix1():
    global m
    m = matrix1
    run_algorithm()
def show_matrix1():
    global m
    m = matrix1
    draw_graph()

def use_matrix2():
    global m
    m = matrix2
    run_algorithm()
def show_matrix2():
    global m
    m = matrix2
    draw_graph()

def show_matrix3():
    global m
    m = matrix3
    draw_graph()
def use_matrix3():
    global m
    m = matrix3
    run_algorithm()

def show_matrix4():
    global m
    m = matrix4
    draw_graph()
def use_matrix4():
    global m
    m = matrix4
    run_algorithm()


# Initialize main window
root = tk.Tk()
root.title("Graph Visualization and Algorithm")
root.geometry("800x400")


# #add image
#
# # Load the uploaded background image
# background_image_path = "ronaldopic.jpg"  # Replace with your uploaded image path/-strong/-heart:>:o:-((:-h # background_image = Image.open(background_image_path)
# background_image = background_image.resize((736, 1313), Image.Resampling.LANCZOS)  # Resize the image to match the window size
# background_photo = ImageTk.PhotoImage(background_image)
#
# # Create a Label widget to display the background image
# background_label = Label(root, image=background_photo)
# background_label.place(relwidth=1, relheight=1)  # Cover the entire window


# Add matrix size entry
size_frame = tk.Frame(root)
size_frame.pack(pady=20)

tk.Label(size_frame, text="Enter matrix size:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
matrix_size_entry = tk.Entry(size_frame, width=5, font=("Arial", 14))
matrix_size_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(size_frame, text="Enter", command=create_matrix_form, font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5)

# tao cac nut de lam example
example_frame = tk.Frame(root)
example_frame.pack(pady=20)

tk.Button(example_frame, text="Calculate Matrix Example 1", command=use_matrix1, font=("Arial", 12), width=22).grid(row=1, column=2, padx=5, pady=5)
tk.Button(example_frame, text="Show Matrix Example 1", command=show_matrix1, font=("Arial", 12), width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(example_frame, text="Calculate Matrix Example 2", command=use_matrix2, font=("Arial", 12), width=22).grid(row=2, column=2, padx=5, pady=5)
tk.Button(example_frame, text="Show Matrix Example 2", command=show_matrix2, font=("Arial", 12), width=20).grid(row=2, column=0, padx=5, pady=5)
tk.Button(example_frame, text="Show Matrix Example 3", command=show_matrix3, font=("Arial", 12), width=20).grid(row=3, column=0, padx=5, pady=5)
tk.Button(example_frame, text="Calculate Matrix Example 3", command=use_matrix3, font=("Arial", 12), width=22).grid(row=3, column=2, padx=5, pady=5)
tk.Button(example_frame, text="Show Matrix Example 4", command=show_matrix4, font=("Arial", 12), width=20).grid(row=4, column=0, padx=5, pady=5)
tk.Button(example_frame, text="Calculate Matrix Example 4", command=use_matrix4, font=("Arial", 12), width=22).grid(row=4, column=2, padx=5, pady=5)

instruction_label = tk.Label(
    root,
    text="Created by JSH2019",
    font=("Arial", 6,"italic bold"),
    justify="left",
    wraplength=700  # Wrap text within 700 pixels
)
instruction_label.pack(pady=40)

# Main loop
root.mainloop()