import tkinter as tk
from tkinter import Canvas, Button, Text
import random

def brute_force_convex_hull(points):
    if len(points) < 3:
        return points, []

    def on_the_left(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

    hull = []
    non_hull = []
    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                left_side = True
                for k in range(len(points)):
                    if k != i and k != j:
                        if not on_the_left(points[i], points[j], points[k]):
                            left_side = False
                            break
                if left_side:
                    hull.append((points[i], points[j]))
                else:
                    non_hull.append((points[i], points[j]))

    return hull, non_hull

def on_canvas_click(event):
    x, y = event.x, event.y
    points.append((x, y))
    draw_point(x, y)

def draw_point(x, y):
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='black')

def draw_hull_lines(lines, color):
    for line in lines:
        canvas.create_line(line[0], line[1], tags='line', fill=color)
        canvas.update()
        canvas.after(250)

def draw_hull(hull, non_hull):
    canvas.delete('line')
    draw_hull_lines(non_hull, 'black')
    draw_hull_lines(hull, 'red')

def draw_grid():
    for x in range(0, 601, 50):
        canvas.create_line(x, 0, x, 400, fill='gray', dash=(2, 2))
        canvas.create_text(x, 400, anchor='sw', text=str(x), fill='black')

    for y in range(0, 401, 50):
        canvas.create_line(0, y, 600, y, fill='gray', dash=(2, 2))
        canvas.create_text(0, y, anchor='e', text=str(400 - y), fill='black')

def calculate_hull():
    hull, non_hull = brute_force_convex_hull(points)
    draw_hull(hull, non_hull)
    
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Time Complexity: O(n^3)\n")  # Simplified notation
    result_text.insert(tk.END, "Space Complexity: O(1)\n")  # Constant space complexity

root = tk.Tk()
root.title("Convex Hull - Brute Force")
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()
canvas.bind('<Button-1>', on_canvas_click)

calculate_button = tk.Button(root, text="Calculate Convex Hull", command=calculate_hull)
calculate_button.pack()

points = []

draw_grid()

result_text = Text(root, height=5, width=40)
result_text.pack()

root.mainloop()
