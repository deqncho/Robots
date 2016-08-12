from gasp import *
import random

begin_graphics()


c1 = Circle((10,10),10)
update_when("key_pressed")
x = 5
y = 5

while x<630 and y<470:
    x = x+4.04
    y = y+3
    move_to(c1,(x,y))
    sleep(0.012)
update_when("key_pressed")
end_graphics()
