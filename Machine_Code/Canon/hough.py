import cv2
import numpy as np

# from tkinter import Tk
# from tkinter.filedialog import askopenfilename

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def get_coords(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]
    
    def get_equation(self):
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - m * self.x1
        return m, b

def detect(img_arr, gray_arr, filter, angle1=0, angle2=np.pi, req=0): #req = 0, 1, or 2
    filtered = cv2.filter2D(src=gray_arr, ddepth=-1, kernel=filter)
    #cv2.imwrite("show_blurred_" + str(req) + ".png", filtered)

    # Find the edges in the image using canny detector
    img = img_arr.copy()
    thresh1 = 35
    thresh2 = 60
    if req == 2:
        thresh1 = 30
        thresh2 = 50
    edges = cv2.Canny(filtered, thresh1, thresh2)

    # Detect points that form a line
    threshold = 40
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold, min_theta=angle1, max_theta=angle2)

    try:
        for line in lines:
            try:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                if (req == 0) or (req == 1 and x1 < img.shape[1]/3) or (req == 2 and x1 > img.shape[1]*2/3):
                    found_line = Line(x1, y1, x2, y2)
                    coords = found_line.get_coords()
                    cv2.line(img, coords[0], coords[1], (0, 0, 255), 3)
                    break
            except:
                i = 0
    except:
        i = 0
    # Show result
    #cv2.imwrite("show_edges_" + str(req) + ".png", edges)
    return img, found_line

def line_detection(file): #full path name
    kernel0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])/72
    kernel1 = np.array([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]])/72
    kernel2 = np.array([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]])/72
    
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    # Convert the image to gray-scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image, bottom = detect(image, gray, kernel0, angle1=np.pi*7/16, angle2=np.pi*9/16)
    image, left = detect(image, gray, kernel1, angle1=np.pi*7/8, angle2=np.pi*9/8, req=1)
    image, right = detect(image, gray, kernel2, angle1=np.pi*7/8, angle2=np.pi*9/8, req=2)
    #cv2.imwrite("show_result.png", image)
    return image, bottom, left, right #each line is in the format [(x1, y1), (x2, y2)]

def in_tube(curr_x, curr_y, bottom, left, right): #assumes x and y are within the boundaries of the image
    m, b = bottom.get_equation()
    try:
        if curr_y >= (m * curr_x + b):
            return False
    except:
        print(curr_x)
        print(curr_y)
        import traceback
        traceback.print_exc()
        return False
    
    m, b = left.get_equation()
    #if curr_x <= (m * left.x1 + curr_y - left.y1) / m:
    if curr_x <= (curr_y - b) / m:
        return False
    
    m, b = right.get_equation()
    #if curr_x >= (m * right.x1 + curr_y - right.y1) / m:
    if curr_x >= (curr_y - b) / m:
        return False
    
    return True