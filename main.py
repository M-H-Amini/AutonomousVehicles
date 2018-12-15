"""
Sprite Collect Coins

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade
import os
import numpy as np

# --- Constants ---

#double comment === can be removed!

##SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_CAR = 0.05
CAR_COUNT = 1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 960

class Car(arcade.Sprite):
    def __init__(self,filename,scale):
        arcade.Sprite.__init__(self,filename,scale)
        #comment needed! @MHA WHat is 2 and what is 1 in the next line of code?
        self.x_direction=random.random()*2-1
        self.y_direction=random.random()*2-1
        self.speed=random.random()*10
        
        
class MyMap(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Cars map!")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        ##self.player_list = None
        self.car_list = None

        ## Set up the player info
        ##self.player_sprite = None
        ##self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the map and initialize the variables. """

        # Sprite lists
        ##self.player_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()

        ## Score
        ##self.score = 0

        ## Set up the player
        ## Character image from kenney.nl
        ##self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
        ##self.player_sprite.center_x = 50
        ##self.player_sprite.center_y = 50
        ##self.player_list.append(self.player_sprite)

        # Create the cars
        for i in range(CAR_COUNT):

            # Create the car instance
            car = Car("images/pic%d"%(i+1) + ".jpg", SPRITE_SCALING_CAR)

            # Position the car
            '''
            car.center_x = random.randrange(SCREEN_WIDTH)
            car.center_y = random.randrange(SCREEN_HEIGHT)
            '''
            car.center_x = 370
            car.center_y = 1500
            # Add the car to the lists
            self.car_list.append(car)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        texture = arcade.load_texture("images/street1.jpg")
        arcade.draw_texture_rectangle(SCREEN_HEIGHT/2, SCREEN_WIDTH/2,SCREEN_WIDTH,
                              SCREEN_HEIGHT, texture, 0)
        self.car_list.draw()
        ##self.player_list.draw()

        # Put the text on the screen.
        #output = "Score: {}".format(self.score)
        output = "Computational Intelligence Project"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        ## Move the center of the player sprite to match the mouse x, y
        ##self.player_sprite.center_x = x
        ##self.player_sprite.center_y = y

    # Find pixels around a car in a given radius
    def car_around(self, center, radius):
        result=[]
        #comment needed! @MHA what is 0, 360, 10?
        for i in range(0,360,10):
            result.append([int(center[0] + radius * np.cos(i * 180/np.pi)), int(center[1] + radius * np.sin(i * 180/np.pi))])
            #print(i)
        #print('len{}'.format(len(result)))
        #print(result)
        return result
    
    def car_sensor(self, car, center):
        #comment needed! @MHA what is radius10 and radius20? what is 70 and 75?
        radius10=self.car_around(center,70)
        radius20=self.car_around(center,75)
        
        #comment needed! @MHA
        radius10.extend(radius20)
        for i in radius10:
            point=arcade.draw_commands.get_pixel(i[0],i[1])
            if point!=(255,255,255):
                #Change needed!
                print('Coooooooooooooooooooooooooool')
                
                #car.speed*=-1
                #temp=car.x_direction
                #car.x_direction=-car.y_direction
                #car.y_direction=temp
                
                car.center_x=370
                car.center_y=1500
                car.x_direction=random.random()*2-1
                car.y_direction=random.random()*2-1
                #arcade.draw_circle_outline(point[0], point[1], 20, arcade.color.WISTERIA, 8)
                print(center)
                print(i)
                print(point)
                break
    
    
    def update(self, delta_time):
        """ Movement and map logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        
        for car in self.car_list:
            
            #print('speed{}'.format(coin.speed))
            
            #comment needed! @MHA
            if 1:#coin.speed!=0:
                car.center_x += car.speed*car.x_direction
                car.center_y += car.speed*car.y_direction
                car.angle = 0
                if (car.x_direction < 0):
                    car.angle=180
                if (car.x_direction == 0):
                    car.angle=0
                else:
                    car.angle += np.arctan(car.y_direction / car.x_direction) * 180/np.pi - 90
                    
                    
                if car.center_x > SCREEN_WIDTH:
                    car.center_x -= SCREEN_WIDTH
            
                if car.center_y > SCREEN_HEIGHT:
                    car.center_y -= SCREEN_HEIGHT
                #aaa=self.around([coin.center_x,coin.center_y],10)
                self.car_sensor(car, [car.center_x, car.center_y])
            #my_point=arcade.draw_commands.get_pixel(100,100)
        
                
        #self.coin_list[1].center_x += 1
        
        self.car_list.update()

        ## Generate a list of all sprites that collided with the player.
        ##coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        ## Loop through each colliding sprite, remove it, and add to the score.
        ##for coin in coins_hit_list:
        ##    coin.kill()
        ##    self.score += 1


def main():
    """ Main method """
    window = MyMap()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()