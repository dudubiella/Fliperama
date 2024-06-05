import pygame
import os

class Passaro:
    # Define a imagem deste objeto
    caminho = os.path.dirname(__file__) + '\\imgs'
    IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(caminho,'bird3.png')))
    ]
    # Constantes da animação da rotação
    ROTACAO_MAX = 25
    VEL_ROTACAO = 20
    TEMPO_ANIMAÇAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.cont_img = 0
        self.img = self.IMGS[0]
    
    # Almenta a velocidade para cima do Passaro
    def pular(self):
        self.velocidade = -10.5
        # Tempo da função da queda
        self.tempo = 0
        self.altura = self.y

    # Move o Passaro
    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        # S = So + Vo * t + a * t ** 2 / 2 
        deslocamento = self.velocidade * self.tempo + 1.5 * (self.tempo ** 2)

        ## Restringir o deslocamento
        # Vel Max
        if deslocamento > 16:
            deslocamento = 16

        # Impulso no pulo

        elif deslocamento < 0:
            deslocamento -= 2

        # Desloca o Passaro
        self.y += deslocamento

        # define a angulação para cima e o mantem por um tempo assim
        if deslocamento < 0 or self.y < self.altura + 50:
            # Limita a angulação maxima
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
            
            # Limita a angulação mínima
        else:
            if self.angulo > -90:
                self.angulo -= self.VEL_ROTACAO

    def desenhar(self, tela):
        # Definir qual imagem do passado usar
        self.cont_img += 1

        # Cria a animação de bater de assas
        if self.cont_img < self.TEMPO_ANIMAÇAO:
            self.img = self.IMGS[0]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 2:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 3:
            self.img = self.IMGS[2]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4:
            self.img = self.IMGS[1]
        elif self.cont_img < self.TEMPO_ANIMAÇAO * 4 + 1:
            self.img = self.IMGS[0]
            self.cont_img = 0

        # Não bate assas caso o Passaro esteja caindo
        if self.angulo <= -80:
            self.img = self.IMGS[1]
            self.cont_img = self.TEMPO_ANIMAÇAO * 2

        ## Desenha a imagem
        # Roda a imagem
        img_rot = pygame.transform.rotate(self.img, self.angulo)
        # Define o centro
        centro = self.img.get_rect(topleft = (self.x, self.y)).center
        # Cria um retangulo em volta
        retangulo = img_rot.get_rect(center = centro)
        # Desenha na tela
        tela.blit(img_rot, retangulo.topleft)

    # Cria a mascara de pixels para futuramente definir se há colisão
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
