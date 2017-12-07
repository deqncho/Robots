from gasp import *
from pydub import AudioSegment
import random
import os
import pygame

#TODO: Implement walls (this will be a hard one)
# newComment

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = None

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall():
    def inBetween(self, robot, player):
        pass

class HorizontalWall(Wall):
    def __init__(self, start_x, end_x, pos_y):
        self.start_x = start_x
        self.end_x = end_x
        self.pos_y = pos_y

    def extend_wall(self, junk):
        for j in junk:
            if (j.x == self.start_x - 1 and j.y == self.pos_y):
                self.start_x -= 1
            elif (j.x == self.end_x + 1 and j.y == self.pos_y):
                self.end_x  +=1

    def inBetween(self, robot, player):
        if ((robot.y < self.pos_y < player.y) and (self.start_x<=robot.x<=self.end_x)
            and (self.start_x<=player.x<=self.end_x)):
            return True
        else:
            return False

class VerticalWall(Wall):
    def __init__(self, start_y, end_y, pos_x):

        self.start_y = start_y
        self.end_y = end_y
        self.pos_x = pos_x

    def extend_wall(self, junk):
        for j in junk:
            if (j.y == self.start_y - 1 and j.x == self.pos_x):
                self.start_y -= 1
            elif (j.y == self.end_y + 1 and j.x == self.pos_y):
                self.end_y +=1

    def inBetween(self, robot, player):
        if ((robot.x < self.pos_x < player.x) and (self.start_y <= robot.y <= self.end_y)
            and (self.start_y <= player.y <= self.end_y)):
            return True
        else:
            return False

def collided(thing1, list_of_things):
    for thing2 in list_of_things:
        if thing1.x == thing2.x and thing1.y == thing2.y:
            return True
    return False

def place_player():
    player = Player(random_between(0, 71), random_between(0, 47))
    return player


def checkWhoSeesPlayer(robots, player, junk):
    """
    Basic function that returns who sees the player.
    Only works for walls of 1 junk.
    To be implemented with walls consisting of more than 1 junk.

    :param robots:
    :param player:
    :param junk:
    :return:
    """
    robotsThatSeePlayer = []
    robotsThatDontSeePlayer = []
    for index_robot, evil_robot in enumerate(robots):
        for trash in junk:
            if ((player.x < trash.x < evil_robot.x and (player.y == trash.y == evil_robot.y)) or
                    ((evil_robot.x < trash.x < player.x) and (player.y == trash.y == evil_robot.y)) or
                    ((player.y < trash.y < evil_robot.y) and (player.x == trash.x == evil_robot.x)) or
                    ((evil_robot.y < trash.y < player.y) and (player.x == trash.x == evil_robot.x))):
                robotsThatDontSeePlayer.append(index_robot)

    robotsThatSeePlayer = [rob for index, rob in enumerate(robots) if index not in robotsThatDontSeePlayer]
    return robotsThatSeePlayer

def place_robots(limitBots):
    robots = []
    while len(robots) < limitBots:
        evilBot = Robot(random_between(0, 71), random_between(0, 47))
        evilBot.x = random_between(0, 71)
        evilBot.y = random_between(0, 47)
        if not collided(evilBot, robots):
            evilBot.shape = Box((10 * evilBot.x, 10 * evilBot.y), 10, 10)
            robots.append(evilBot)
    return robots

def safely_place_player(robots, junk):
    player = place_player()
    while collided(player, robots + junk):
        del player
        player = place_player()
    player.shape = Circle((10 * player.x + 5, 10 * player.y + 5), 5, filled=True)

    return player


def move_player(robots, junk, player, teleportsLeft, teleportsInfo):
    key = update_when('key_pressed')  # makes the program wait for user key before doing anything else

    while key == '5':

        if teleportsLeft > 0:
            teleportsLeft = teleportsLeft - 1
            remove_from_screen(teleportsInfo)
            teleportsInfo = Text("Teleports:" + str(teleportsLeft), (10, 450), size=15)
            remove_from_screen(player.shape)
            player = safely_place_player(robots, junk)
        key = update_when("key_pressed")

    if key == '6':
        player.x = (player.x + 1) % 72
    elif key == '3':

        if player.x != 71 and player.y != 0:

            player.x = player.x + 1
            player.y = player.y - 1
        elif player.x == 71 and player.y == 0:
            player.x = 0
            player.y = 47
        elif player.x == 71 and player.y != 0:
            player.x = 71 - 47 + player.y
            player.y = 47
        elif player.x != 71 and player.y == 0:
            if player.x - 47 <= 0:
                player.y = player.x
                player.x = 0
            else:
                player.y = 47
                player.x = player.x - 47

    elif key == '1':
        if player.x == 0 and player.y == 47:
            pass
        elif player.x == 0 and player.y == 0:
            player.x = 71
            player.y = 47
        elif player.x != 0 and player.y != 0:
            player.x = player.x - 1
            player.y = player.y - 1
        elif player.x == 0 and player.y != 0:
            player.x = 47 - player.y
            player.y = 47
        elif player.x != 71 and player.y == 0:
            if player.x <= 71 - 47:
                player.y = 47
                player.x = player.x + 47
            else:
                player.y = 71 - player.x
                player.x = 71


    elif key == '2':
        player.y = (player.y - 1) % 48
    elif key == '4':
        player.x = (player.x - 1) % 72
    elif key == '7':
        if player.x != 0 and player.y != 47:
            player.x = player.x - 1
            player.y = player.y + 1
        elif player.x == 0 and player.y == 47:
            player.x = 71
            player.y = 0
        elif player.y != 47 and player.x == 0:
            player.x = player.y
            player.y = 0
        elif player.y == 47 and player.x != 0:
            if player.x <= 71 - 47:
                player.x = player.x + 47
                player.y = 0
            else:
                player.y = -71 + player.x + 47
                player.x = 71

    elif key == '8':
        player.y = (player.y + 1) % 48
    elif key == '9':
        if player.x == 71 and player.y == 0:
            pass
        elif player.x == 71 and player.y == 47:
            player.x = 0
            player.y = 0
        elif player.y != 47 and player.x != 71:
            player.x += 1
            player.y += 1
        elif player.x == 71 and player.y != 47:
            player.x = 71 - player.y
            player.y = 0
        elif player.x != 71 and player.y == 47:
            if player.x >= 47:
                player.y = 0
                player.x = player.x - 47
            else:
                player.y = 47 - player.x
                player.x = 0

    if key != '5':
        move_to(player.shape, (10 * player.x + 5, 10 * player.y + 5))

    return player, teleportsInfo, teleportsLeft


def move_robots(robots, player):
    for rob in robots:

        if rob.x < player.x and rob.y > player.y:
            rob.x += 1
            rob.y -= 1
        elif rob.x == player.x and rob.y > player.y:
            rob.y -= 1
        elif rob.x > player.x and rob.y > player.y:
            rob.x -= 1
            rob.y -= 1
        elif rob.y == player.y and rob.x > player.x:
            rob.x -= 1
        elif rob.y < player.y and rob.x > player.x:
            rob.x -= 1
            rob.y += 1
        elif rob.y < player.y and rob.x == player.x:
            rob.y += 1
        elif rob.y < player.y and rob.x < player.x:
            rob.x += 1
            rob.y += 1
        elif rob.y == player.y and rob.x < player.x:
            rob.x += 1

        move_to(rob.shape, (10 * rob.x, 10 * rob.y))


def checkCollisions():
    global player, robots, junk
    return collided(player, robots)


def robot_crashed(the_bot, robots):
    for a_bot in robots:
        if a_bot == the_bot:  # we have reached our self in the list
            return False
        if a_bot.x == the_bot.x and a_bot.y == the_bot.y:  # a crash
            return a_bot
    return False

timesDied = 0

def game():
    key = None
    finished = False
    stayInMenu = True
    global timesDied
    while stayInMenu:
        Text("Times died:" + str(timesDied), (600, 430), size=15)
        Text("Choose difficulty (use number keys):", (35, 430), size=20)
        Text("1. Easy", (35, 400), size=20)
        Text("2. Medium", (35, 370), size=20)
        Text("3. Hard", (35, 340), size=20)
        Text("4. Impossible", (35, 310), size=20)
        Text("5. Instructions", (35, 250), size=20)

        key = update_when('key_pressed')

        if key == '`':
            stayInMenu = False
            numbots = 1
            teleportsLeft = 100

        if key == '1':
            stayInMenu = False
            numbots = 10
            teleportsLeft = 1000
        if key == '2':
            stayInMenu = False
            numbots = 50
            teleportsLeft = 20
        if key == '3':
            stayInMenu = False
            numbots = 100
            teleportsLeft = 5
        if key == '4':
            stayInMenu = False
            numbots = 600
            teleportsLeft = 3
        if key == '5':
            clear_screen()
            Text("Use numpad to move horizontally, vertically and diagonally.", (35, 310), size=15)
            Text("Use number 5 to teleport.", (35, 290), size=15)
            if update_when('key_pressed') or update_when('mouse_clicked'):
                clear_screen()
        clear_screen()

        if key != '1' and key != '2' and key != '3' and key != '4' and key != '5':
            Text("Please enable numpad", (120, 150), size=15)
            Text("and enter correct key.", (120, 135), size=15)
            sleep(2)
            clear_screen()

    clear_screen()
    teleportsInfo = Text("Teleports:" + str(teleportsLeft), (10, 450), size=15)
    robots = place_robots(numbots)
    junk = []
    walls = []

    # TODO: Modulise code into functions

    player = safely_place_player(robots, junk)
    while not finished:
        died = False
        robotsThatSeePlayerBeforeMove = checkWhoSeesPlayer(robots, player, junk)
        player, teleportsInfo, teleportsLeft = move_player(robots, junk, player, teleportsLeft, teleportsInfo)

        move_robots(robotsThatSeePlayerBeforeMove, player)

        crashedOnMove = []
        crashedInJunk = []
        for bot in robots:
            if robot_crashed(bot, robots):
                crashedOnMove.append(bot)
                crashedOnMove.append(robot_crashed(bot, robots))
                junk.append(bot)

        crashedOnMove = list(set(crashedOnMove))
        for crashed in crashedOnMove:
            remove_from_screen(crashed.shape)
        junk = list(set(junk))
        for j in junk:
            j.shape = Box((10 * j.x, 10 * j.y), 10, 10, filled=True)

        robots = [x for x in robots if x not in crashedOnMove]

        for bot0 in robots:
            if collided(bot0, junk):
                crashedInJunk.append(bot0)

        for junked in crashedInJunk:
            if junked is not None:
                remove_from_screen(junked.shape)

        robots = [y for y in robots if y not in crashedInJunk]

        if len(robots) == 0:
            if not finished:
                sleep(0.4)
                clear_screen()
                finished = True

                winningText = Text("You win!", (250, 240), size=48)

        if (collided(player, robots + junk)):
            sleep(0.4)
            finished = True
            clear_screen()
            if not died:
                timesDied += 1
                died = True
                key_text = Text("You died!", (250, 240), size=48)

        robotsThatSeePlayerAfterMove = checkWhoSeesPlayer(robots, player, junk)
        move_robots(robotsThatSeePlayerAfterMove, player)

        crashedOnMove = []
        crashedInJunk = []
        for bot in robots:
            if robot_crashed(bot, robots):
                crashedOnMove.append(bot)
                crashedOnMove.append(robot_crashed(bot, robots))
                junk.append(bot)

        crashedOnMove = list(set(crashedOnMove))
        for crashed in crashedOnMove:
            remove_from_screen(crashed.shape)
        junk = list(set(junk))
        for j in junk:
            j.shape = Box((10 * j.x, 10 * j.y), 10, 10, filled=True)

        robots = [x for x in robots if x not in crashedOnMove]

        for bot0 in robots:
            if collided(bot0, junk):
                crashedInJunk.append(bot0)

        for junked in crashedInJunk:
            if junked is not None:
                remove_from_screen(junked.shape)

        robots = [y for y in robots if y not in crashedInJunk]

        if len(robots) == 0:
            if not finished:
                sleep(0.4)
                clear_screen()
                finished = True

                winningText = Text("You win!", (250, 240), size=48)

        if (collided(player, robots + junk)):
            if not died:
                sleep(0.4)
                finished = True
                clear_screen()
                timesDied += 1
                key_text = Text("You died!", (250, 240), size=48)

    sleep(1.5)
    clear_screen()
    del robots
    del junk
    del player
    del teleportsInfo
    del teleportsLeft

    game()

if __name__ == '__main__':

    if os.path.isfile('./mergedTrack.mp3'):
        os.remove('./mergedTrack.mp3')

    music = ['./audio/track7.mp3', './audio/track8.mp3', './audio/track9.mp3', './audio/track10.mp3',
             './audio/track11.mp3', './audio/track12.mp3', './audio/track13.mp3', './audio/track14.mp3']

    random.shuffle(music)
    paths = []
    soundsToMerge = []

    for track in music:
        paths.append(os.path.abspath(track))

    for path in paths:
        audio = AudioSegment.from_mp3(path)
        soundsToMerge.append(audio)

    trackToPlay = reduce((lambda x, y: x + y), soundsToMerge)
    trackToPlay.export("./audio/mergedTrack.mp3", format="mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('./audio/mergedTrack.mp3')
    pygame.mixer.music.play(-1)

    begin_graphics(720, 480)
    game()
