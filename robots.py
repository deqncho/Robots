from gasp import *
import random

class Player:
    pass

class Robot:
    pass

def place_player():
    global player
    player = Player()
    player.x = random_between(0,63)
    player.y = random_between(0,47)






def place_robot():
    global robot
    robot = Robot()
    robot.x = random_between(0,63)
    robot.y = random_between(0,47)
    robot.shape = Box((10*robot.x + 5,10*robot.y + 5),5,5,filled = False)


def collided():
    if player.x == robot.x and player.y == robot.y:
        return True
    else:
        return False

def safely_place_player():
    global player
    place_player()

    while collided():
        place_player()
    player.shape = Circle((10*player.x+5, 10*player.y+5), 5, filled=True)

def move_player():
    global player

    key = update_when('key_pressed') # makes the program wait for user key before doing anything else

    while key == '5':
        remove_from_screen(player.shape)
        safely_place_player()
        key = update_when("key_pressed")


    if key == '6' and player.x < 63:
        player.x += 1
    elif key == '3':
        if player.x < 63:
            player.x += 1
        if player.y > 0:
            player.y -= 1
    elif key == '1':
        if player.x >0:
            player.x -= 1
        if player.y >0:
            player.y -= 1

    elif key == '2' and player.y>0:
        player.y -= 1
    elif key == '4' and player.x >0:
        player.x -=1
    elif key == '7':
        if player.x >0:
            player.x -= 1
        if player.y < 47:
            player.y += 1
    elif key == '8' and player.y< 47:
        player.y += 1
    elif key == '9':
        if player.x<63:
            player.x +=1
        if player.y<47:
            player.y +=1




    if key != '5':
        move_to(player.shape, (10*player.x+5, 10*player.y+5))



def move_robot():

    global robot,player

    if robot.x < player.x and robot.y > player.y:
        robot.x +=1
        robot.y -=1
    elif robot.x == player.x and robot.y > player.y:
        robot.y -=1
    elif robot.x > player.x and robot.y > player.y:
        robot.x -= 1
        robot.y -=1
    elif robot.y == player.y and robot.x > player.x:
        robot.x -=1
    elif robot.y < player.y and robot.x > player.x:
        robot.x -=1
        robot.y +=1
    elif robot.y < player.y and robot.x == player.x:
        robot.y +=1
    elif robot.y < player.y and robot.x < player.x:
        robot.x +=1
        robot.y +=1
    elif robot.y == player.y and robot.x < player.x:
        robot.x +=1


    move_to(robot.shape, (10*robot.x+5, 10*robot.y+5))


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
        remove_from_screen(player.shape)
        remove_from_screen(robot.shape)
        key_text = Text("Game Over", (175, 240), size=48)
        sleep(4)


end_graphics()
