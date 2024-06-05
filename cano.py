import pygame
import os
import random

class Cano:
    # Define a imagem deste objeto
    IMAGEM = pygame.transform.scale2x(pygame.image.load(os.path.join(os.path.dirname(__file__) + '\\imgs','pipe.png')))

    # Defina a distância entre os canos
    DISTANCIA = 200
    # Define a velocidade dos canos
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(self.IMAGEM, False, True)
        self.CANO_BASE = self.IMAGEM
        self.passou = False
        self.def_altura()

    # Define a altura dos novos canos aleatoriamente
    def def_altura(self):
        self.altura = random.randrange(50, 500)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    # Move os Canos
    def mover(self):
        self.x -= self.VELOCIDADE
    
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
