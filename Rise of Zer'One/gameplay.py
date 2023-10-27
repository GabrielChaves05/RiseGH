from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *

janela=Window(1333,750)
janela.set_title("Rise of Zer'One")
background=GameImage("cidade2_background.png")

#Cenário
chao=janela.height-190
paredeE=GameImage("parede.png")
paredeE.set_position(-paredeE.width,0)
paredeD=Sprite("parede.png")
paredeD.set_position(janela.width,0)

#HUD
vida=Sprite("vida4.png")
vida.set_position(20,20)
habilidade=Sprite("habilidade.png")
habilidade.set_position(250,20)

#Jogador
jogador=Sprite("zuckin_idle.png",2)
jogador.set_total_duration(1300)
jogador.set_position(0, chao)
jogadorxspeed=350
speed=jogadorxspeed
jogadoryspeed=0

#Inimigos
drone=Sprite("drone_idle.png",6)
drone.set_total_duration(1000)
drone.set_position(janela.width-drone.width, 0)


teclado=Window.get_keyboard()
run=False
idle=0
pulo=False
ult='d'
while True:
    background.draw()
    jogador.draw()
    drone.draw()
    vida.draw()
    habilidade.draw()

    #Movimento Horizontal
    if teclado.key_pressed("A"):
        jogador.move_x(-jogadorxspeed * janela.delta_time())
        ult='a'
    if teclado.key_pressed("D"):
        jogador.move_x(jogadorxspeed * janela.delta_time())
        ult='d'

    x=jogador.x
    y=jogador.y
    #Pulo
    if teclado.key_pressed("W"):
        if pulo==False:
            jogadoryspeed=-1200
            jogador.move_y(jogadoryspeed * janela.delta_time())
            if ult=='a':
                jogador=Sprite("zuckin_jumpE.png")
            elif ult=='d':
                jogador=Sprite("zuckin_jump.png")
            jogador.set_total_duration(1000)
            jogador.x=x
            jogador.y=y
            pulo=True
    
    #Gravidade e Detecção do Chão
    if jogador.y+(jogadoryspeed * janela.delta_time())<chao:
        jogadoryspeed+=60
        jogador.move_y(jogadoryspeed * janela.delta_time())
    else:
        jogador.y=chao
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

    if Collision.collided(jogador,paredeE):
        jogadorxspeed=0
        jogador.move_x(1)
    elif Collision.collided(jogador,paredeD):
        jogadorxspeed=0
        jogador.move_x(-1)
    else:
        jogadorxspeed=speed

    jogador.update()
    drone.update()
    janela.update()