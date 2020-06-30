
import arcade
from character import PlayerCharacter
WIDTH=1000
HEIGHT=600
HALF=WIDTH//2

GRAVEDAD=1
VEL_MOVIMIENTO= 8
VEL_SALTO= 20
VEL_DIS= 8

TILE_WIDTH= 30
MAP_WIDTH=300*TILE_WIDTH
MAP_HEIGHT=10*TILE_WIDTH



class ventana(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400,200)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.player_x = 100
        self.player_y=150
        self.ground_list = None
        self.physics_engine=None
        disparo= None
        self.setup()



#MAPA
    def setup(self):
        self.mapa = arcade.read_tiled_map("mapa/parque.tmx",1)
        self.ground_list= arcade.generate_sprites(self.mapa,"Capa de patrones 1",2)

        self.sprite1= arcade.Sprite("personaje/personaje.png",2)
        self.disparos= arcade.SpriteList()
        #self.enemigos= arcade.tilemap.process_layer(self.mapa,"enemigo_amarillo")
        #for enemigo in self.enemigos:
        #    enemigo.change_x= 2

       #Fisicasa
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.sprite1, self.ground_list, gravity_constant=GRAVEDAD)
        self.sprite1.set_position(self.player_x, self.player_y)

#PRINTEAR
    def on_draw(self):
        arcade.start_render()
        self.ground_list.draw()
        self.sprite1.draw()
        self.disparos.draw()
        #self.enemigos.draw()

 # POSICION
    def clamp(self, value, mini, maxi):
        return max(min(value, maxi), mini)

 #MOVIMIENTO
    def on_update(self, delta_time):
        #self.enemigos.update()

        self.sprite1.center_x = self.clamp(self.sprite1.center_x, 0, MAP_WIDTH)

        if self.sprite1.center_x > HALF and self.sprite1.center_x < MAP_WIDTH - TILE_WIDTH - HALF:
            camara = True
        else:
            camara = False

        if camara:
            arcade.set_viewport(self.sprite1.center_x - HALF, self.sprite1.center_x + HALF, 0, HEIGHT)

        self.disparos.update()
        for disparo in self.disparos:
            choques=arcade.check_for_collision_with_list(disparo,self.ground_list)
            if len(choques)!=0:
                self.disparos.remove(disparo)
        self.physics_engine.update()


#TECLADO
    def on_key_press(self, symbol, modifiers):
        if symbol== arcade.key.D:
            self.sprite1.change_x = VEL_MOVIMIENTO
        if symbol== arcade.key.A:
            self.sprite1.change_x = -VEL_MOVIMIENTO
        if symbol==arcade.key.W:
            if self.physics_engine.can_jump():
                self.sprite1.change_y = VEL_SALTO
        if symbol==arcade.key.SPACE:
            if self.sprite1.change_x<0:
                disparo = arcade.Sprite("personaje/d2.png",2)
                disparo.center_x = self.sprite1.center_x-50
                disparo.center_y = self.sprite1.center_y-15
                disparo.change_x= -VEL_DIS
                self.disparos.append(disparo)
            else:
                disparo = arcade.Sprite("personaje/d1.png",2)
                disparo.center_x = self.sprite1.center_x+50
                disparo.center_y = self.sprite1.center_y-15
                disparo.change_x = VEL_DIS
                self.disparos.append(disparo)

    def on_key_release(self, symbol, modifiers):
        if symbol== arcade.key.D or symbol ==arcade.key.A:
            self.sprite1.change_x = 0


ventana(WIDTH, HEIGHT, "CATVID-19")
arcade.run()
