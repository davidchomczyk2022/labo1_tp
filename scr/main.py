
import pygame
import random
#from aleatorios import *
from funciones_block import *
from random import randint, randrange
from sys import exit
from config import *
from colisiones import *
from pygame.locals import *





#inicializar los modulos de pygame
#-------------utlizo  el try excepts en caso que no encuntre la ventana ---------
try:
    pygame.init()
    #---> CONFIGURO LA DIRECCION
    screen = pygame.display.set_mode(size_screen)
except pygame.error:
    print("Error no se pued Abrir la ventana :")
#---> creo un reloj
clock = pygame.time.Clock()

#CONFIGURO LA PANTALLA PRINCIPAL
pygame.display.set_caption("Primer Juego")


# --->seteo sonidos 
golpe_sound = pygame.mixer.Sound("./scr/sounds/laser.mp3")
golpe_nave = pygame.mixer.Sound("./scr/sounds/laser3.mp3")
round_two = pygame.mixer.Sound("./scr/sounds/round-two.mp3")
round_three = pygame.mixer.Sound("./scr/sounds/round-three.mp3")
game_over_sound = pygame.mixer.Sound("./scr/sounds/game-over-1-gameover.mp3")
diparo_laser = pygame.mixer.Sound("./scr/sounds/diaparo_laser.mp3")   
background = pygame.transform.scale(pygame.image.load("./scr/images/espacio_01.jpg"),size_screen)
#--->musica  fondo (solo 1 se permite)
pygame.mixer.music.load("./scr/sounds/primer_sonido.mp3")


# --->  sonido .PLAY tiene 3 parametros
pygame.mixer.music.play()

#-->control de volumen 
pygame.mixer.music.set_volume(0.2)
playing_music = True

#-->creo boton

btn_comenzar= pygame.Rect(screen.get_width() // 2 - size_button[0] // 2, 500, *size_button)

btn_salir= pygame.Rect(screen.get_width() // 2 - size_button2[0] // 2, 550, *size_button2)
#--->CARGA DE IMAGENES

imagen_player = pygame.image.load("./scr/images/nave_1-alcon.png")
imagen_icono = pygame.image.load("./scr/images/icono_juego.png")
imagen_enemiga1 = pygame.image.load("./scr/images/nave_enemiga1.png")  
imagen_enemiga2 = pygame.image.load("./scr/images/nave_enemiga2.png") 
imagen_enemiga3 = pygame.image.load("./scr/images/nave_enemiga3.png") 
imagen_enemiga4 = pygame.image.load("./scr/images/nave_enemiga4.png") 
imagen_enemiga = pygame.image.load("./scr/images/nave_enemiga.png")
imagen_nave = pygame.image.load("./scr/images/nave_star1.png")
imagen_nave2 = pygame.image.load("./scr/images/nave_star2.png")
imagen_asteroide = pygame.image.load("./scr/images/asteroide_2-nuevo.png")

background2 = pygame.transform.scale(pygame.image.load("./scr/images/fondo_2.jpg"),size_screen)

#-->eventos personales
EVENT_NWE_NAVE = pygame.USEREVENT + 1

pygame.time.set_timer(EVENT_NWE_NAVE,4000)

pygame.display.set_icon(imagen_icono)

#-----------creo el bloque donde le agrego la imagen de la nave y le doy los parametros -------
try:
    block = creo_naves_nuevas(imagen_player,randint(0,width - rect_w),randint(0,height - rect_h),
    rect_w,rect_h,get_color(colors),radio= 30)
    
except pygame.error:
    print("Error al ingresar los datos")

try:
    block2 = creo_naves_nuevas(imagen_enemiga2,(width),(-100),
    rect_w,rect_h,speed_y,rebote=True)
    
except pygame.error:
    print("Error al ingresar los datos")

block3 = creo_naves_nuevas(imagen_enemiga3,(height // 2),(-100),
rect_w,rect_h,speed_y,rebote=True)

# block4 = creo_naves_nuevas(imagen_enemiga4,(height),(-100),
# rect_w,rect_h,speed_y,rebote=True,bajando=True)

max_contador = 0

DISPARO_LASER = pygame.USEREVENT 
pygame.time.set_timer(DISPARO_LASER,2000)

while True:#--> aca se reinicia el juego en un bucle
    #---> aca en este punto se reinicia el juego , en un bucle el
    #--> score empieza desde cero
    #---> extablesco fuente
    laser = None
    score = 0
    rafaga = False
    lives = 3
    direccion = 1
    rebote = True
    velocidad_disparos = 100
    colision_enemigo = False
    velocidad = 150
    #-----------UTILIZO try except en caso  que la funte se cargue mal o no se encuentre en el ordenador-----
    try:
        fuente = pygame.font.SysFont("MV Boli",30)
        texto = fuente.render(f"Score :{score}",True,red)
        rec_texto = texto.get_rect()
        rec_texto.midtop = (width // 2 , 30)
    except pygame.error:
        print("Error Fuente no se encuentra : ")    

    mostrar_texto(screen,f"Lives: {lives}",fuente,(200, height -30),magenta)


    #--------creo las naves-------------
    naves = []
    genero_naves(naves,numero_naves,imagen_nave)


    cont_comer = 0

    #-->creo una lista de laseres
    lasers = []
    disparos = []
    disparo = 0
    disparos = []
    disparos_nave1 = []

    #--> aca lo vuelvo hacer vicible al cursos del mouse
    pygame.mouse.set_visible(True)

    screen.blit(background2,origin)
    mostrar_texto(screen,"Estrella de la Muerte",fuente,(width //2 ,50 ),green)
    
    pygame.display.flip()

   #-->creo el boton,, lo muestro en su estado final

    estado = ESTADO_INICIO
    while True:
        if estado == ESTADO_INICIO:
            estado = wait_click_stark(btn_comenzar)
        elif estado == ESTADO_SALIR:
            estado = boton_salir(btn_salir)

        block4 = creo_naves_nuevas(imagen_enemiga4,width - 50, height - height + 100,
        rect_w,rect_h,speed_y,rebote=True,bajando=True)

        #---> aca dejo invicible el mouse
        pygame.mouse.set_visible(False)

        # pygame.mixer.music.play(-1)

        trick_reverse = False
        trick_slow = False

    
        is_running = True
        time_play = FPS * 40

        while is_running:
            #---> aca se crea el tiempo de juego
            time_play -= 1
            if time_play == 0:
                is_running = False

            clock.tick(FPS)
            #--->detectar los eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running = False

                elif event.type == DISPARO_LASER:
                  
                
                    disparos_nave1.append(create_laser_naves_enemigas(block2["rect"].midtop,velocidad_disparos,cyan))
                    disparos_nave1.append(create_laser_naves_enemigas(block3["rect"].midtop,velocidad_disparos,cyan))
                    disparos_nave1.append(create_laser_naves_enemigas(block4["rect"].midtop,velocidad_disparos,cyan))  

                    for disparo in disparos_nave1:
                        if disparo["rect"].bottom >= 0:
                            disparo["rect"].move_ip(0, disparo["velocidad_laser_y"])
                        else:
                            disparos_nave1.remove(disparo)

                    rebote_creado(block2,velocidad,width)
                    rebote_creado(block3,velocidad,width)
                    rebote_creado(block4,velocidad,width) 


                    for disparo in disparos_nave1:
                        if disparo["rect"].colliderect(block["rect"]):
                            disparos_nave1.remove(disparo)
                            if lives > 1:
                                lives -= 1
                            else: 
                                is_running = False
                            if playing_music:
                                golpe_nave.play()

                    
                    colision  = False
                    for disparo in disparos_nave1[:]:
                        if detectar_colision_circulo(disparo["rect"],block["rect"]):
                            disparos_nave1.remove(disparo)
                            score += 1 
                            texto = fuente.render(f"Score :{score}",True,red)
                            rec_texto = texto.get_rect()
                            rec_texto.midtop = (width // 2,30)
                            # cont_comer = 10
                            colision = True
                            if playing_music:
                                golpe_nave.play()
    #----------------------eventos de movimientos con el boton apretado-------------
            
    
                if event.type == KEYDOWN:
                    if event.key == K_f:#-->se creo el evento del disparo laser con la letra f
                        if rafaga:#-->aca se crea la lista de laserss
                            lasers.append(create_laser(block["rect"].midtop,speed_laser,green))
                        else:
                            if not laser:#--> aca sigue normal 
                                laser = create_laser(block["rect"].midtop,speed_laser)
                            if  playing_music:
                                diparo_laser.play()
                    

            
    #-----------> se recrea los movimientos con las teclas d / a / w / s------------------------------->
            
                    
                    if event.key == K_RIGHT or event.key == K_d:
                        move_right = True
                        move_left = False

                    if event.key == K_LEFT or event.key == K_a:
                        move_left = True
                        move_right = False

                    if event.key == K_UP or event.key == K_w:
                        move_up = True
                        move_down = False

                    if event.key == K_DOWN or event.key == K_s:
                        move_down = True
                        move_up = False
    #-------------------------------------------------------------------------------

    # #-----------------> activo los efectos dados con las teclas l /r----------------------------------->
                    if event.key == K_l:
                        trick_slow = True

                    if event.key == K_r:
                        trick_reverse = True
    #-------------------------------------------------------------------------------------------------->
    #---------------> aca se utiliza la letra g para la rafaga de lasers------------------------------->
                    if event.key == K_g:
                        rafaga= True
    
    #--------------> en este evento utilizo la M del teclado para poner un pause el sonido del juego
                    if event.key == K_m:
                        if playing_music:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                        playing_music = not playing_music
    #------------->aca se pausa el juego--------------------------------------------------------------->
                    if event.key == K_p:
                        if playing_music:
                            pygame.mixer.music.pause()
                            mostrar_texto(screen,"PAUSA",fuente,center_scree,red,black)
                            wait_user()
                        if playing_music:
                            wait_user()
                            pygame.mixer.music.unpause()
    # #--------------------------------------------------------------------------------------------------> 
            
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                            move_right = False
                    if event.key == K_LEFT:
                            move_left = False
                    if event.key == K_UP:
                            move_up = False
                    if event.key == K_DOWN:
                            move_down = False
                    #-->desactivo las teclas el efecto / dado
                    if event.key == K_l:
                        trick_slow = False
                    if event.key == K_r:
                        trick_reverse = False
                    #--> aca se utiliza la letra g para la rafaga de lasers(queda en FALSE)
                    if event.key == K_g:
                        rafaga = False
        
                if event.type == EVENT_NWE_NAVE:
                    naves.append(creo_naves_nuevas(imagen_nave,randint(0,width - ancho_nave),randint(0,height - largo_nave),
                                                ancho_nave,largo_nave,green,largo_nave // 1))

    #------------------evento con el mouse apretado-----------------------------------------------------------------------------------
                if event.type == MOUSEBUTTONDOWN:
                    #-->aca se vuelve a utilizar el laser ,con el mouse
                    if event.button == 1:
                        if rafaga:
                            lasers.append(create_laser(block["rect"].midtop,speed_laser,green))
                            if playing_music:
                                diparo_laser.play()
                        else:    
                            if not laser:
                                laser = create_laser(block["rect"].midtop,speed_laser,red)
                            if playing_music:
                                diparo_laser.play()
                    if event.button == 3:
                        block["rect"].center = center_scree
            #----> aca es cuando el mouse se mueva por l apantalla del juego
                if event.type == MOUSEMOTION:
                    block["rect"].center = event.pos
                    
            #----> ACTUALIZO LOS ELEMNTOS------------------->

            # #-------------- movimientos  con las teclas de las flecha---------------------->
            
            if move_up and block["rect"].top >= 0:
                #-->muevo arriba
                block["rect"].top -= SPEED
            if move_down and block["rect"].bottom <= height:
                #--> muevo abajo
                block["rect"].top += SPEED
            if move_left and block["rect"].left >= 0:
                #--->muevo izquierda
                block["rect"].left -= SPEED
            if move_right and block["rect"].right <= width:
                #-->muevo derecha
                block["rect"].left += SPEED
            
            # #------------------movimiento con el mouse-acompañando a al nave----------------------------------->
            pygame.mouse.set_pos(block["rect"].centerx,block["rect"].centery)

            for nave in naves:
                #-->movimiento normal si 
                if not trick_reverse and not trick_slow: #--> aca no pasa nada el movimiento es normal
                    if nave["rect"].top <= height:
                        nave["rect"].move_ip(0,nave["speed_y"])
                    else:
                        nave["rect"].bottom = 0
                elif trick_slow:#--> determino la velocidad mas lento con la letra l
                    if nave["rect"].top <= height:
                        nave["rect"].move_ip(0,1)
                    else:
                        nave["rect"].bottom = 0
                elif trick_reverse:#-->aca los pongo en reversa a los asteroides en caso de apretar la letra r
                    if nave["rect"].top <= height:
                        nave["rect"].move_ip(0,- nave["speed_y"])

                #--->creo el movimiento del laser 
                #----> si existe el laser ?
                #-->creo la rafaga y si existe disparo la rafaga y si NO disparo normal
                #--> aca recorro una copia de la lista de lasers
            if rafaga:
                for laser in lasers[:]:
                    if laser["rect"].bottom >= 0:
                        laser["rect"].move_ip(0, -laser["velocidad_laser_y"])
                    else:
                        #-->si el laser salio de la pantalla lo destruyo
                        lasers.remove(laser)
            else:
                if laser:
                        #--->si el laser esta dentro de la pantgalla lo muevo
                    if laser["rect"].bottom >= 0:
                        laser["rect"].move_ip(0, -laser["velocidad_laser_y"])
                    else:
                        #-->si el laser salio de la pantalla lo destruyo
                        laser = None  
          #  -----------------------------------------------------------------   
            if rafaga:
                for laser in lasers[:]:
                        #-->de detecta colicion de la nave con laser
                    colision  = False
                    for nave in naves[:]:
                        if detectar_colision_circulo(nave["rect"],laser["rect"]):
                            naves.remove(nave)
                            score += 1 
                            texto = fuente.render(f"Score :{score}",True,red)
                            rec_texto = texto.get_rect()
                            rec_texto.midtop = (width // 2,30)
                            cont_comer = 10
                            colision = True
                            if playing_music:
                                golpe_sound.play()

                            if len(naves) == 0:
                                genero_naves(naves,numero_naves,imagen_nave2)
                                round_two.play()
                            # elif len(naves) == 5:
                            #     genero_naves(naves,numero_naves,imagen_nave2)
                            #     round_three.play()
                    if colision:
                        lasers.remove(laser)
            else:
                if laser:
                        #-->de detecta colicion de la nave con el laser
                    colision  = False
                    for nave in naves[:]:
                        if detectar_colision_circulo(nave["rect"],laser["rect"]):
                            naves.remove(nave)
                            score += 1 
                            texto = fuente.render(f"Score :{score}",True,red)
                            rec_texto = texto.get_rect()
                            rec_texto.midtop = (width // 2,30)
                            # cont_comer = 10
                            colision = True
                            if playing_music:
                                golpe_nave.play()
                            
                            if len(naves) == 0:
                                genero_naves(naves,numero_naves,imagen_nave2)
                                round_two.play()
                    if colision:
                        laser = None

                    #-----detecto colicion y descuento las vidas
            for nave in naves[:]:
                    if detectar_colision_circulo(nave["rect"],block["rect"]):
                        naves.remove(nave)
                        if lives > 1:
                            lives -= 1
                        else:
                            game_over_sound.play()
                            is_running = False
                            # cont_comer = 10
                        if playing_music:
                            golpe_nave.play()
    #------------------------------------------------------------------------------            
            if cont_comer >= 2:
                cont_comer -= 1
                block2["rect"].width = rect_w + 5
                block2["rect"].height = rect_h + 5
            else:
                #block2["rect"].width = rect_w
                block2["rect"].height = rect_h
    #------------------------------------------------------------------------------>

            #---> dibujar pantalla-------------------->
            #screen.fill(black)
            screen.blit(background,origin)

            #dibujar_naves(screen,naves)
            dibujar_naves(screen,naves)
                
            #pygame.draw.rect(screen,block["color"],block["rect"],block["borde"],block["radio"])
            screen.blit(block["imagen"],block["rect"])
            #-->creo el lasery creo la rafaga de lasers
            if rafaga:
                for laser in lasers:
                    pygame.draw.rect(screen,laser["color"],laser["rect"])
            else:
                if laser:
                    pygame.draw.rect(screen,laser["color"],laser["rect"])
    #----------------------dibujo los disparos de las naves enemigas-------------------------->
            for disparo in disparos_nave1:
                pygame.draw.rect(screen,disparo["color"],disparo["rect"])  

            screen.blit(block2["imagen"],block2["rect"])

            for disparo in disparos_nave1:
                pygame.draw.rect(screen,disparo["color"],disparo["rect"])     

            screen.blit(block3["imagen"],block3["rect"])

            for disparo in disparos_nave1:
                pygame.draw.rect(screen,disparo["color"],disparo["rect"])   

            screen.blit(block4["imagen"],block4["rect"])


        #---> aca mostramos las vidas que tenemos al comenzar
            mostrar_texto(screen,f"Lives: {lives}",fuente,(100, height -30),magenta)
            mostrar_texto(screen,f"Score:{score}",fuente,(140, 20),green)
            
            mostrar_texto(screen,f"Time:{time_play:2d}",fuente,(140, 60),green)
            if time_play == 0:
                mostrar_texto(screen," Time Finished ",fuente,center_scree,red)
            mostrar_texto(screen,f"Top Score:{max_contador}",fuente,(width - 150, 20),green)
            #----->ACTUALIZO PANTALLA----------------->
            pygame.display.flip()


        if score > max_contador:
            max_contador = score

        #--> aca doy los mensajes del score el juego termino y una tecla precionar para continuar

        pygame.mixer.music.stop()
        game_over_sound.play()
        screen.fill(black)
        mostrar_texto(screen,f"Score:{score}",fuente,(140, 20),green)
        mostrar_texto(screen,f"Top Score:{max_contador}",fuente,(width - 150, 20),green)
        mostrar_texto(screen,"Game Over",fuente,center_scree,red)
        mostrar_texto(screen,"Presione una tecla para comenzar....",fuente,(width //2 , height - 50 ),blue)
        pygame.display.flip()

        wait_user()

    terminar()

    #         tiempo_actual = pygame.time.get_ticks()
        #         if tiempo_actual -tiempo_ultimo_disparo > intervalo_disparo:
        #             for blocks in [block2,block3,block4]:
        #                 x_disparo = blocks["rect"].midbottom and blocks["rect"].width // 2
        #                 y_disparo = blocks["rect"].midbottom  and blocks["rect"].height
        #             disparos.append(pygame.Rect(x_disparo,y_disparo,10,15))

        #     #----------mover los disparos   hacia abajo
        #         for disparo in disparos:
        #             disparo.y += velocidad_disparos       
        # #---------elimino los disparos q salen de la pantalla--------
        #         disparos = [disparo for disparo in disparos if disparo.y < height]