import pygame
import os
import random

class Cano:
    # Define a imagem deste objeto
    IMAGEM = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','pipe.png')))

    def __init__(self, x, dificuldade = 0):
        self.tipo = random.randrange(0, 2)
        self.x = x
        self.dificuldade = dificuldade
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(self.IMAGEM, False, True)
        self.CANO_BASE = self.IMAGEM
        self.passou = False
        self.velocidade = 5
        self.distancia = 200
        if self.dificuldade == 1:
            self.dificuldade = random.randrange(0,2)
        elif self.dificuldade == 2:
            self.distancia = 190
        self.def_altura()

    # Define a altura dos novos canos aleatoriamente
    def def_altura(self):
        self.altura = random.randrange(100, 301)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.distancia

    # Move os Canos
    def mover(self):
        vel_y = 0
        match self.dificuldade:
            case 0:
                self.velocidade = 10
            case 1:
                self.velocidade = 10
                vel_y = 2
            case 2:
                self.velocidade = 12
                vel_y = 3

        self.x -= self.velocidade

        if vel_y != 0:
            self.move_y(vel_y)

    def move_y(self, vel):
        match self.tipo:
            case 0:
                self.pos_topo += vel
                self.pos_base += vel
            case 1:
                self.pos_topo -= vel
                self.pos_base -= vel
        if self.pos_topo < -500 and self.tipo != 0:
            self.tipo = 0
        elif self.pos_base > 500 and self.tipo != 1:
            self.tipo = 1
    # Desenha os Canos
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    # Define se algum Passaro colide com o Cano
    def colidir(self, passaro):
        # Retira as mascaras do tamanho em pixes de cada objeto
        pass_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # Define a distancia do Passaro dos Canos
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # Verifica se tem pixes sobrepostos dos objetos (colisão)
        topo_ponto = pass_mask.overlap(topo_mask, distancia_topo)
        base_ponto = pass_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False
