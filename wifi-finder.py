import numpy as np
from src import point, vector, line, source

# Initializing Wifi source at random 3D location, which we don't know
sx, sy, sz = np.random.randint(0, 100, 1)[0], np.random.randint(0, 100, 1)[0],  np.random.randint(0, 100, 1)[0]

wifi = source.Source(sx, sy, sz)

# Initializing our Detector at 0,0,0
initx, inity, initz = 0, 0, 0

# Getting Intensity of WIfi Signal
start = point.Point(initx, inity, initz)
start.Intensity(wifi)

#################################### XY PLANE ###########################################

# Moving to 1,1,0 from 0,0,0
init_p1, init_p2 = point.Point(initx, inity, initz), point.Point(1, 1, initz)

# Moving Along XY Plane
# Creating a line path where our detector should be moving to detect the source
init_line = line.Line(init_p1, init_p2, axis=2)

# Moving along above defined line to find 2D location
interation = 100
found = False
counter = 0
step = 1

inten1 = start.Intensity(wifi)
while found is False and counter < interation:
    
    
    start.MoveAlongLine_xy(init_line, step)
    inten2 = start.Intensity(wifi)
    
    if inten2 < inten1:
        step = -step/3
    
    if abs((inten2 - inten1) *100 / inten1) < 0.005:
        found = True
        
    inten1, inten2 = inten2, None
    
# Intensity of Signal will be maximum when distance between source point and line is Minimum
# At the point of minimum distance (Perpendicular to line),
# Wifi will be present at perpendicular distance to the line 
new_direction = init_line.GetPerpendicularFromPoint(start, axis=2)
print('Line towards WIfi Source, Slope: {}, Intercept: {}'.format(new_direction.slope_xy, new_direction.intercept_xy))

# Now resetting our detector to origin 0, 0, 0
# Move along another direction to get one more line point towards wifi,
# So that we can find interection between these 2 lines to get 2D Coordinate of Wifi
start.Goto(initx, inity, initz) 

# Moving in the direction of new line from Starting point
interation = 100
found = False
counter = 0
step = 1

inten1 = start.Intensity(wifi)
while found is False and counter < interation:
    
    
    start.MoveAlongLine_xy(new_direction, step)
    inten2 = start.Intensity(wifi)
    
    if inten2 < inten1:
        step = -step/3
    
    if abs((inten2 - inten1) *100 / inten1) < 0.005:
        found = True
        
    inten1, inten2 = inten2, None

# Intensity of Signal will be maximum when distance between source point and line is Minimum
# At the point of minimum distance (Perpendicular to line),
# Wifi will be present at perpendicular distance to the line 
new_direction_2 = new_direction.GetPerpendicularFromPoint(start, axis=2)        

# Finding intersection of these 2 lines to get 2D coordinate of Wifi
wifi_prediction = line.Line.IntersectLine(new_direction, new_direction_2, axis=2)

px = round(wifi_prediction.x, 0)
py1 = round(wifi_prediction.y, 0)
print('2D Coordinate of Wifi Source, X: {}, Y: {}'.format(px, py1))

#################################### YZ PLANE ###########################################
# Moving Along YZ Plane
# Creating a line path where our detector should be moving to detect the source
init_p1, init_p3 = point.Point(initx, inity, initz), point.Point(initx, 1, 1)

# Creating a line along which Detector will move
init_line_2 = line.Line(init_p1, init_p3, axis=3)

# Moving along above defined line to find 2D location in YZ Plane
interation = 100
found = False
counter = 0
step = 1

inten1 = start.Intensity(wifi)
while found is False and counter < interation:
    
    
    start.MoveAlongLine_yz(init_line_2, step)
    inten2 = start.Intensity(wifi)
    
    if inten2 < inten1:
        step = -step/3
    
    if abs((inten2 - inten1) *100 / inten1) < 0.005:
        found = True
        
    inten1, inten2 = inten2, None
    
# Intensity of Signal will be maximum when distance between source point and line is Minimum
# At the point of minimum distance (Perpendicular to line),
# Wifi will be present at perpendicular distance to the line 
new_direction = init_line_2.GetPerpendicularFromPoint(start, axis=3)

print('Line towards WIfi Source, Slope: {}, Intercept: {}'.format(new_direction.slope_yz, new_direction.intercept_yz))

# Now resetting our detector to origin 0, 0, 0
# Move along another direction to get one more line point towards wifi,
# So that we can find interection between these 2 lines to get 2D Coordinate in YZ Plane of Wifi 
start.Goto(initx, inity, initz)

# Moving in the direction of new line from Starting point
interation = 100
found = False
counter = 0
step = 1

inten1 = start.Intensity(wifi)
while found is False and counter < interation:
    
    
    start.MoveAlongLine_yz(new_direction, step)
    inten2 = start.Intensity(wifi)
    
    if inten2 < inten1:
        step = -step/3
    
    if abs((inten2 - inten1) *100 / inten1) < 0.005:
        found = True
        
    inten1, inten2 = inten2, None
    
# Intensity of Signal will be maximum when distance between source point and line is Minimum
# At the point of minimum distance (Perpendicular to line),
# Wifi will be present at perpendicular distance to the line 
new_direction_2 = new_direction.GetPerpendicularFromPoint(start, axis=3)

# Finding intersection of these 2 lines to get 2D coordinate in YZ Plane of Wifi
wifi_prediction = line.Line.IntersectLine(new_direction, new_direction_2, axis=3)

# YZ Coordinate
py2 = round(wifi_prediction.y, 0)
pz = round(wifi_prediction.z, 0)

# 3D coordinate calculated
print('3D Coordinate Estimated as: ')
print('X: {}, Y: {}, Z: {}'.format(px, (py1 + py2)/2, pz))

print('Original 3D coordinate of Wifi: X: {}, Y: {}, Z: {}'.format(sx, sy, sz))