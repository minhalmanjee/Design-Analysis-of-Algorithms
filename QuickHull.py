import tkinter as tk
import math
import random
import timeit

dt = 200

def findDistance(a: list, b: list, p: list):
    #rewriting coordinates for simply geometric syntax
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    px, py = p[0], p[1]
    d = 0
    d = (abs(((bx - ax) * (ay - py)) - ((ax - px) * (by - ay)))) / math.sqrt((pow((bx - ax), 2)) + (pow((by - ay), 2)))
    return d

def isLeft(a: list, b: list, c: list) -> bool:
    #rewriting coordinates for simply geometric syntax
    ax, ay, bx, by, cx, cy = a[0], a[1], b[0], b[1], c[0], c[1]

    #we will take point a and point b and do the cross product of these points
    z = ((bx - ax) * (cy - ay)) - ((cx - ax) * (by - ay))

    if z > 0:
        return True
    else:
        return False

def upperHull(a: list, b: list, pList: list):
    #base case for when there are no points to the left of selected vector
    if len(pList) == 0:
        return []

    upperHullPoints = []
    resultPoints = []
    #find p farthest from the line
    maxDis = 0.0
    furthestPoint = []
    for p in pList:
        if isLeft(a, b, p) == True:
            upperHullPoints.append(p)
            pDis = findDistance(a, b, p)
            if(pDis > maxDis):
                maxDis = pDis
                furthestPoint = p

    #add the furthest point to convexHull result (finalList)
    if furthestPoint:
        resultPoints.append(furthestPoint)
    
    #calling upperHull algorithm on region 1 (left of vector a, furthestPoint) and region 3 (left of vector furthestPoint, b)
    region1 = upperHull(a, furthestPoint, upperHullPoints)
    region3 = upperHull(furthestPoint, b, upperHullPoints)

    resultPoints += region1
    resultPoints += region3
    return resultPoints

def draw_hull(hull, canvas):
    color = "red"
    canvas.delete("hull")
    for i in range(len(hull) - 1):
        x1, y1 = hull[i]
        x2, y2 = hull[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill=color, tags="hull")
    canvas.after(dt)
    canvas.update()

def quickhull(points,canvas):
    hull = elimation(points,canvas)
    
    start_point = min(hull, key=lambda p: (p[1], p[0]))
    
    sorted_points = sorted(hull, key=lambda p: (math.atan2(p[1]-start_point[1], p[0]-start_point[0]), p))
    
    if len(sorted_points) >= 3 and sorted_points[0] != sorted_points[-1]:
        sorted_points.append(sorted_points[0])
       
    canvas.delete("hull")
    for i in range(len(sorted_points) - 1):
        x1, y1 = sorted_points[i]
        x2, y2 = sorted_points[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="red", tags="hull")
        
def elimation(pList: list,canvas) -> list:
    convexHullList = []

    #find left-most and right-most points and add to result
    leftPoint = min(pList)
    rightPoint = max(pList)
    convexHullList.append(leftPoint)
    convexHullList.append(rightPoint)

    draw_hull(convexHullList,canvas)
    
    #call upperHull algorithm for upper part of convex hull
    allPointsUpper = upperHull(leftPoint, rightPoint, pList)
    draw_hull(allPointsUpper,canvas)
    
    #call upperHull algorithm for lower part of convex hull (lower hull)
    allPointsLower = upperHull(rightPoint, leftPoint, pList)
    draw_hull(allPointsLower,canvas)
    
    #create final result list (convexHullList)
    convexHullList += allPointsUpper
    convexHullList += allPointsLower

    return convexHullList

def choice(algorithm):
    window = tk.Toplevel(app)
    window.geometry("400x200")
    window.title(algorithm)
    
    
    button_find_hull = tk.Button(window, text=f"Random 20 points", command=lambda: randomp(algorithm), bg='lightblue', fg='black')  # Set button background and foreground (text) colors
    button_find_hull.pack()

def choosepoints(algorithm):
    window = tk.Toplevel(app)
    window.title(algorithm)
    canvas = tk.Canvas(window, width=800, height=600, bg='white')
    canvas.pack()

    points = []

def find_convex_hull(points, canvas, algorithm,window):
    starttime = timeit.default_timer()

    algos[algorithm](points, canvas)
    endtime = timeit.default_timer() - starttime
    label1 = tk.Label(window, text=f"Method {algorithm} took {endtime:.5f} ms", bg='lightgreen')  
    label1.pack()

def randomp(algorithm):
    points = []
    for _ in range(20):
        x, y = random.randint(100,700), random.randint(75, 500)
        points.append([x,y])

    window = tk.Toplevel(app)
    window.title(algorithm)
    canvas = tk.Canvas(window, width=800, height=600, bg='white')
    canvas.pack()

    for i in range(20):
        x, y = points[i][0],points[i][1]
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="pink")
        canvas.create_text(x, y-10,text=f"{x},{y}", fill="black")
    
    button_find_hull = tk.Button(window, text=f"Find Convex Hull for {algorithm}", command=lambda: find_convex_hull(points, canvas, algorithm,window), bg='lightblue', fg='black')  # Set button background and foreground (text) colors
    button_find_hull.pack()

algos = {"Quick Elimination":quickhull}
app = tk.Tk()
app.geometry("400x200")
app.title("Geometric Algorithms")


label = tk.Label(app, text="Homepage - Select an Algorithm", bg='lightgreen')  
label.pack()

button_jarvis_march = tk.Button(text="Quick Elimination", command=lambda: choice("Quick Elimination"), bg='lightpink', fg='black')
button_jarvis_march.pack()

app.mainloop()