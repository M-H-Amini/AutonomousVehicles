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
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.05
COIN_COUNT = 1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 960

class Car(arcade.Sprite):
    def __init__(self,filename,scale):
        arcade.Sprite.__init__(self,filename,scale)
        self.x_direction=random.random()*2-1
        self.y_direction=random.random()*2-1
        self.speed=random.random()*10
        
        
class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Car("images/pic%d"%(i+1) + ".jpg", SPRITE_SCALING_COIN)

            # Position the coin
            '''
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            '''
            coin.center_x = 750
            coin.center_y = 1500
            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        texture = arcade.load_texture("images/street1.jpg")
        arcade.draw_texture_rectangle(SCREEN_HEIGHT/2, SCREEN_WIDTH/2,SCREEN_WIDTH,
                              SCREEN_HEIGHT, texture, 0)
        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    ##  Find pixels around a car in a given radius...
    def around(self,center,radius):
        result=[]
        for i in range(0,360,5):
            result.append([int(center[0]+radius*np.cos(i*180/np.pi)),int(center[1]+radius*np.sin(i*180/np.pi))])
            #print(i)
        #print('len{}'.format(len(result)))
        #print(result)
        return result
    
    def coinSensor(self,car,center):
        radius10=self.around(center,50)
        radius20=self.around(center,70)
        radius10.extend(radius20)
        for i in radius10:
            #print('iiiiiiiii={}'.format(i))
            point=arcade.draw_commands.get_pixel(i[0],i[1])
            if point!=(255,255,255):
                print('Coooooooooooooooooooooooooool')
                car.speed*=-1
                arcade.draw_circle_outline(point[0], point[1], 20, arcade.color.WISTERIA, 8)
                print(center)
                print(i)
                print(point)
                break
    
    
    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        
        for coin in self.coin_list:
            #print('speed{}'.format(coin.speed))
            if 1:#coin.speed!=0:
                coin.center_x += coin.speed*coin.x_direction
                coin.center_y += coin.speed*coin.y_direction
                coin.angle=0
                if coin.x_direction<0:
                    coin.angle=180
                if coin.x_direction==0:
                    coin.angle=0
                else:
                    coin.angle+=np.arctan(coin.y_direction/coin.x_direction)*180/np.pi-90
                    
                    
                if coin.center_x > SCREEN_WIDTH:
                    coin.center_x -= SCREEN_WIDTH
            
                if coin.center_y > SCREEN_HEIGHT:
                    coin.center_y -= SCREEN_HEIGHT
                #aaa=self.around([coin.center_x,coin.center_y],10)
                self.coinSensor(coin,[coin.center_x,coin.center_y])
            #my_point=arcade.draw_commands.get_pixel(100,100)
        
                
        #self.coin_list[1].center_x += 1
        
        self.coin_list.update()

        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()