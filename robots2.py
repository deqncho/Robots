from gasp import *
import random

class Player:
    pass

class Robot:
    pass

class Junk:
    pass

junk = []
deadBots = []
numbots = 10

def collided(thing1, list_of_things):
    for thing2 in list_of_things:
        if thing1.x == thing2.x and thing1.y == thing2.y:
            return True
    return False


def place_player():
    global player
    player = Player()
    player.x = random_between(0,63)  # put the var in the instance of the class Player
    player.y = random_between(0,47)

def place_robots():
    global robots, junk
    junk = []
    robots = []
    while len(robots)<numbots:
        robot = Robot()
        robot.x = random_between(0,63)
        robot.y = random_between(0,47)
        if not collided(robot,robots):
            robot.shape = Box((10*robot.x, 10*robot.y),10,10)
            robots.append(robot)


def safely_place_player():
    global player
    place_player()

    while collided(player,robots+junk):
        place_player()
    player.shape = Circle((10*player.x, 10*player.y), 5, filled=True)

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



def move_robots():

    global robots,player

    for rob in robots:

        if rob.x < player.x and rob.y > player.y:
            rob.x +=1
            rob.y -=1
        elif rob.x == player.x and rob.y > player.y:
            rob.y -=1
        elif rob.x > player.x and rob.y > player.y:
            rob.x -= 1
            rob.y -=1
        elif rob.y == player.y and rob.x > player.x:
            rob.x -=1
        elif rob.y < player.y and rob.x > player.x:
            rob.x -=1
            rob.y +=1
        elif rob.y < player.y and rob.x == player.x:
            rob.y +=1
        elif rob.y < player.y and rob.x < player.x:
            rob.x +=1
            rob.y +=1
        elif rob.y == player.y and rob.x < player.x:
            rob.x +=1

        move_to(rob.shape, (10*rob.x+5, 10*rob.y+5))

def checkCollisions():
    global player, robots,junk
    return collided(player,robots)


def robot_crashed(the_bot):
    for a_bot in robots:
        if a_bot == the_bot:    # we have reached our self in the list
            return False
        if a_bot.x == the_bot.x and a_bot.y == the_bot.y:  # a crash
            return a_bot
    return False

begin_graphics()

finished = False

Text("Choose difficulty:", (35,430), size = 20 )
Text("1. Easy", (35,400), size = 20 )
Text("2. Medium", (35,370), size = 20 )
Text("3. Hard", (35,340), size = 20 )
Text("4. Impossible", (35,310), size = 20 )

key = update_when("key_pressed")

if key == '1':
    numbots = 10
if key == '2':
    numbots = 50
if key == '3':
    numbots = 100
if key == '4':
    numbots = 400

elif key != '1' and key != '2' and key != '3' and key !='4':
    while key != '1' and key != '2' and key != '3' and key !='4':
        clear_screen()
        Text("Please enter correct key",(150,150), size = 25)
        sleep(2)
        clear_screen()
        Text("Choose difficulty:", (35,430), size = 20 )
        Text("1. Easy", (35,400), size = 20 )
        Text("2. Medium", (35,370), size = 20 )
        Text("3. Hard", (35,340), size = 20 )
        Text("4. Impossible", (35,310), size = 20 )

        key = update_when("key_pressed")

        if key == '1':
            numbots = 10
        if key == '2':
            numbots = 50
        if key == '3':
            numbots = 100
        if key == '4':
            numbots = 400



clear_screen()

place_robots()
safely_place_player()
while not finished:
     move_player()
     move_robots()

     crashedOnMove = []
     crashedInJunk = []
     for bot in robots:
         if robot_crashed(bot)!=False:
             crashedOnMove.append(bot)
             crashedOnMove.append(robot_crashed(bot))
             junk.append(bot)



     crashedOnMove = list(set(crashedOnMove))
     for crashed in crashedOnMove:
         remove_from_screen(crashed.shape)
     junk = list(set(junk))
     for j in junk:
         j.shape = Box((10*j.x,10*j.y),10,10,filled = True)


     robots = [x for x in robots if x not in crashedOnMove]

     for bot0 in robots:
         if collided(bot0,junk):
            crashedInJunk.append(bot0)


     for junked in crashedInJunk:
         if junked is not None:
             remove_from_screen(junked.shape)

     robots = [y for y in robots if y not in crashedInJunk]

     if len(robots)==0:
         clear_screen()
         finished = True




         winningText = Text("You win",(220, 240), size=48)
         sleep(4)

     if (collided(player,robots + junk)):
         finished = True
         clear_screen()

         key_text = Text("Game Over", (175, 240), size=48)
         sleep(4)
update_when("key_pressed")

end_graphics()
