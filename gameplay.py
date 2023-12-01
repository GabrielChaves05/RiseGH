from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *
from teste import *



#Tiro do Jogador


def col_chao(altura):
    global jogador
    global pulo
    global run

    jogador.y=altura
    y=jogador.y
    x=jogador.x
    if pulo==True:
        if ult=='a':
            jogador=Sprite("zuckin_idleE.png",2)
        elif ult=='d':
            jogador=Sprite("zuckin_idle.png",2)
        jogador.set_total_duration(1300)
        jogador.x=x
        jogador.y=y
        run=False
    pulo=False

def det_chao(obj):
    if Collision.collided(jogador,obj):
        global jogadoryspeed
        tj=jogador.x+jogador.width
        to=obj.x+obj.width
        if tj-10 >= obj.x and jogador.x+10 <= to:
            jogadoryspeed=0
            col_chao(obj.y-jogador.height)
        elif tj >= obj.x and tj <= obj.x+10:
            jogador.set_position(obj.x-jogador.width, jogador.y)
        elif jogador.x <= to and jogador.x >= to-10:
            jogador.set_position(to, jogador.y)

def est_pulo():
    global jogador
    global pulo
    x=jogador.x
    y=jogador.y
    if ult=='a':
        jogador=Sprite("zuckin_jumpE.png")
    elif ult=='d':
        jogador=Sprite("zuckin_jump.png")
    jogador.set_total_duration(1000)
    jogador.x=x
    jogador.y=y
    pulo=True


janela=Window(1333,750)
janela.set_title("Rise of Zer'One")
background=GameImage("cidade2_background.png")

#Cenário
chao=janela.height-170

chaot=GameImage("chao.png")
chaot.set_position(0, chao+20+chaot.height)

paredeE=GameImage("parede.png")
paredeE.set_position(-paredeE.width,0)
paredeD=GameImage("parede.png")
paredeD.set_position(janela.width,0)
carro1=GameImage("carro2.png")
carro1.set_position(500, chao-60)

#HUD
vidas=4
habilidade=Sprite("habilidade.png")
habilidade.set_position(250,20)

#Jogador
jogador=Sprite("zuckin_idle.png",2)
jogador.set_total_duration(1300)
jogador.set_position(0, chao-10)
jogadorxspeed=400
jogadoryspeed=0

#Armas
bala_speed=1200
bala_delay=0.3
bala_tick=bala_delay
balas=[]
tiro_car=0
direcao_x = 0
direcao_y = 0

#Inimigos
drone=Sprite("drone_idleE.png",6)
drone.set_total_duration(1000)
drone.set_position(janela.width-drone.width, 0)
drone_speed=500
direita=False
laser=Sprite("laser.png")
laser_delay=2.5
laser_tick=laser_delay


teclado=Window.get_keyboard()
mouse=Window.get_mouse()

run=False
idle=0
pulo=False
ult='d'
while True:
    background.draw()
    jogador.draw()
    drone.draw()
    carro1.draw()
    chaot.draw()
    habilidade.draw()
    if vidas==4:
        vida=Sprite("vida4.png")
    elif vidas==3:
        vida=Sprite("vida3.png")
    elif vidas==2:
        vida=Sprite("vida2.png")
    elif vidas==1:
        vida=Sprite("vida1.png")
    vida.set_position(20,20)
    vida.draw()

    #Movimento Horizontal
    if teclado.key_pressed("A"):
        jogador.move_x(-jogadorxspeed * janela.delta_time())
        ult='a'
    if teclado.key_pressed("D"):
        jogador.move_x(jogadorxspeed * janela.delta_time())
        ult='d'

    #Pulo
    if teclado.key_pressed("W"):
        if not pulo:
            jogadoryspeed=-1500
            jogador.move_y(jogadoryspeed * janela.delta_time())
            est_pulo()
    
    #Gravidade e Detecção do Chão
    if jogador.y+(jogadoryspeed * janela.delta_time())<chao:
        if jogadoryspeed<=3000:
            jogadoryspeed+=30
        jogador.move_y(jogadoryspeed * janela.delta_time())
    det_chao(chaot)
    det_chao(carro1)
    

    x=jogador.x
    y=jogador.y
    #Animação Idle
    if idle==1 and pulo==False:
        if ult=='a':
            jogador=Sprite("zuckin_idleE.png",2)
        elif ult=='d':
            jogador=Sprite("zuckin_idle.png",2)
        jogador.set_total_duration(1300)
        jogador.x=x
        jogador.y=y
        run=False

    #Animação Run
    if teclado.key_pressed("A") or teclado.key_pressed("D"):
        if not(teclado.key_pressed("A") and teclado.key_pressed("D")):
            idle=0
            if run==False and pulo==False:
                if teclado.key_pressed("A"):
                    jogador=Sprite("zuckin_runE.png",4)
                if teclado.key_pressed("D"):
                    jogador=Sprite("zuckin_run.png",4)
                jogador.set_total_duration(600)
                jogador.x=x
                jogador.y=y
                run=True
        else:
            idle+=1
    else:
        idle+=1

    #Limites Laterais
    if Collision.collided(jogador,paredeE):
        jogador.set_position(paredeE.x+paredeE.width, jogador.y)
    elif Collision.collided(jogador,paredeD):
        jogador.set_position(paredeD.x-jogador.width, jogador.y)

    #Atirar
    bala_tick+=janela.delta_time()
    if mouse.is_button_pressed(1) and bala_tick>=bala_delay:
        vet_balas(0, ult, jogador, balas)
        bala_tick=0
    if mouse.is_button_pressed(3) and tiro_car==10:
        vet_balas(1, ult, jogador, balas)
        tiro_car=0

    #Atualização das Balas
    for b in balas:
        if (b[0].x + b[0].width <= 0) or (b[0].x >= janela.width) or (b[0].y <= 0) or (b[0].y + b[0].height >= janela.height):
            balas.remove(b)

        elif Collision.collided_perfect(b[0],carro1):
            balas.remove(b)

        elif Collision.collided(b[0], drone):
            if b[0]!=laser:
                balas.remove(b)
                if tiro_car<10:
                    tiro_car+=1
        
        elif Collision.collided(b[0], jogador):
            if b[0]==laser:
                balas.remove(b)
                vidas-=1
                

        b[0].draw()
        b[0].move_x(b[1]*bala_speed*janela.delta_time())
        b[0].move_y(b[2]*bala_speed*janela.delta_time())


    #Movimento Drone
    if not direita:
        if drone.x>=100:
            drone.move_x(-drone_speed*janela.delta_time())
        else:
            x=drone.x
            y=drone.y
            drone=Sprite("drone_idle.png",6)
            drone.set_total_duration(1000)
            drone.x=x
            drone.y=y
            direita=True
        laser_x=drone.x-laser.width

    if direita:
        if drone.x<=janela.width-drone.width-100:
            drone.move_x(drone_speed*janela.delta_time())
        else:
            x=drone.x
            y=drone.y
            drone=Sprite("drone_idleE.png",6)
            drone.set_total_duration(1000)
            drone.x=x
            drone.y=y
            direita=False
        laser_x=drone.x+drone.width

    #Atirar Drone
    laser_tick+=janela.delta_time()
    if laser_tick>=laser_delay:
        laser_tick=0

        alvo_x=jogador.x+(jogador.width/2)
        alvo_y=jogador.y+(jogador.height/2)
        laser=Sprite("laser.png")
        laser.set_position(laser_x, drone.y+(drone.height/2))

        direcao_x = alvo_x-laser.x
        direcao_y = alvo_y-laser.y
        mag=((direcao_x**2)+(direcao_y)**2)**(1/2)
        direcao_x/=mag
        direcao_y/=mag

        balas.append([laser,direcao_x,direcao_y])

    janela.draw_text("{}%".format(tiro_car*10), janela.width/2, 0, size=50, color=(255,0,0), font_name="Comic Sans", bold=True, italic=False)

    jogador.update()
    drone.update()
    janela.update()