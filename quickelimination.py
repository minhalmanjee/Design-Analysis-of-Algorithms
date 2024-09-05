import tkinter as tk
from tkinter import Canvas
import numpy as np

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def quick_elimination(points, canvas):
    # Choose the first quadrilateral as the initial bounding box
    rect = [min(points, key=lambda p: p[0]), max(points, key=lambda p: p[0]),
            max(points, key=lambda p: p[1]), min(points, key=lambda p: p[1])]

    #canvas.create_text(10, 10, anchor=tk.NW, text='Quick Elimination Convex Hull Visualization', fill='black')

    # Draw the initial bounding box
    rect.append(rect[0])  # Close the loop
    rect_x, rect_y = zip(*rect)
    canvas.create_line(rect_x, rect_y, fill='red', dash=(4, 2))

    # Eliminate points inside the bounding box
    points = [p for p in points if not (ccw(rect[0], rect[1], p) and ccw(rect[1], rect[2], p)
                                       and ccw(rect[2], rect[3], p) and ccw(rect[3], rect[0], p))]

    # Draw the remaining points after elimination
    for p in points:
        canvas.create_oval(p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2, fill='green')

    # Find the convex hull of the remaining points
    hull = []
    for p in sorted(points, key=lambda x: (np.arctan2(x[1] - rect[0][1], x[0] - rect[0][0]), x)):
        while len(hull) >= 2 and not ccw(hull[-2], hull[-1], p):
            hull.pop()
        hull.append(p)

    hull.append(hull[0])  # Close the loop

    # Draw the convex hull
    hull_x, hull_y = zip(*hull)
    canvas.create_line(hull_x, hull_y, fill='purple')

def visualize():
    points = [(int(entry_x.get()), int(entry_y.get())) for entry_x, entry_y in zip(entry_x_list, entry_y_list)]
    quick_elimination(points, canvas)

# Create the main window
root = tk.Tk()
root.title('Quick Elimination Convex Hull Visualization')

# Create canvas
canvas = Canvas(root, width=400, height=400, bg='white')
canvas.pack()

# Entry widgets for points
entry_x_list = [tk.Entry(root) for _ in range(4)]
entry_y_list = [tk.Entry(root) for _ in range(4)]

# Place entry widgets using pack
for i, (entry_x, entry_y) in enumerate(zip(entry_x_list, entry_y_list)):
    entry_x.pack(side=tk.LEFT)
    entry_y.pack(side=tk.LEFT)

# Button to trigger visualization
btn_visualize = tk.Button(root, text='Visualize', command=visualize)
btn_visualize.pack()

# Run the Tkinter event loop
root.mainloop()
