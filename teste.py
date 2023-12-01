from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.collision import *


def vet_balas(tipo, ult, jogador, balas):
    mouse=Window.get_mouse()

    x=mouse.get_position()[0]
    y=mouse.get_position()[1]
    if ult=='d':
        x_bala=jogador.x+jogador.width-20
    elif ult=='a':
        x_bala=jogador.x

    if tipo==0:
        bala=Sprite("zero.png")
    elif tipo==1:
        bala=Sprite("um.png")
    bala.set_position(x_bala, jogador.y+(jogador.height/2)-20)
    
    direcao_x = x-bala.x
    direcao_y = y-bala.y
    mag=((direcao_x**2)+(direcao_y)**2)**(1/2)
    direcao_x/=mag
    direcao_y/=mag
    balas.append([bala,direcao_x,direcao_y])