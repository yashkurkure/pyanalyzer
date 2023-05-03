# Final Project
# CS 111, Reckinger
# Owen Gutierrez, Shengteng Wu
# Spring 2023
 

import json
import turtlefunc as tf
import numpy as np
from PIL import ImageFont

data = json.load(open('data.json', 'r'))
points = json.load(open('points.json', 'r'))

# calcs. the est. distance between two coords
def calc_dis(coord1, coord2):
  x_dis = abs(coord1[0]-coord2[0])
  y_dis = abs(coord1[1]-coord2[1])
  distance = x_dis+y_dis
  return distance

# compares the coords with min (can merge with determine_closest)
def compare_dis(coord1, coord2, min):
  distance = calc_dis(coord1, coord2)
  if distance < min:
    return True, distance
  else:
    return False, min

# determines closest points to destination
def determine_closest(destination):
  min = 99999
  for i in points:
    dict = data[destination]
    start_coords = dict['coords']
    isLess, min = compare_dis(points[i], start_coords, min)
    if isLess:
      chosen_point = i
  return chosen_point

def clicked_loc(x, y): # allows user to click on valid points
  global num, drawn_path, des_border
  num += 1
  checker.goto(x, y)
  for loc in data:
    xy = data[loc]['coords']
    if(checker.distance(xy[0], xy[1]) < 30 and loc not in startend and drawn_path == False): # gives user leeway on where they click
      checker.goto(xy[0], xy[1]) 
      checker.shape("circle")
      if num == 1:
        checker.color("green")
      else:
        checker.color("red") 
      checker.stamp()
      startend.append(loc) # returns name of location

      des_text = data[loc]['description'] 
      des_border = description(des_text)

      break

def draw_path(): # uses hypotenuse to find the closest location to the current starting point
  global first_time, num, drawn_path, total_distance, des_border
  first_time = True 
  if num >= 2 and drawn_path == False:
    drawn_path = True
    cor_arr = []
    for loc in startend: # creates new list with np.array of the coordinates of each location in startend
      cor_arr.append(np.array(data[loc]['coords']))
    d1 = startend[0] # starting point is first coordinate clicked
    startend.pop(0) # to keep lengths the same
    cor_arr.pop(0)

    while(len(cor_arr) != 0):
      
      p1 = determine_closest(d1) # closest intersection to start_point
      
      print(f'starting point: {p1}')
      current_pos = p1
      if first_time:
        tf.turtle_start(data[d1]['coords'])
        first_time = False
      
      tf.move_turtle(points[current_pos])
      
      cur_int = np.array(points[current_pos])
      dist = np.linalg.norm(cor_arr-cur_int, axis=1) # makes a list of the distances of the closest intersection to all destinations
      min_ind = np.argmin(dist) # finds the index of the closest distance
      d2 = startend[min_ind] # closest destination to the closest intersection

      p2 = determine_closest(d2) # closest intersection to destination
      
      visited_points = []
      while current_pos != p2:
        # this entire section is just to find the two closest points
        points_map = {}
        for i in points:
          if i != current_pos and not i in visited_points:
            distance = calc_dis(points[i], points[current_pos])
            points_map[i] = distance
      
        sorted_points_map = {k: points_map[k] for k in sorted(points_map, key=points_map.get)}
        list_points_map = list(sorted_points_map.keys())
        
        # this decides which point is closer to the destination (more advantageous)
        adj_points = []
        for i in range(4):
          adj_points.append(list_points_map[i])
      
        min = 9999
        for i in adj_points:
          adj_dis = calc_dis(points[i], data[d2]['coords'])
          if adj_dis < min:
            min = adj_dis
            current_pos = i
      
        if current_pos != p2:
          tf.move_turtle(points[current_pos])
          visited_points.append(current_pos)
          print(f'moved to: {current_pos}')

      close_point, moved_distance = tf.move_turtle(data[d2]['coords'])
      total_distance += moved_distance
      print(f'arrived at destination ({current_pos})')
      
      d1 = startend[min_ind] # new starting location
      startend.pop(min_ind) # to keep lengths the same
      cor_arr.pop(min_ind)
      if len(cor_arr) != 0:
        tf.move_turtle(close_point)
        
    write_distance(des_border)

def description(text): # creates description of locations on the left side
  wt.clear()
  wt.color("orange")
  tf.s.tracer(0)
  font = ImageFont.load_default().font 
  text_list = text.split()
  line = text_list[0] + " "
  i = 1
  y = tf.window_y - 110
  while i < len(text_list):
    wt.sety(y)
    size = font.getsize(line + text_list[i] + " ")
    textwidth = size[0]
    if(textwidth > 292 or i == len(text_list) - 1): 
      y -= 20
      if(i == len(text_list)-1): # for the last line of text
        last_size = font.getsize(line + text_list[i] + " ")
        final_width = last_size[0] 

        # if the width size of text with the last word is over 292 then write excess in next line
        if(final_width > 292): 
          wt.write(line, align="left", font=('Ariel', 9, 'normal'))
          line = ""
          wt.sety(y) 
        line += text_list[i] + " "
        wt.write(line, align="left", font=('Ariel', 9, 'normal'))

      else: # if not last line of text just 
        wt.write(line, align="left", font=('Ariel', 9, 'normal'))
        line = "" # resets line to blank for next line
    else:
       line += text_list[i] + " "
    i += 1
  tf.s.tracer(True)
  return y

def write_distance(border): # write path distance of turtle 
  global total_distance
  y = border - 20
  wt.color("turquoise") 
  wt.sety(y)
  total_distance *= 2.5
  if total_distance >= 2640: 
    total_distance /= 5280 # converts to miles
    unit = 'miles'
    total_distance = round(total_distance, 2)
  else:
    unit = 'feet' # converts to feet
  wt.write(f"Total Distance: {total_distance} {unit}", align="left", font=('Ariel', 9, 'normal')) # prints the total distance
  total_distance = 0

def reset_map(): # resets everything
  global num, drawn_path, startend, cor_arr
  checker.clear()
  wt.clear()
  tf.t.clear()
  tf.t.ht()
  drawn_path = False
  startend = [] 
  cor_arr = []
  num = 0
  
  
#========================================================================
# MAIN PROGRAM
#========================================================================
tf.s.bgpic('bg.png')

total_distance = 0
num = 0
startend = []
drawn_path = False

tf.s.onclick(clicked_loc)

tf.s.onkey(draw_path, "d")

tf.s.onkey(reset_map, "c")


checker = tf.turtle.Turtle(visible=False) # use new one to use different speed and not displace where t is at
checker.speed(0)
checker.penup()
tf.intruction_write()

wt = tf.turtle.Turtle(visible=False)
wt.penup()
wt.setx(457)


tf.turtle.listen()
tf.turtle.mainloop() # uncomment once you start doing turtle drawing