from gasp import *
import random

def place_player():
    global player_x, player_y
    player_x = random_between(0,63)
    player_y = random_between(0,47)






def place_robot():
    global robot_x, robot_y, robot_shape

    robot_x = random_between(0,63)
    robot_y = random_between(0,47)
    robot_shape = Box((10*robot_x + 5,10*robot_y + 5),5,5,filled = False)


def collided():
    if player_x == robot_x and player_y == robot_y:
        return True
    else:
        return False

def safely_place_player():
    global player_shape
    place_player()

    while collided():
        place_player()
    player_shape = Circle((10*player_x+5, 10*player_y+5), 5, filled=True)

def move_player():
    global player_x, player_y, player_shape

    key = update_when('key_pressed') # makes the program wait for user key before doing anything else

    while key == '5':
        remove_from_screen(player_shape)
        safely_place_player()
        key = update_when("key_pressed")


    if key == '6' and player_x < 63:
        player_x += 1
    elif key == '3':
        if player_x < 63:
            player_x += 1
        if player_y > 0:
            player_y -= 1
    elif key == '1':
        if player_x >0:
            player_x -= 1
        if player_y >0:
            player_y -= 1

    elif key == '2' and player_y>0:
        player_y -= 1
    elif key == '4' and player_x >0:
        player_x -=1
    elif key == '7':
        if player_x >0:
            player_x -= 1
        if player_y < 47:
            player_y += 1
    elif key == '8' and player_y< 47:
        player_y += 1
    elif key == '9':
        if player_x<63:
            player_x +=1
        if player_y<47:
            player_y +=1




    if key != '5':
        move_to(player_shape, (10*player_x+5, 10*player_y+5))



def move_robot():

    global robot_x, robot_y, robot_shape
    global player_x, player_y, player_shape
    if robot_x < player_x and robot_y > player_y:
        robot_x +=1
        robot_y -=1
    elif robot_x == player_x and robot_y > player_y:
        robot_y -=1
    elif robot_x > player_x and robot_y > player_y:
        robot_x -= 1
        robot_y -=1
    elif robot_y == player_y and robot_x > player_x:
        robot_x -=1
    elif robot_y < player_y and robot_x > player_x:
        robot_x -=1
        robot_y +=1
    elif robot_y < player_y and robot_x == player_x:
        robot_y +=1
    elif robot_y < player_y and robot_x < player_x:
        robot_x +=1
        robot_y +=1
    elif robot_y == player_y and robot_x < player_x:
        robot_x +=1


    move_to(robot_shape, (10*robot_x+5, 10*robot_y+5))


def checkCollisions():
    return collided()

begin_graphics()
finished = False


place_robot()
safely_place_player()
while not finished:
    move_player()
    move_robot()
    if (collided()):
        finished = True
        remove_from_screen(player_shape)
        remove_from_screen(robot_shape)
        key_text = Text("Game Over", (175, 240), size=48)
        sleep(4)


end_graphics()
